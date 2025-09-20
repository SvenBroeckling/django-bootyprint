from django.contrib.staticfiles import finders
from django.template import Library
from django.utils.safestring import mark_safe

from bootyprint.utils import get_accumulated_fonts_css

register = Library()

@register.simple_tag
def bootyprint_css():
    with open(finders.find('bootyprint/bootyprint.min.css')) as f:
        return mark_safe(f"<style>{f.read()}</style>")

@register.simple_tag
def local_static(path):
    """
    A template tag to return the local path to a static file,
    with behavior similar to Django's built-in {% static %} tag.
    """
    file_path = finders.find(path)
    if file_path:
        return file_path
    else:
        raise ValueError(f"Static file '{path}' could not be found.")

@register.simple_tag
def font_kits():
    """
    This Tag returns the accumulated font kits css from the configured font kit path.
    Settings:
      BOOTYPRINT_FONT_KITS_STATIC_PATH: the static path to the font kits
          (default: 'font_kits')
    """
    return get_accumulated_fonts_css()
