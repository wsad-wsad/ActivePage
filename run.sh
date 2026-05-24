#!/bin/bash
source .venv/bin/activate

cleanup() {
    echo "Stopping servers..."
    kill $(jobs -p)
    exit
}
trap cleanup SIGINT

uvicorn api:app & ./atomic-llama-cpp-turboquant/build/bin/llama-server \
  -m ./gemma-4-E2B-it-Q4_K_M.gguf \
  --mtp-head ./gemma-4-E2B-it-assistant.Q8_0.gguf \
  --spec-type mtp \
  --draft-block-size 2 --draft-max 4 --draft-min 0 \
  --chat-template-kwargs '{"enable_thinking":false}' \
  -ctk turbo4 -ctv turbo4 \
  -ctkd turbo4 -ctvd turbo4 \
  -c 131072 -fa on \
  --port 8100 --no-webui

wait

deactivate
