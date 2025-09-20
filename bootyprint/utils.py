import glob
import hashlib
import os
import re
import tempfile
from pathlib import Path

from django.contrib.staticfiles import finders
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from weasyprint import HTML

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


def get_font_dirs():
    """
    Return a list of font directories, which must be subdirectories of the static
    font kits path.
    """
    static_fonts = finders.find(get_setting('FONT_KITS_STATIC_PATH') or 'font_kits')
    if static_fonts:
        return [
            d for d in glob.glob(os.path.join(static_fonts, "*")) if os.path.isdir(d)
        ]
    return []


def get_font_choices():
    """
    Return a list of font choices, suitable for use in a Django model field.
    """
    font_choices = set()
    for font_dir in get_font_dirs():
        css_path = os.path.join(font_dir, "stylesheet.css")
        if os.path.exists(css_path):
            with open(css_path) as f:
                content = f.read()
                font_families = re.findall(r"font-family:\s*'([^']+)'", content)
                for family in font_families:
                    font_choices.add((family, family))
    return sorted(list(font_choices))


def load_stylesheet(font_path):
    """
    Open the stylesheet.css file in the given font directory and replace relative URLs
    with absolute URLs.
    """
    css_path = os.path.join(font_path, "stylesheet.css")
    if not os.path.exists(css_path):
        return ""

    with open(css_path) as f:
        content = f.read()

    def replace_url(match):
        url = match.group(1).strip("'\"")
        if url.startswith(("http://", "https://", "/")):
            return f"url({url})"
        return f"url({os.path.join(os.path.dirname(css_path), url)})"

    return re.sub(r"url\((.*?)\)", replace_url, content)


def get_accumulated_fonts_css():
    """
    Combine all stylesheet.css files from all font directories into one CSS file.
    """
    return mark_safe(
        "\n".join(load_stylesheet(font_dir) for font_dir in get_font_dirs())
    )
