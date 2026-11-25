import pathlib,json,subprocess,os,time,socket
r=pathlib.Path('/data/users/example/h3-turbo4')
for _ in range(90):
    v=json.loads((r/'models/base-verification.json').read_text())
    if v.get('success'):break
    if v.get('mismatch'):raise RuntimeError(v['mismatch'])
    time.sleep(20)
else:raise TimeoutError('Weights not verified')
pidfile=r/'server.pid'
if pidfile.exists():
    p=pathlib.Path('/proc')/pidfile.read_text().strip()/'cmdline'
    if p.exists() and b'h3-turbo4' in p.read_bytes():raise RuntimeError('Server already active')
rows=subprocess.check_output(['nvidia-smi','--query-gpu=index,uuid,memory.used','--format=csv,noheader,nounits'],text=True).splitlines()
uuids=[]
for row in rows:
    i,u,mem=[s.strip() for s in row.split(',')]
    if int(i)<4:
        if int(mem)>20:raise RuntimeError('Selected GPU occupied: '+row)
        uuids.append(u)
assert uuids==['GPU-REPLACE-0','GPU-REPLACE-1','GPU-REPLACE-2','GPU-REPLACE-3'], 'GPU mapping changed'
with socket.socket() as s:s.bind(('127.0.0.1',30010))
env=os.environ.copy()
env.update(CUDA_VISIBLE_DEVICES='0,1,2,3',CUDA_HOME=str(r/'runtime-venv/lib/python3.12/site-packages/nvidia/cu13'),LD_LIBRARY_PATH=str(r/'driver-libs'),HF_HOME=str(r/'cache/huggingface'),HF_ENDPOINT='https://hf-mirror.com',TMPDIR=str(r/'tmp'),APPTAINER_TMPDIR=str(r/'tmp'),APPTAINER_CACHEDIR=str(r/'cache/apptainer'),TORCHINDUCTOR_CACHE_DIR=str(r/'cache/inductor'),TRITON_CACHE_DIR=str(r/'cache/triton'),SGLANG_AUTO_NUMA_BIND='0')
env['APPTAINERENV_PREPEND_PATH']=str(r/'runtime-venv/bin')+':'+env['CUDA_HOME']+'/bin'
env['XDG_CACHE_HOME']=str(r/'cache')
env['SGLANG_CACHE_DIR']=str(r/'cache/sglang')
env['SGLANG_JIT_CACHE_DIR']=str(r/'cache/sglang/jit')
args=[str(r/'tools/apptainer-mirror/bin/apptainer'),'exec','--nv','--bind','/data','--env','LD_LIBRARY_PATH='+env['LD_LIBRARY_PATH'],str(r/'ubuntu-rootfs'),str(r/'runtime-venv/bin/sglang'),'serve','--model-path',str(r/'models/MiniMax-H3'),'--model-variant','fl2va','--num-gpus','4','--tp-size','2','--ulysses-degree','2','--encoder-parallel','auto','--performance-mode','speed','--host','127.0.0.1','--port','30010','--output-path',str(r/'outputs'),'--lora-path',str(r/'models/turbo-v4/minimax_h3_turbo_v4_step600_ema.safetensors'),'--lora-nickname','h3-turbo-v4','--lora-scale','1.0','--lora-merge-mode','dynamic']
(r/'launch-args.json').write_text(json.dumps(args,indent=2))
with (r/'logs/server.log').open('ab') as f:
    p=subprocess.Popen(args,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=f,start_new_session=True,cwd=r)
pidfile.write_text(str(p.pid));print('SERVER_STARTED',p.pid,flush=True)
