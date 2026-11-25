import pathlib,subprocess
r=pathlib.Path('/data/users/example/h3-turbo4/ubuntu-rootfs')
for p in sorted((r/'var/cache/apt/archives').glob('*.deb')):
 names=subprocess.check_output(['ar','t',str(p)],text=True).splitlines();name=next(x for x in names if x.startswith('data.tar'))
 a=subprocess.Popen(['ar','p',str(p),name],stdout=subprocess.PIPE)
 subprocess.run(['tar',('--use-compress-program=zstd' if name.endswith('.zst') else '-J' if name.endswith('.xz') else '-z'),'--keep-directory-symlink','--no-same-owner','-xf','-','-C',str(r)],stdin=a.stdout,check=True);a.stdout.close();assert a.wait()==0
print('EXTRACT_COMPLETE',flush=True)
