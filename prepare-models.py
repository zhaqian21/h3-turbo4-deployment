import os, json, pathlib
R=pathlib.Path('/data/users/example/h3-turbo4')
os.environ['HF_ENDPOINT']='https://hf-mirror.com'
os.environ['HF_HOME']=str(R/'cache/huggingface')
os.environ['MODELSCOPE_CACHE']=str(R/'cache/modelscope')
from modelscope.hub.api import HubApi
api=HubApi()
files=api.get_model_files('MiniMax/MiniMax-H3',recursive=True)
(R/'models/modelscope-manifest.json').write_text(json.dumps(files,indent=2))
print(json.dumps(files[:8],indent=2),flush=True)
from modelscope import snapshot_download
p=snapshot_download('MiniMax/MiniMax-H3',local_dir=str(R/'models/MiniMax-H3'),allow_file_pattern=['FL2VA/*','configuration.json','README.md','LICENSE'],max_workers=8)
print('BASE_READY',p,flush=True)
from huggingface_hub import hf_hub_download
p=hf_hub_download('larryvrh/MiniMax-H3-Turbo-Lora','minimax_h3_turbo_v4_step600_ema.safetensors',revision='43a74557ac3f6539db8e0f2a959d03feb7a81480',local_dir=str(R/'models/turbo-v4'))
print('LORA_READY',p,flush=True)
