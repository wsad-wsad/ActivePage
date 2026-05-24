#!/bin/bash
uv venv .venv
uv sync & uv lock
deactivate

curl -L "https://huggingface.co/unsloth/gemma-4-E2B-it-GGUF/resolve/main/gemma-4-E2B-it-Q4_K_M.gguf?download=true" -o gemma-4-E2B-it-Q4_K_M.gguf
curl -L "https://huggingface.co/AtomicChat/gemma-4-E2B-it-assistant-GGUF/resolve/main/gemma-4-E2B-it-assistant.Q8_0.gguf?download=true" -o gemma-4-E2B-it-assistant.Q8_0.gguf

git clone https://github.com/AtomicBot-ai/atomic-llama-cpp-turboquant
cd atomic-llama-cpp-turboquant

mkdir build
cd build

cmake .. -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON
cmake --build . --config Release --target llama-server -j10
