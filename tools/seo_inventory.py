"""Public HTML discovery and parsed head contract, shared by audit and sitemap."""
import json
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from seo_metadata import CONFIG, canonical_url

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path, html):
        super().__init__(convert_charrefs=True)
        self.path, self.html = path, html
        self.meta = defaultdict(list)
        self.canonicals, self.alternates, self.titles, self.graphs = [], [], [], []
        self.lang, self.direction = '', ''
        self._head, self._title, self._json = False, False, False
        self._text = ''
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang, self.direction = a.get('lang', ''), a.get('dir', '')
        if tag == 'head': self._head = True
        if not self._head: return
        if tag == 'title': self._title, self._text = True, ''
        if tag == 'meta':
            self.meta[(a.get('name') or a.get('property') or '').lower()].append(a.get('content', ''))
        if tag == 'link':
            rel=a.get('rel', '').lower().split()
            if 'canonical' in rel: self.canonicals.append(a.get('href', ''))
            if 'alternate' in rel and 'hreflang' in a: self.alternates.append((a['hreflang'],a.get('href', '')))
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self._json, self._text = True, ''

    def handle_data(self, data):
        if self._title or self._json: self._text += data

    def handle_endtag(self, tag):
        if tag == 'title' and self._title:
            self.titles.append(self._text); self._title = False
        if tag == 'script' and self._json:
            try: self.graphs.append(json.loads(self._text))
            except json.JSONDecodeError: self.graphs.append(None)
            self._json = False
        if tag == 'head': self._head = False

    @property
    def canonical(self):
        return self.canonicals[0] if len(self.canonicals)==1 else ''

    @property
    def noindex(self):
        return any('noindex' in value.lower().replace(',', ' ').split() or 'none' in value.lower().replace(',', ' ').split()
                   for key in ('robots', 'googlebot') for value in self.meta[key])

    @property
    def external(self):
        return bool(self.canonical and not self.canonical.startswith(CONFIG['site_url']))


def public_paths(root):
    root = Path(root)
    # Source/package directories are deliberately outside the indexable site.
    # Other new public directories are included automatically.
    excluded={'tools','scripts','tests','templates','plugins','skills','vendor','node_modules'}
    return sorted(p for p in root.rglob('*.html')
                  if not (p.parent == root and p.name == 'google767fc14b71f44ff9.html')
                  if not any(part.startswith(('.', '_')) for part in p.relative_to(root).parts)
                  and p.relative_to(root).parts[0] not in excluded
                  and not p.relative_to(root).parts[0].startswith('downloads ')
                  and not p.relative_to(root).as_posix().startswith(('docs/specs/','docs/seo/')))


def pages(root=ROOT):
    root=Path(root)
    result=[]
    for path in public_paths(root):
        relative=path.relative_to(root).as_posix()
        html=path.read_text(encoding='utf-8')
        if html.startswith('---'):
            include=root/'_includes/seo-pages'/relative
            if not include.exists():
                raise ValueError(f'{relative}: missing generated Jekyll contract; run tools/build_seo.py')
            head=include.read_text(encoding='utf-8')
            # Generated includes are the source-mode contract, NOT rendered Jekyll evidence.
            # Source-mode simulation of share.html; built HTML is audited separately.
            import re
            from site_share import tags, description
            captures = dict(re.findall(r'{% capture (\w+) %}(.*?){% endcapture %}', head, re.S))
            head = re.sub(r'{% capture \w+ %}.*?{% endcapture %}', '', head, flags=re.S)
            metadata=Page(relative,'<head>'+head+'</head>')
            language=''
            for graph in metadata.graphs:
                if isinstance(graph,dict):
                    language=next((n.get('inLanguage','') for n in graph.get('@graph',[]) if n.get('@type')=='WebPage'),'')
            if captures:
                head += tags(language, captures['seo_share_title'], description(language, captures['seo_share_description']), captures['seo_canonical'])
            direction=' dir="rtl"'  if language.split('-')[0]=='ar' else ''
            html=f'<html lang="{language}"{direction}><head>{head}</head></html>'
        result.append(Page(relative,html))
    return result


def local_path(url):
    if not url.startswith(CONFIG['site_url']): return None
    parsed=urlparse(url)
    if parsed.query or parsed.fragment or parsed.scheme!='https': return None
    relative=unquote(url[len(CONFIG['site_url']):])
    if '..' in Path(relative).parts or relative.startswith('/'): return None
    return relative or 'index.html'


def indexable(pages):
    result=[]
    seen=set()
    paths={p.path for p in pages}
    for page in pages:
        if page.noindex or page.external: continue
        canonical=page.canonical
        if not canonical: raise ValueError(f'{page.path}: exactly one canonical is required')
        if canonical!=canonical_url(page.path):
            raise ValueError(f'{page.path}: canonical must match actual public path: {canonical}')
        if local_path(canonical) not in paths: raise ValueError(f'{page.path}: nonexistent canonical {canonical}')
        if canonical in seen: raise ValueError(f'{page.path}: duplicate canonical {canonical}')
        seen.add(canonical); result.append(page)
    return result
