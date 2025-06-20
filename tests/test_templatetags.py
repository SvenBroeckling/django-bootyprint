import unittest

from bootyprint.templatetags.bootyprint import bootyprint_css, local_static


class TestTemplateTags(unittest.TestCase):

    def test_bootyprint_css_tag(self):
        css = bootyprint_css()
        self.assertIn('.border-3', css)
        self.assertIn('.card-inlay', css)

    def test_local_static_tag(self):
        path = local_static('bootyprint/bootyprint.min.css')
        self.assertIn('bootyprint/bootyprint.min.css', path)

