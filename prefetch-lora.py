import os
os.environ['HF_ENDPOINT']='https://hf-mirror.com'
os.environ['HF_HOME']='/data/users/example/h3-turbo4/cache/huggingface'
from huggingface_hub import hf_hub_download
print(hf_hub_download('larryvrh/MiniMax-H3-Turbo-Lora','minimax_h3_turbo_v4_step600_ema.safetensors',revision='43a74557ac3f6539db8e0f2a959d03feb7a81480',local_dir='/data/users/example/h3-turbo4/models/turbo-v4'),flush=True)
