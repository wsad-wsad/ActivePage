from threading import Lock
from typing import Any, List

from openai import OpenAI
from openai.types.chat import ChatCompletionDeveloperMessageParam
from pydantic import BaseModel

from src.prompt import PROMPT_SYSTEM_START


class ModelWithCache:
    """
    Append only kv cache, with structure:
    1. fix cache: system prompt for the AI to understand what is the task
    2. fix cache: book text with append every page
    3. not fix cache: specific prompt to use so it doesn't need to calculate step 1 & 2 couple of times
    """

    def __init__(self, max_tokens: int = 8192):
        self.client = OpenAI(
            base_url="http://localhost:8100/v1", api_key="sk-no-key-required"
        )
        self._model_alias = "gemma-4"
        self._max_tokens = max_tokens
        self._lock = Lock()

        self.current_page = 0
        self._fixed_text_cache = ""

    def _full_fixed_cache(
        self, general_prompt: str | None = None
    ) -> List[ChatCompletionDeveloperMessageParam]:
        messages = [
            {"role": "system", "content": PROMPT_SYSTEM_START},
            {
                "role": "assistant",
                "content": f"Here is the book: {self._fixed_text_cache}",
            },
        ]
        if general_prompt:
            messages.append({"role": "system", "content": general_prompt})
        return messages  # type:ignore

    def append_fixed_cache(self, new_pages: List[str]):
        with self._lock:
            for page in new_pages:
                self.current_page += 1
                self._fixed_text_cache += f"\n<Page {self.current_page}>: {page}"

            self.client.chat.completions.create(
                model=self._model_alias,
                messages=self._full_fixed_cache(),
                max_tokens=3,
            )

    def clear_cache(self):
        self.current_page = 0
        self._fixed_text_cache = ""

    def chat_specific_prompt(
        self,
        specific_prompt: str,
        text: str,
        previous_conversation: List[dict] | None = None,
        temperature: float = 1,
    ):
        with self._lock:
            chat = self._full_fixed_cache(specific_prompt) + [
                {"role": "user", "content": text}
            ]
            if previous_conversation:
                chat += previous_conversation

            response = self.client.chat.completions.create(
                model=self._model_alias,
                messages=chat,  # type: ignore
                max_tokens=self._max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content

    def invoke_specific_prompt(self, specific_prompt: str, temperature: float = 1):
        with self._lock:
            response = self.client.chat.completions.create(
                model=self._model_alias,
                messages=self._full_fixed_cache(specific_prompt),
                max_tokens=self._max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content

    def invoke_specific_prompt_struct(
        self,
        specific_prompt: str,
        output_schema: BaseModel | Any,
        temperature: float = 1,
    ):
        with self._lock:
            response = self.client.chat.completions.parse(
                model=self._model_alias,
                messages=self._full_fixed_cache(specific_prompt),
                response_format=output_schema,  # type:ignore
                max_tokens=self._max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.parsed
