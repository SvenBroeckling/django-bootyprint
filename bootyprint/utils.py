import tempfile
from pathlib import Path

from django.template.loader import render_to_string
from django.core.cache import cache
from django.utils.encoding import force_str
import hashlib

from bootyprint.settings import get_setting


def generate_pdf(template_name=None, context=None, filename=None, cache_key=None):
    """
    Generate a PDF from a template and context.

    Args:
        template_name: The template to use, defaults to setting DEFAULT_TEMPLATE
        context: The context to pass to the template
        filename: The filename to use when saving
        cache_key: If provided and caching is enabled, will try to retrieve from cache

    Returns:
        BytesIO: PDF content as bytes
    """
    try:
        from weasyprint import HTML
    except ImportError:
        raise ImportError(
            "WeasyPrint is required for PDF generation. "
            "Install it with: uv add weasyprint"
        )

    if context is None:
        context = {}

    if template_name is None:
        template_name = get_setting('DEFAULT_TEMPLATE')

    # Cache handling
    if cache_key and get_setting('CACHE_ENABLED'):
        cached_pdf = cache.get(cache_key)
        if cached_pdf:
            return cached_pdf

    # Render the HTML template
    html_string = render_to_string(template_name, context)

    # Get PDF options from settings
    pdf_options = get_setting('PDF_OPTIONS')

    # Generate PDF
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
        tmp.write(html_string.encode('utf-8'))
        tmp_path = Path(tmp.name)

    # Use the file path to create the PDF (helps with relative resources)
    html = HTML(filename=tmp_path)
    pdf_content = html.write_pdf(**pdf_options)

    # Clean up temp file
    tmp_path.unlink()

    # Cache the generated PDF
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
