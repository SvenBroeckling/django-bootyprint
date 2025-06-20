import tempfile
from pathlib import Path

from django.template.loader import render_to_string

try:
    from weasyprint import HTML
except ImportError:
    raise ImportError(
        "WeasyPrint is required for PDF generation. "
        "Install it with: uv add weasyprint"
    )

from django.core.cache import cache
from django.utils.encoding import force_str
import hashlib

from bootyprint.settings import get_setting


def generate_pdf(template_name=None, context=None, cache_key=None, encoding='utf-8'):
    """
    Generate a PDF from a template and context.

    Args:
        template_name: The template to use, defaults to setting DEFAULT_TEMPLATE
        context: The context to pass to the template
        cache_key: If provided and caching is enabled, will try to retrieve from cache
        encoding: The encoding to use for the rendered template

    Returns:
        BytesIO: PDF content as bytes
    """
    if context is None:
        context = {}

    if template_name is None:
        template_name = get_setting('DEFAULT_TEMPLATE')

    if cache_key and get_setting('CACHE_ENABLED'):
        cached_pdf = cache.get(cache_key)
        if cached_pdf:
            return cached_pdf

    html_string = render_to_string(template_name, context)
    pdf_options = get_setting('PDF_OPTIONS')

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
        tmp.write(html_string.encode('utf-8'))
        tmp_path = Path(tmp.name)

    html = HTML(filename=tmp_path, encoding=encoding)
    pdf_content = html.write_pdf(**pdf_options)

    tmp_path.unlink()

    if cache_key and get_setting('CACHE_ENABLED'):
        cache.set(cache_key, pdf_content, get_setting('CACHE_TIMEOUT'))

    return pdf_content


def generate_cache_key(template_name, context):
    """
    Generate a cache key for a template and context.
    """
    context_str = force_str(context)
    key = f"{template_name}:{context_str}"
    return f"bootyprint:pdf:{hashlib.md5(key.encode()).hexdigest()}"
