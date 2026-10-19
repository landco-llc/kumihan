"""Apply the shared contract at generator output boundaries, before drift checks."""
from functools import wraps
from seo_metadata import enrich_html


def seo_outputs(builder):
    @wraps(builder)
    def outputs(*args, **kwargs):
        def finalize(path, content):
            if not path.endswith('.html'):
                return content
            if path.startswith('docs/install-ziheng') or path.startswith('docs/install-kumihan-bn-') or path.startswith('kumihan-bn'):
                from web_fonts import format_static
                return format_static(content, path)
            return enrich_html(content, path)
        return {path: finalize(path, content) for path, content in builder(*args, **kwargs).items()}
    return outputs
