import hashlib,json,subprocess,urllib.request,concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE='https://landco-llc.github.io/kumihan/';TAG='kumihan-de-v0.1.0'
release=json.loads(subprocess.check_output(['gh','api','repos/landco-llc/kumihan/releases/tags/'+TAG]))
assert not release['draft'];local=ROOT/'plugins/kumihan-satzbild/downloads';expected={p.name:p for p in local.iterdir() if p.is_file()};assert len(expected)==17
assert set(expected)=={a['name'] for a in release['assets']}
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'KUMIHAN-Satzbild-public-verification'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.status,r.read(),r.geturl()
def asset(a):
 p=expected[a['name']];b=p.read_bytes();sha=hashlib.sha256(b).hexdigest();assert a['size']==len(b);assert a['digest']=='sha256:'+sha
 status,download,url=get(a['browser_download_url']);assert status==200;assert download==b
 return dict(name=a['name'],url=a['browser_download_url'],bytes=len(download),sha256=sha,status='passed')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:assets=list(pool.map(asset,release['assets']))
paths=['kumihan-de'+s+'.html' for s in ('','.en','.ja')]+['docs/install-satzbild-'+h+s+'.html' for h in ('chatgpt','claude','gemini') for s in ('','.en','.ja')]
def page(path):
 status,b,url=get(BASE+path);text=b.decode('utf-8');assert status==200 and 'KUMIHAN' in text and 'Satzbild' in text
 # Static pages must match the committed source byte-for-byte (no Jekyll frontmatter here).
 assert b==(ROOT/path).read_bytes(),path+' differs from current committed page'
 return dict(path=path,url=url,http=status,sha256=hashlib.sha256(b).hexdigest(),status='passed')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:pages=list(pool.map(page,paths))
status,b,url=get(BASE);assert status==200 and 'kumihan-de.ja.html' in b.decode()
result=dict(tag=TAG,release=release['html_url'],draft=release['draft'],asset_count=len(assets),assets=assets,pages=pages,gateway=dict(url=url,http=status,de_link='kumihan-de.ja.html',status='passed'),local_sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
(Path('/tmp/kumihan-de-public-verification.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PUBLIC VERIFIED: 17 assets exact bytes/digests + 12 Pages exact bytes + DE gateway')
