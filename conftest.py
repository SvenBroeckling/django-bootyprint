import os
import django
from django.conf import settings


def pytest_configure():
    """Configure Django settings for pytest."""
    settings.configure(
        DEBUG=False,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'bootyprint',
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        },
        ROOT_URLCONF='bootyprint.urls',
        SECRET_KEY='test-secret-key',
        BOOTYPRINT={
            'DEFAULT_TEMPLATE': 'bootyprint/default.html',
            'PDF_OPTIONS': {
                'media_type': 'print',
                'pdf_identifier': None,
                'pdf_variant': None,
                'pdf_version': None,
                'pdf_forms': False,
                'uncompressed_pdf': False,
                'custom_metadata': False,
                'srgb': True,
                'optimize_images': True,
                'jpeg_quality': 95,
                'presentational_hints': False,
                'dpi': 96,
                'full_fonts': True,
                'hinting': True,
            },
            'CACHE_ENABLED': True,
            'CACHE_TIMEOUT': 60 * 60 * 24,  # 24 hours
        }
    )

    django.setup()
