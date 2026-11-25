import pathlib,json,hashlib,time
r=pathlib.Path('/data/users/example/h3-turbo4')
manifest=json.loads((r/'models/official-fl2va-manifest.json').read_text())
out=r/'models/base-verification.json'
done={}
for attempt in range(180):
    pending=[]
    for f in manifest['files']:
        name=f['path']
        if name in done: continue
        p=r/'models/MiniMax-H3'/name
        if not p.is_file() or p.stat().st_size!=f['size']:
            pending.append(name);continue
        actual=hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
        ok=f['sha256'] is None or actual==f['sha256']
        done[name]={'bytes':p.stat().st_size,'sha256':actual,'expected_sha256':f['sha256'],'ok':ok}
        print(name,ok,flush=True)
        if not ok:
            out.write_text(json.dumps({'success':False,'mismatch':name,'checked':done},indent=2));raise RuntimeError(name)
    state={'success':not pending,'revision':manifest['revision'],'checked':done,'pending':pending}
    out.write_text(json.dumps(state,indent=2))
    if not pending:
        print('VERIFICATION_COMPLETE',len(done),flush=True);break
    time.sleep(60)
else:raise TimeoutError('Base files incomplete after 3 hours')
