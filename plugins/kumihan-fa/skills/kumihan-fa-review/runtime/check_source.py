#!/usr/bin/env python3
"""Read-only byte preservation and bounded HTML diagnostics. No renderer or shaper."""
import argparse
import hashlib
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
MAX_BYTES=1048576
STATUSES=('passed','failed','needs-review','not-checked','unsupported','waived','not-applicable')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def check(rule,status,evidence,scope='static-source'):
 return dict(rule_id=rule,status=status,scope=scope,evidence=evidence,host='Python standard library',remediation='Review original evidence; never auto-rewrite source.',dependencies=[],notes='No rendered or native-language claim.')
def compare(source,candidate,source_metadata=None,candidate_metadata=None):
 a=source.decode('utf-8');b=candidate.decode('utf-8')
 same=source==candidate and source_metadata==candidate_metadata
 return dict(rule_id='FA-ENC-01',status='passed' if same else 'failed',scope='exact supplied bytes and supplied metadata',evidence=dict(bytes_equal=source==candidate,metadata_equal=source_metadata==candidate_metadata),source_sha256=sha(source),candidate_sha256=sha(candidate),metadata_equal=source_metadata==candidate_metadata,derived_nfc_equal=unicodedata.normalize('NFC',a)==unicodedata.normalize('NFC',b),host='Python '+unicodedata.unidata_version,remediation='Restore original bytes and metadata or obtain explicit editing scope.',dependencies=[],notes='NFC equality is derived evidence only; source is never overwritten.')
class Parser(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.stack=[];self.nodes=[];self.text=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs);parent=self.stack[-1] if self.stack else None
  node=dict(tag=tag,attrs=attrs,lang=attrs.get('lang',parent['lang'] if parent else ''),direction=attrs.get('dir',parent['direction'] if parent else ''),isolated=tag=='bdi' or attrs.get('dir') in ('ltr','auto') or bool(parent and parent['isolated']),line=self.getpos()[0]);self.nodes.append(node)
  if tag not in ('input','img','meta','link','br','hr','source','wbr','area','base','embed','param','track','col'):self.stack.append(node)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i]['tag']==tag:del self.stack[i:];break
 def handle_data(self,data):
  if self.stack:self.text.append((self.stack[-1],data))
def check_html(source):
 raw=source.encode('utf-8')
 if len(raw)>MAX_BYTES:raise ValueError('HTML exceeds 1 MiB bounded static scope')
 p=Parser();p.feed(source);checks=[]
 root=next((n for n in p.nodes if n['tag']=='html'),None);lang=root['lang'] if root else '';primary=lang.lower().split('-')[0]
 specialized='unsupported' if primary in ('ar','ur') else ('available' if primary=='fa' else 'not-checked')
 checks.append(check('FA-BIDI-01','unsupported' if primary in ('ar','ur') else ('passed' if primary=='fa' else 'not-checked'),'Explicit lang='+repr(lang)+'; script alone never establishes language.'))
 if primary=='fa':
  checks.append(check('FA-BIDI-01','passed' if root['direction']=='rtl' else 'failed','html direction='+repr(root['direction'])))
 for n,data in p.text:
  if n['tag'] in ('script','style'):continue
  if n['lang'].lower().split('-')[0]=='fa' and re.search(r'[\u0600-\u06ff]',data):
   if n['direction'] not in ('rtl','auto'):checks.append(check('FA-BIDI-01','needs-review',f'line {n["line"]}: Persian paragraph has direction {n["direction"]!r}; confirm paragraph intent.'))
   if re.search(r'https?://|[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}',data) and not n['isolated']:checks.append(check('FA-BIDI-03','needs-review',f'line {n["line"]}: mixed-direction URL/email without local isolation; visual intent not measured.'))
 for n in p.nodes:
  style=n['attrs'].get('style','') if n['lang'].lower().split('-')[0]=='fa' else ''
  if re.search(r'letter-spacing\s*:\s*(?!0(?:px|em|rem)?\s*(?:;|$)|normal)[^;]+',style,re.I):checks.append(check('FA-TYPE-01','needs-review',f'line {n["line"]}: inline letter-spacing candidate.'))
  if re.search(r'(white-space\s*:\s*nowrap|word-break\s*:\s*break-all|overflow(?:-x|-y)?\s*:\s*hidden)',style,re.I):checks.append(check('FA-TYPE-04','needs-review',f'line {n["line"]}: inline clipping/wrapping candidate; exception may be intentional.'))
  if n['tag'] in ('input','textarea'):checks.append(check('FA-UI-04','not-checked',f'line {n["line"]}: input/copy round-trip requires interactive host test.'))
 if re.search('[\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]',source):checks.append(check('FA-BIDI-05','needs-review','Directional control codepoints present; preserve and review intent.'))
 if primary=='fa' and re.search('[\u0643\u064a\u0649]',source):checks.append(check('FA-ENC-02','needs-review','Arabic Kaf/Yeh candidate; never auto-replace protected quotations.'))
 if primary=='fa' and '\u200b' in source:checks.append(check('FA-ENC-01','needs-review','U+200B ZWSP differs from U+200C ZWNJ; inspect.'))
 if primary=='fa' and re.search('[\ufb50-\ufdff\ufe70-\ufeff]',source):checks.append(check('FA-ENC-03','needs-review','Presentation forms present; do not automatically rewrite.'))
 if '\u0640' in source:checks.append(check('FA-TYPE-05','needs-review','Tatweel present and preserved; author intent requires review.'))
 checks.append(check('FA-NUM-01','not-checked','No digits, prices, dates or identifiers converted; number/calendar/timezone contract requires explicit instruction.'))
 checks.append(check('FA-UI-03','passed','Static HTML only: inherited lang/dir, inline styles, mixed URL/email candidates. External CSS, scripts, accessibility tree, rendering, copy and semantic quality not checked.'))
 return dict(source_sha256=sha(raw),locale=lang,persian_specialized=specialized,rendered='not-checked',checks=checks)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path);parser.add_argument('--candidate',type=Path);args=parser.parse_args()
 raw=args.source.read_bytes()
 report=compare(raw,args.candidate.read_bytes()) if args.candidate else check_html(raw.decode('utf-8'))
 print(json.dumps(report,ensure_ascii=False,indent=2));return int(report.get('status')=='failed' or any(c['status']=='failed' for c in report.get('checks',[])))
if __name__=='__main__':raise SystemExit(main())
