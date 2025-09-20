from bootyprint.settings import get_setting, BOOTYPRINT_DEFAULTS
import unittest
from unittest.mock import patch


class TestSettings(unittest.TestCase):

    def test_default_settings(self):
        """Test that default settings are returned when not overridden"""
        with patch('bootyprint.settings.settings') as mock_settings:
            # Remove BOOTYPRINT from settings
            mock_settings.BOOTYPRINT = {}

            # Test each default setting
            for key, expected in BOOTYPRINT_DEFAULTS.items():
                self.assertEqual(get_setting(key), expected)

    def test_custom_settings(self):
        """Test that custom settings override defaults"""
        custom_settings = {
            'DEFAULT_TEMPLATE': 'custom/template.html',
            'FONT_KITS_STATIC_PATH': 'font_kits',
            'PDF_OPTIONS': {
                'custom_metadata': True,
                'srgb': False,
                'optimize_images': False,
            }
        }

        with patch('bootyprint.settings.settings') as mock_settings:
            mock_settings.BOOTYPRINT = custom_settings

            # Test custom settings
            self.assertEqual(get_setting('DEFAULT_TEMPLATE'), 'custom/template.html')
            self.assertEqual(get_setting('PDF_OPTIONS'), {'custom_metadata': True, 'srgb': False, 'optimize_images': False})

            # Test fallback to defaults for settings not specified
            self.assertEqual(get_setting('CACHE_ENABLED'), BOOTYPRINT_DEFAULTS['CACHE_ENABLED'])

    def test_nonexistent_setting(self):
        """Test that None is returned for nonexistent settings"""
        with patch('bootyprint.settings.settings') as mock_settings:
            mock_settings.BOOTYPRINT = {}
            self.assertIsNone(get_setting('NONEXISTENT_SETTING'))
