"""Shared edition version presentation at generator boundaries, plus Jekyll fragments.

This module owns only version/download metadata. It does not translate or rewrite
editorial copy, SEO metadata, logos, fonts, footer or historical release notes.
"""
from functools import wraps, lru_cache
import hashlib
import json
import zipfile
from html import escape, unescape
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit, quote
import edition_versions as v

ROOT = v.ROOT
VERSION = re.compile(r'v?\d+\.\d+\.\d+(?:-preview)?')


def x(value): return escape(str(value), quote=True)


def edition_for(path):
    name = Path(path).name
    if name in ('kumihan.html', 'en.html', 'zh-tw.html') or re.fullmatch(r'install-(?:chatgpt|claude|gemini)(?:\.zh-tw)?\.html', name): return 'ja'
    for code, spec in v.catalogue().items():
        if code == 'ja': continue
        lp = {'zh-hans':'zh-cn', 'zh-hant':'zh-han'}.get(code, code)
        if re.fullmatch(r'kumihan-'+lp+r'(?:[.-](?:en|ja))?\.html', name): return code
        slug = spec['product'].removeprefix('kumihan-')
        if name.startswith(tuple('install-'+s for s in (slug+'-', slug+'.', 'kumihan-'+slug+'-', code+'-'))): return code
    return None


def words(lang):
    if lang.startswith('ja'):
        return dict(current='現行公開版', source='ソース', published='正式公開', unpublished='Release未公開', unavailable='正式公開ZIPはダウンロードできません', date='公開日時', release='Release履歴', downloads='検証済みZIP', unverified='未検証')
    if lang.startswith('zh-Hant'):
        return dict(current='目前公開版本', source='原始碼', published='正式公開', unpublished='Release 尚未公開', unavailable='尚無正式公開 ZIP 可供下載', date='公開時間', release='Release 紀錄', downloads='已驗證 ZIP', unverified='尚未驗證')
    if lang.startswith('zh-Hans'):
        return dict(current='当前公开版本', source='源码', published='正式公开', unpublished='Release 尚未公开', unavailable='暂无正式公开 ZIP 可下载', date='公开时间', release='Release 记录', downloads='已验证 ZIP', unverified='未验证')
    # New metadata uses explicitly marked English on other page locales. Existing
    # editorial translations remain verbatim; native metadata translation is pending.
    return dict(current='Current Version', source='Source', published='Published', unpublished='Release unpublished', unavailable='Published ZIP downloads unavailable', date='Published at', release='Release history', downloads='Verified ZIP downloads', unverified='Not verified')


def panel(f, lang, slot='current'):
    w = words(lang)
    status = f['release_status']
    attrs = f'class="edition-version" lang="{x(lang if lang.startswith(("ja", "zh-Hant", "zh-Hans")) else "en")}" data-edition-version="{slot}" data-release-status="{status}" dir="ltr"'
    current = f.get('published_version') or f['source_version']
    label = w['current'] if status == 'published' else w['source']
    number = f'<bdi dir="ltr">v{x(current)}</bdi>'
    if status == 'published': number = f'<a href="{x(f["release_url"])}">{number}</a>'
    text = f'<strong>{x(label)} {number}</strong>'
    if status == 'published':
        if slot != 'hero':
            text += f'<span>{x(w["published"])} · {x(w["date"])} <time datetime="{x(f["published_at"])}"><bdi dir="ltr">{x(f["published_at"])}</bdi></time></span>'
        if f['source_version'] != current: text += f'<span>{x(w["source"])} v{x(f["source_version"])}</span>'
    else:
        label = w['unpublished'] if status == 'unpublished' else w['unverified']
        text += f'<span>{x(label)} — {x(w["unavailable"])}</span>'
    return f'<!-- edition-version:{slot} --><div {attrs}>{text}</div><!-- /edition-version:{slot} -->'


def consumer_archives(code, version):
    """Offline consumer packages (plugins/<product>/downloads/manifest.json): every ZIP must
    match the manifest's size and SHA-256 and pass a CRC check, or generation stops."""
    if code not in v.catalogue(): return frozenset()
    folder = ROOT / 'plugins' / v.catalogue()[code]['product'] / 'downloads'
    manifest = folder / 'manifest.json'
    if not manifest.exists(): return frozenset()
    data = json.loads(manifest.read_bytes())
    if data['version'].removeprefix('v') != version:
        raise ValueError('Consumer package manifest version mismatch: '+code)
    admitted = set()
    for row in data['packages']:
        path = folder / row['file']
        if not path.resolve().is_relative_to(folder.resolve()):
            raise ValueError('Package path escapes distribution')
        content = path.read_bytes()
        if len(content) != row['bytes'] or hashlib.sha256(content).hexdigest() != row['sha256']:
            raise ValueError('Package checksum mismatch: '+str(path))
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None: raise ValueError('Package CRC mismatch: '+str(path))
        admitted.add(path.relative_to(ROOT).as_posix())
    return frozenset(admitted)


def role(name): return VERSION.sub('@VERSION@', unquote(Path(urlsplit(unescape(name)).path).name))


@lru_cache(maxsize=64)
def source_archives(code, version):
    """Admit existing source ZIPs by full path, never by ambiguous basename.

    This is an offline source-distribution contract, independent of Releases.
    A missing/corrupt manifest or ZIP aborts generation rather than hiding links.
    """
    if code not in ('zh-hans', 'zh-hant'): return consumer_archives(code, version)
    product = v.catalogue()[code]['product']
    base = ROOT / 'plugins' / product
    manifests = sorted(base.glob('downloads*/MANIFEST.json'))
    if not manifests: raise ValueError('Missing source ZIP manifests: '+code)
    admitted = set()
    for manifest in manifests:
        data = json.loads(manifest.read_bytes())
        if data['version'].removeprefix('v') != version:
            # ZiLu and ZiHeng each retain exact, checksummed historical source manifests.
            # Retain pre-update URLs independently of active source candidates.
            from ziheng_retention import VERSIONS
            if code == 'zh-hans' and version == '0.1.0':
                historical = manifest.parent/'history/0.1.0/MANIFEST.json'
                raw = historical.read_bytes()
                if hashlib.sha256(raw).hexdigest() != '4ce535b78bd601cb706ffcf8e1a7568293d1569f6f6c809fa32553127e471f9f':
                    raise ValueError('Historical ZiLu manifest mismatch')
                data = json.loads(raw)
            elif code != 'zh-hant' or version not in VERSIONS:
                raise ValueError('Source ZIP manifest version mismatch: '+code)
            if code == 'zh-hant':
                from ziheng_retention import retained_outputs
                retained = retained_outputs(ROOT, (manifest.parent.name,))
                history = manifest.parent / 'history' / version / 'MANIFEST.json'
                if history.relative_to(ROOT).as_posix() not in retained:
                    raise ValueError('Historical source manifest not retained')
                data = json.loads(history.read_bytes())
                if data['version'].removeprefix('v') != version:
                    raise ValueError('Historical source version mismatch')
                for row in data['archives']:
                    rel = (manifest.parent / row['file']).relative_to(ROOT).as_posix()
                    if rel not in retained:
                        raise ValueError('Historical archive not retained: ' + rel)
        for row in data['archives']:
            path = manifest.parent / row['file']
            if not path.resolve().is_relative_to(manifest.parent.resolve()):
                raise ValueError('Source ZIP path escapes distribution')
            content = path.read_bytes()
            if len(content) != row['bytes'] or hashlib.sha256(content).hexdigest() != row['sha256']:
                raise ValueError('Source ZIP checksum mismatch: '+str(path))
            with zipfile.ZipFile(path) as archive:
                if archive.testzip() is not None: raise ValueError('Source ZIP CRC mismatch: '+str(path))
            admitted.add(path.relative_to(ROOT).as_posix())
    return frozenset(admitted)


def is_source_download(url, f):
    parsed = urlsplit(url)
    path = unquote(parsed.path)
    if parsed.query or parsed.fragment: return False
    if parsed.netloc:
        if parsed.scheme != 'https' or parsed.netloc != 'raw.githubusercontent.com': return False
        prefix = '/landco-llc/kumihan/main/'
        if not path.startswith(prefix): return False
        path = path.removeprefix(prefix)
    else:
        if parsed.scheme: return False
        path = path.removeprefix('../').removeprefix('/kumihan/').lstrip('/')
    if f['release_status'] == 'unpublished' and path in source_archives(f.get('edition'), f['source_version']): return True
    if f['release_status'] == 'unpublished' and f.get('edition') == 'zh-hans' and path in source_archives('zh-hans','0.1.0'): return True
    if f.get('edition') == 'zh-hant':
        from ziheng_retention import retained_outputs
        # Exact path/digest retention only; no basename or arbitrary old version.
        retained = retained_outputs(ROOT, ('downloads', 'downloads Claude', 'downloads Gemini'))
        return path.endswith('.zip') and path in retained
    return False


def rewrite_downloads(text, f):
    assets = {role(a['name']):a for a in f['verified_assets']}
    def anchor(m):
        attrs, url, rest, label = m.groups()
        decoded = unescape(url)
        liquid = re.fullmatch(r"{{\s*'([^']+)'\s*\|\s*relative_url\s*}}", decoded)
        if liquid: decoded = liquid[1]
        basename = Path(urlsplit(decoded).path).name
        metadata = {a['name']:a for a in f.get('verified_metadata',[])}
        if basename in metadata:
            return f'<a{attrs}href="{x(metadata[basename]["url"])}"{rest}>{label}</a>'
        if basename == 'SHA256SUMS.txt' and f.get('source_commit') and 'downloads' in unquote(decoded):
            path = unquote(urlsplit(decoded).path).removeprefix('../').lstrip('/')
            if path.startswith('downloads '):
                target = 'https://raw.githubusercontent.com/landco-llc/kumihan/'+f['source_commit']+'/'+quote(path)
                return f'<a{attrs}href="{x(target)}"{rest}>{label}</a>'
        prefix = re.escape(v.REPO+'/releases/tag/'+f.get('tag_prefix', 'v'))
        if decoded == v.REPO+'/releases/latest' or re.fullmatch(prefix+r'\d+\.\d+\.\d+', decoded):
            if f['release_status'] != 'published':
                return f'<span class="download-unavailable" aria-disabled="true">{label} (Release unavailable)</span>'
            return f'<a{attrs}href="{x(f["release_url"])}"{rest}>{VERSION.sub("v"+f["published_version"],label)}</a>'
        if not urlsplit(decoded).path.lower().endswith('.zip'): return m[0]
        if is_source_download(decoded, f):
            marker = '<span lang="en"> (Source ZIP)</span>'
            if marker not in label: label += marker
            return f'<a{attrs}href="{url}"{rest}>{label}</a>'
        a = assets.get(role(decoded))
        if not a: return f'<span class="download-unavailable" data-source-zip="{x(Path(urlsplit(decoded).path).name)}" aria-disabled="true">{label} (ZIP unavailable)</span>'
        label = VERSION.sub('v'+f['published_version'], label)
        return f'<a{attrs}href="{x(a["url"])}"{rest}>{label}</a>'
    text = re.sub(r'<a\b([^>]*?)href="([^"]+)"([^>]*)>(.*?)</a>', anchor, text, flags=re.S)
    # Concrete URLs/file names inside copyable commands must track the admitted asset.
    def pre(m):
        content = m[0]
        if '.zip' not in content: return content
        if f['release_status'] != 'published':
            return '<p class="download-unavailable" lang="en">Published ZIP commands unavailable; use the source instructions.</p>'
        def url(m):
            a = assets.get(role(m[0]))
            if not a: raise ValueError('Unverified ZIP in command: '+m[0])
            return x(a['url'])
        content = re.sub(r'https?://[^\s<>"\x27]+\.zip', url, content)
        for a in assets.values():
            # Replace only names sharing an admitted role; generic unzip local paths stay intact.
            pattern = re.escape(a['name'])
            pattern = re.sub(r'\d+\\\.\d+\\\.\d+', r'\\d+\\.\\d+\\.\\d+(?:-preview)?', pattern)
            content = re.sub(pattern, lambda _: a['name'], content)
        return content
    return re.sub(r'<pre\b.*?</pre>', pre, text, flags=re.S)


COMING = {'ja': '配布準備中', 'zh-Hant': '準備中', 'zh-Hans': '准备中'}


def gateway_badge(code, lang):
    facts = v.load()['editions']
    if code not in facts:
        # An edition with pages but no package or Release yet (tools/build_upcoming_sites.py).
        status = next((s for k, s in COMING.items() if lang.startswith(k)), 'Coming soon')
        return f'<span class="state" aria-label="{x(status)}"><span class="version-state" lang="{x(lang if lang.startswith(("ja","zh")) else "en")}">{x(status)}</span></span>'
    f = facts[code]
    number = f.get('published_version') or f['source_version']
    w = words(lang)
    status = w['published'] if f['release_status']=='published' else w['unpublished']
    label = f'v{number} · {status}'
    return f'<span class="state" aria-label="{x(label)}"><bdi dir="ltr">v{x(number)}</bdi><span class="version-state" lang="{x(lang if lang.startswith(("ja","zh")) else "en")}">{x(status)}</span></span>'


def apply_html(text, path, facts=None):
    code = edition_for(path)
    if code is None: return text
    f = (facts or v.load())['editions'][code]
    lang = re.search(r'<html\b[^>]*\blang="([^"]+)"', text)[1]
    # Own blocks are replaceable, so static-source maintenance remains idempotent.
    text = re.sub(r'<!-- edition-version:([\w-]+) -->.*?<!-- /edition-version:\1 -->', '', text, flags=re.S)
    text = re.sub(r'<link rel="stylesheet" href="[^"]*assets/version-info.css">', '', text)
    text = rewrite_downloads(text, f)
    root = '../' if path.startswith('docs/') else ''
    text = re.sub(r'<head>\s*', lambda _: f'<head><link rel="stylesheet" href="{root}assets/version-info.css">\n', text, count=1)
    install = path.startswith('docs/')
    if install:
        text, count = re.subn(r'(<aside\b[^>]*>)', lambda m:m[0]+panel(f,lang), text, count=1)
        if count != 1: raise ValueError('Missing install sidebar: '+path)
    else:
        # Every edition landing has a hero. Place version immediately before its title.
        text, count = re.subn(r'(<h1\b)', lambda m:panel(f,lang,'hero')+m[0], text, count=1)
        if count != 1: raise ValueError('Missing landing hero: '+path)
        # Versions in the old hero foot/status heading are metadata, not historical prose.
        text = re.sub(r'(<(?:div|p)[^>]*class="(?:hero-foot|status-title)"[^>]*>)(.*?)(</(?:div|p)>)',
                      lambda m:m[1]+VERSION.sub('v'+(f.get('published_version') or f['source_version']),m[2])+m[3],text,flags=re.S)
    # Put metadata in the existing installation area; never in footer/top gateway hero.
    if not install:
        text, count = re.subn(r'(<section\b[^>]*\bid="install"[^>]*>)', lambda m:m[0]+panel(f,lang,'install'),text,count=1)
        if count != 1: raise ValueError('Missing landing install section: '+path)
    return text


def version_outputs(builder):
    @wraps(builder)
    def outputs(*args, **kwargs):
        return {path:apply_html(content,path) if path.endswith('.html') else content
                for path, content in builder(*args, **kwargs).items()}
    return outputs


if __name__ == '__main__':
    print(apply_html(sys.stdin.read(),sys.argv[1]),end='')
