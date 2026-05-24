from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.AI_cache_manager import ModelWithCache
from src.prompt import PROMPT_USER_QUESTION, prompt_mcq
from src.schema import Mcq, UserQuestionOut

app = FastAPI()
model = ModelWithCache()
chat_conversation = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("./src/index.html", "r") as f:
    home_html = f.read()


@app.get("/")
def home():
    return HTMLResponse(home_html)


@app.post("/add-page")
def add_page(page: str):
    model.append_fixed_cache([page])


@app.delete("/book")
def delete_book():
    model.clear_cache()


@app.get("/chat")
def chat(text: str):
    out = model.chat_specific_prompt(
        PROMPT_USER_QUESTION, text, chat_conversation, temperature=0.3
    )
    chat_conversation.append({"role": "user", "content": text})
    return out


@app.delete("/chat")
def new_chat():
    """to get new chat, delete the old chat conversation"""
    chat_conversation.clear()


@app.get("/mcq")
def make_mcq() -> UserQuestionOut:
    """
    multiple choice question with provided right & wrong answer and explanation.
    """
    mcq_raw: UserQuestionOut = model.invoke_specific_prompt_struct(
        prompt_mcq(model.current_page), UserQuestionOut, temperature=1
    )  # type:ignore

    mcq = []
    for mcq_item in mcq_raw.mcq:
        question = mcq_item.question
        right_answer = mcq_item.right_answer
        wrong_answers = mcq_item.wrong_answer
        explanation = mcq_item.explanation

        try:
            wrong_answers.remove(
                right_answer
            )  # sometime the agent give duplicate answer
        except Exception:
            pass

        if len(wrong_answers) > 4:
            print(f"more than 4 wrong answer: {wrong_answers}")

        mcq.append(
            Mcq(
                question=question,
                right_answer=right_answer,
                wrong_answer=wrong_answers,
                explanation=explanation,
            )
        )
    return UserQuestionOut(mcq=mcq)
