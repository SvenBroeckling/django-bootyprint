from django.contrib.staticfiles import finders
from django.template import Library
from django.utils.safestring import mark_safe

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

