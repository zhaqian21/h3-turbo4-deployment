import os,json,pathlib
os.environ['HF_ENDPOINT']='https://hf-mirror.com'
from huggingface_hub import HfApi
r=pathlib.Path('/data/users/example/h3-turbo4')
m=HfApi().model_info('MiniMaxAI/MiniMax-H3',revision='42ed227ee7df40d41602854ae760620d6eb651fe',files_metadata=True)
a=[{'path':f.rfilename,'size':f.size,'sha256':f.lfs.sha256 if f.lfs else None} for f in m.siblings if f.rfilename.startswith('FL2VA/')]
(r/'models/official-fl2va-manifest.json').write_text(json.dumps({'revision':m.sha,'files':a},indent=2));print('manifest_files',len(a),flush=True)
