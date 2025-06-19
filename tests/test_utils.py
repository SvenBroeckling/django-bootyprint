import unittest
from unittest.mock import patch, MagicMock

from bootyprint.utils import generate_cache_key


class TestUtils(unittest.TestCase):

    def test_generate_cache_key(self):
        """Test that generate_cache_key generates consistent keys"""
        template = 'bootyprint/template.html'
        context = {'title': 'Test Document', 'content': 'Hello World'}

        # Generate key twice with same inputs
        key1 = generate_cache_key(template, context)
        key2 = generate_cache_key(template, context)

        # Keys should be identical
        self.assertEqual(key1, key2)

        # Keys should be prefixed
        self.assertTrue(key1.startswith('bootyprint:pdf:'))

        # Different context should generate different key
        different_context = {'title': 'Different Document', 'content': 'Hello World'}
        different_key = generate_cache_key(template, different_context)
        self.assertNotEqual(key1, different_key)

    @patch('bootyprint.utils.render_to_string')
    @patch('bootyprint.utils.HTML')
    @patch('bootyprint.utils.cache')
    @patch('bootyprint.utils.get_setting')
    def test_generate_pdf_with_cache(self, mock_get_setting, mock_cache, mock_html, mock_render):
        """Test PDF generation with caching"""
        from bootyprint.utils import generate_pdf

        # Setup mocks
        mock_get_setting.side_effect = lambda key: {
            'DEFAULT_TEMPLATE': 'bootyprint/default.html',
            'PDF_OPTIONS': {'page_size': 'A4'},
            'CACHE_ENABLED': True,
            'CACHE_TIMEOUT': 86400
        }.get(key)

        mock_cache.get.return_value = None

        # Return a string from render_to_string that can be encoded
        mock_render.return_value = "<html><body>Test</body></html>"

        mock_pdf = b'PDF_CONTENT'
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = mock_pdf
        mock_html.return_value = mock_html_instance

        # Call function
        result = generate_pdf(
            template_name='test.html',
            context={'title': 'Test'},
            cache_key='test-key'
        )

        # Assertions
        mock_cache.get.assert_called_with('test-key')
        mock_render.assert_called_once()
        mock_html.assert_called_once()
        mock_html_instance.write_pdf.assert_called_with(page_size='A4')
        mock_cache.set.assert_called_with('test-key', mock_pdf, 86400)
        self.assertEqual(result, mock_pdf)
