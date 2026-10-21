import hashlib,importlib.util,io,json,posixpath,re,unittest,zipfile,subprocess,sys
from urllib.parse import urlsplit
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2];P=ROOT/"plugins/kumihan-szyk"
# Installation guides come from tools/build_install_guides.py (one generator for every edition).
HOST_MARK={'chatgpt':'GPT-Codex','claude':'Claude','gemini':'Gemini'}
def install_guides(code):
 """(generator, {path: html}) for the edition's nine guides (3 hosts x native/en/ja)."""
 sys.path.insert(0,str(ROOT/'tools'))
 import build_install_guides as G
 out=G.outputs()
 return G,{G.guide_path(code,h,l):out[G.guide_path(code,h,l)] for h in G.HOSTS for l in (code,'en','ja')}
def check_guide(t,G,code,native,path,text,brand):
 """Release downloads, language attributes/switch/alternates and brand of one guide."""
 import edition_versions as V
 facts=V.load()['editions'][code];slug=V.catalogue()[code]['product']
 host,lang=next((h,l) for h in G.HOSTS for l in (code,'en','ja') if G.guide_path(code,h,l)==path)
 t.assertEqual((ROOT/path).read_text(encoding='utf-8'),text,path+' is stale')
 attr=native if lang==code else lang
 t.assertIn(f'<html lang="{attr}"'+(' dir="rtl"' if lang==code and code in G.RTL else '')+'>',text)
 t.assertIn(brand,text);t.assertIn('<main',text)
 alts=dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">',text))
 expected={(native if k==code else k):G.BASE+G.guide_path(code,host,k) for k in (code,'en','ja')}
 t.assertEqual(alts,dict(expected,**{'x-default':G.BASE+G.guide_path(code,host,code)}))
 switch=re.findall(r'<a href="([^"]+)" lang="([^"]+)" hreflang="[^"]+" data-language( aria-current="page")?>',text)
 t.assertEqual([(h,l) for h,l,_ in switch],[(G.guide_path(code,host,k).removeprefix('docs/'),native if k==code else k) for k in (code,'en','ja')])
 t.assertEqual([h for h,_,c in switch if c],[G.guide_path(code,host,lang).removeprefix('docs/')])
 # Downloads: exactly the edition's verified Release assets for this host + SHA256SUMS.
 t.assertEqual(facts['release_status'],'published')
 verified={a['url'] for a in facts['verified_assets']}
 zips=re.findall(r'<a href="([^"]+\.zip)"',text);names=[z.rsplit('/',1)[1] for z in zips]
 t.assertEqual(len(zips),5,path);t.assertEqual(len(set(zips)),5,path);t.assertLessEqual(set(zips),verified,path)
 t.assertTrue(all(z.startswith(f"{facts['release_url'].replace('/tag/','/download/')}/") for z in zips),path)
 plugins=[n for n in names if re.search(r'plugin|extension',n)];t.assertEqual(len(plugins),1,path)
 t.assertIn(HOST_MARK[host],plugins[0])
 for n in names:
  t.assertTrue((ROOT/'plugins'/slug/'downloads'/n).is_file(),n)
  for other,mark in HOST_MARK.items():
   if other!=host:t.assertNotIn(mark,n,(path,n))
 sums=next(m['url'] for m in facts['verified_metadata'] if m['name']=='SHA256SUMS.txt')
 t.assertIn(f'<a href="{sums}">SHA256SUMS.txt</a>',text)
 for v in re.findall(r'(?:href|src)="([^"]+)"',text):
  if urlsplit(v).scheme or v.startswith(('#','/')):continue
  target=posixpath.normpath(posixpath.join(posixpath.dirname(path),urlsplit(v).path))
  t.assertTrue((ROOT/target).is_file(),(path,v))
def data(path):return json.loads((P/path).read_text())
def module(path):
 spec=importlib.util.spec_from_file_location(path.stem,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class SzykV010Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.build=module(ROOT/"tools/build_szyk.py");cls.site=module(ROOT/"tools/build_szyk_site.py")
  cls.api=module(P/"runtime/checks.py")
 def test_bilingual_identity(self):
  m=data("plugin.json");self.assertEqual(m["name"],"kumihan-szyk")
  self.assertEqual(m["extensions"]["com.openai"]["interface"]["displayName"],"KUMIHAN｜Szyk")
  for path in ("plugin.json",".claude-plugin/plugin.json","gemini-extension.json"):
   j=data(path);self.assertIn(" | ",j["description"]);self.assertIn("Polish",j["description"])
  for slug in ("","-web","-documents","-review"):
   t=(P/"entrypoints"/("kumihan-szyk"+slug+".md")).read_text()
   self.assertIn(" | ",t.split("description: ",1)[1].splitlines()[0])
 def test_research_and_provenance(self):
  rs=data("rules/catalog.json");ss=data("sources/public-sources.json")["sources"];fs=data("fixtures/acceptance-ledger.json")
  self.assertEqual(len(rs),40);self.assertEqual(len(fs["fixtures"]),64);self.assertGreaterEqual(len(ss),60)
  self.assertEqual(fs["fixture_execution_summary"]["executed"],0)
  self.assertEqual({x["execution"]["status"] for x in fs["fixtures"]},{"not_run"})
  self.assertEqual({x["status"] for x in rs},{"proposed"})
  src={x["id"] for x in ss}
  self.assertTrue(all(set(x["source_refs"])<=src for x in rs))
  self.assertFalse(any("drive.google" in x["url"] for x in ss))
 def test_15_zips_manifest_and_member_completeness(self):
  o=self.build.plan_outputs();self.assertEqual(o,self.build.plan_outputs())
  fs={n.split("/downloads/")[-1]:b for n,b in o.items() if "/downloads/" in n}
  zs={n for n in fs if n.endswith(".zip")};self.assertEqual(len(zs),15)
  m=json.loads(fs["MANIFEST.json"]);self.assertEqual(m["product"],"KUMIHAN｜Szyk")
  self.assertEqual({x["file"] for x in m["archives"]},zs)
  for item in m["archives"]:
   n=item["file"];b=fs[n]
   self.assertTrue(n.startswith("kumihan-szyk") and n.endswith("-v0.1.0.zip"))
   self.assertEqual(item["sha256"],hashlib.sha256(b).hexdigest());self.assertEqual(item["bytes"],len(b))
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    members=z.namelist();count=sum(x.endswith("/SKILL.md") for x in members)
    self.assertEqual(count,1 if "-skill-v0.1.0.zip" in n else 4)
    self.assertTrue(all(not x.startswith("/") and ".." not in Path(x).parts for x in members))
    for x in members:
     if x.endswith("/SKILL.md"):
      s=z.read(x).decode()
      for link in re.findall(r"\]\(([^)]+)\)",s):self.assertIn((Path(x).parent/link).as_posix(),members)
  self.assertEqual(len(fs["SHA256SUMS.txt"].decode().splitlines()),16)
  for line in fs["SHA256SUMS.txt"].decode().splitlines():
   h,n=line.split("  ");self.assertEqual(hashlib.sha256(fs[n]).hexdigest(),h)
 def test_offline_checks_byte_preservation_and_schema(self):
  a="Łódź a Warszawa\n„Cytat” 25%".encode();r=self.api.inspect(a,locale="pl")
  self.assertEqual(r["source_preservation"]["status"],"passed")
  self.assertEqual(r["rendering"],"not-checked");self.assertEqual(r["research_fixtures_executed"],0)
  self.assertEqual(r["findings"],[]);self.assertEqual(r["original_sha256"],hashlib.sha256(a).hexdigest())
  rr=self.api.inspect(a,"pl",a+b"x");self.assertEqual(rr["source_preservation"]["status"],"failed")
  try:import jsonschema
  except ImportError:return
  for rep in (r,rr):jsonschema.validate(rep,data("schemas/report.schema.json"))
 def test_static_findings_are_narrow(self):
  x=self.api.inspect(b"<html><style>h1{word-break:break-all}</style></html>")
  self.assertEqual({x["rule_id"] for x in x["findings"]},{"PL-TYPE-08","PL-I18N-01"})
  self.assertEqual(self.api.inspect("„Nowość”".encode())["findings"],[])
  self.assertTrue(any(f["rule_id"]=="PL-TYPE-03" for f in self.api.inspect("“Nowość”".encode(),source_role="new_copy")["findings"]))
  self.assertTrue(any(f["rule_id"]=="PL-TYPE-01" for f in self.api.inspect(b"Wczoraj w\nWarszawie",source_role="observed_layout")["findings"]))
  with self.assertRaises(ValueError):self.api.inspect(b"abc",locale="es")
  with self.assertRaises(UnicodeError):self.api.inspect(b"\xff")
 def test_12_pages_and_local_link_resolution(self):
  landings=self.site.outputs();self.assertEqual(len(landings),3);G,guides=install_guides("pl")
  pages={**landings,**guides};self.assertEqual(len(pages),12);allpages={**self.site.all_outputs(),**guides};self.assertEqual(len(allpages),13)
  for path,s in pages.items():
   lang="ja" if ".ja." in path else "en" if ".en." in path else "pl"
   self.assertIn('<html lang="'+lang+'">',s)
   for k in ("pl","en","ja"):self.assertIn('hreflang="'+k+'"',s)
   self.assertIn("KUMIHAN｜Szyk",s);self.assertIn("<main",s)
   self.assertNotIn("Grafía",s);self.assertNotIn("Español",s)
   if path.startswith("docs/"):
    check_guide(self,G,"pl","pl",path,s,'KUMIHAN<span class="brand-sub">｜Szyk</span>')
    # Polish one-letter words (a, i, o, u, w, z) are bound to the next word with U+00A0.
    if not re.search(r"\.(en|ja)\.html$",path):
     visible=re.sub(r"<[^>]+>","‖",re.sub(r"<(script|style|pre|code)[\s\S]*?</\1>"," ",s))
     self.assertEqual(re.findall(r"(?<![\w/=-])[AaIiOoUuWwZz] (?=\w)",visible),[],path)
   class URIs(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
     self.urls += [v for k,v in attrs if k in ("src","href") and v]
   parser=URIs();parser.feed(s)
   for uri in parser.urls:
    if uri.startswith(("https:","http:","mailto:","#","data:")):continue
    uri=uri.split("?")[0]
    if uri.startswith("/kumihan/"):target=uri[len("/kumihan/"):].split("#")[0]
    elif uri.startswith("/"):continue
    else:target=(Path(path).parent/uri.split("#")[0]).as_posix()
    if target:self.assertTrue(target in allpages or (ROOT/target).is_file(),(path,uri,target))
 def test_regeneration_current(self):
  for script in ("tools/build_szyk.py","tools/build_szyk_site.py","tools/build_install_guides.py"):
   p=subprocess.run([sys.executable,str(ROOT/script),"--check"],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr+p.stdout)
if __name__=="__main__":unittest.main()
