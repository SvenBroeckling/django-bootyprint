from django.conf import settings

# Default settings for bootyprint
BOOTYPRINT_DEFAULTS = {
    'DEFAULT_TEMPLATE': 'bootyprint/default.html',
    'PDF_OPTIONS': {
        'page_size': 'A4',
        'margin_top': '0.75in',
        'margin_right': '0.75in',
        'margin_bottom': '0.75in',
        'margin_left': '0.75in',
    },
    'CACHE_ENABLED': True,
    'CACHE_TIMEOUT': 60 * 60 * 24,  # 24 hours
}


def get_setting(setting_name):
    """
    Get a setting from Django settings or use the default value.

    Usage:
        from bootyprint.settings import get_setting
        template_name = get_setting('DEFAULT_TEMPLATE')
    """
    user_settings = getattr(settings, 'BOOTYPRINT', {})

    if setting_name in user_settings:
        return user_settings[setting_name]

    if setting_name in BOOTYPRINT_DEFAULTS:
        return BOOTYPRINT_DEFAULTS[setting_name]

    return None
