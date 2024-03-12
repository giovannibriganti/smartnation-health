# smartnation-health

Resources available: 

1. Wheels Llama cpp python with CuBlas https://github.com/Smartappli/llama-cpp-python-cuBLAS-wheels

-  CPU builds for CPU : https://github.com/Smartappli/llama-cpp-python-cuBLAS-wheels/releases/tag/cpu
-  Wheels builds for Nvidia GPUs: https://github.com/Smartappli/llama-cpp-python-cuBLAS-wheels/releases/tag/wheels
-  ROCm builds for AMD GPUs: https://github.com/smartappli/llama-cpp-python-cuBLAS-wheels/releases/tag/rocm  
-  Metal builds for MacOS 11.0+: https://github.com/smartappli/llama-cpp-python-cuBLAS-wheels/releases/tag/metal

2. Quantized models (GGUF files) : https://alumniumonsac-my.sharepoint.com/:f:/g/personal/532807_umons_ac_be/Eqq5KOeq3yxCmGhUYpbqHBwBFRYjRg5XjqsUUnlYvXoOOA?e=lK8MAn

3. Serge Chat: https://github.com/serge-chat/serge

🐳 Docker:
```bash
docker run -d \
    --name serge \
    -v weights:/usr/src/app/weights \
    -v datadb:/data/db/ \
    -p 8008:8008 \
    ghcr.io/serge-chat/serge:latest
```
4. Starting Code: https://github.com/Smartappli/hackathon
