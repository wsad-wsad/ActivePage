# 📖 Active Page: Tackling Local AI for the Best Active Recall Experiences

Active Page is a privacy-first, local-LLM-powered reading companion designed to solve the "forgetting curve." By leveraging the cutting-edge Gemma 4 E2B model, it transforms passive reading into an interactive learning session through real-time, contextual active recall—running entirely on your machine.

---

## ⚡ Quick Start
### 1. Prerequisites
### 2. Initialization
The `init.sh` script automates the heavy lifting: it manages dependencies via uv, compiles llama.cpp for your specific hardware, and pulls the optimized Gemma 4 E2B weights.

```Bash
bash init.sh
```
  Note for Silicon/AMD: If using Apple M-Series or AMD GPUs, edit init.sh to enable GGML_METAL=ON or GGML_HIPBLAS=ON respectively for hardware acceleration.
  
### 3. Launch
Launch the inference engine and the interactive web interface simultaneously:

```Bash
bash run.sh
```
Access the application at: http://localhost:8000

### 🔧 Troubleshooting
System Crashing / Out of Memory in the init.sh?
If your ram or CPU is limited, adjust the pararrel of building the llama.cpp.
- Decrese the -j
- Ensure no other memory-intensive apps are running.

System Crashing / Out of Memory in the run.sh?
If your GPU VRAM is limited, adjust the Offload Layers in run.sh:
- Decrease the -ngl (number of GPU layers) value to shift more work to your CPU.
- Ensure no other memory-intensive apps are running.
