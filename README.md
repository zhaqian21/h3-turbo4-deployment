# MiniMax H3 Turbo v4 deployment notes

This repository archives the scripts, launch arguments, and diagnostic logs from a four-GPU SGLang deployment attempt on 2026-11-04. Model verification completed for 81 files. SGLang failed to start when linking its CUDA JIT extensions. The run produced no videos.

- [MiniMax H3 base model](https://modelscope.cn/models/MiniMax/MiniMax-H3), FL2VA variant
- [Turbo v4 LoRA, pinned revision](https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora/tree/43a74557ac3f6539db8e0f2a959d03feb7a81480)
- [Launch arguments](launch-args.json) and [server startup log](logs/server.log)
- [Download log](logs/download.log.gz), compressed with gzip

The scripts capture the original environment setup. Before rerunning them, substitute your workspace for /data/users/example/h3-turbo4 and fill in your GPU UUIDs in start-server.py. Account-specific paths, GPU UUIDs, and IPs from the build log were replaced for publication. The scripts reference the external downloads used to set up the original environment.
