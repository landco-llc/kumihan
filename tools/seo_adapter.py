"""Apply the shared contract at generator output boundaries, before drift checks."""
from functools import wraps
from seo_metadata import enrich_html


def seo_outputs(builder):
    @wraps(builder)
    def outputs(*args, **kwargs):
        return {path: enrich_html(content, path) if path.endswith('.html') else content
                for path, content in builder(*args, **kwargs).items()}
    return outputs
