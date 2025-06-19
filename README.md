# Django BootyPrint

A Django app for rendering PDF documents with WeasyPrint.

## Installation

```bash
pip install django-bootyprint
# or with uv
uv add django-bootyprint
```

## Requirements

- Python 3.13+
- Django 5.1.7+
- WeasyPrint 65.0+

## Quick Start

1. Add `'bootyprint'` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    ...
    'bootyprint',
    ...
]
```

2. Customize settings in your settings.py (optional):

```python
BOOTYPRINT = {
    'DEFAULT_TEMPLATE': 'myapp/my_template.html',  # Override default template
    'PDF_OPTIONS': {
        'page_size': 'Letter',  # Change from default A4
        'margin_top': '1in',    # Custom margins
        'margin_right': '1in',
        'margin_bottom': '1in',
        'margin_left': '1in',
    },
    'CACHE_ENABLED': True,      # Enable caching (default: True)
    'CACHE_TIMEOUT': 3600,      # Cache timeout in seconds (default: 86400 - 24 hours)
}
```

## Usage

### Basic Usage

```python
from bootyprint.utils import generate_pdf
from django.http import HttpResponse

def my_pdf_view(request):
    # Generate PDF from template
    context = {'title': 'My Document', 'content': 'Hello World'}
    pdf_content = generate_pdf(
        template_name='myapp/my_template.html',
        context=context
    )

    # Return as response
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="my_document.pdf"'
    return response
```

### Using PDFResponse

```python
from bootyprint.views import PDFResponse
from bootyprint.utils import generate_pdf

def my_pdf_view(request):
    context = {'title': 'My Document', 'content': 'Hello World'}
    pdf_content = generate_pdf(
        template_name='myapp/my_template.html',
        context=context
    )

    return PDFResponse(pdf_content, filename='my_document.pdf')
```

### Using PDFTemplateResponse

```python
from bootyprint.views import PDFTemplateResponse

def my_pdf_view(request):
    context = {'title': 'My Document', 'content': 'Hello World'}

    return PDFTemplateResponse(
        request=request,
        template='myapp/my_template.html',
        context=context,
        filename='my_document.pdf'
    )
```

## Templates

Bootyprint comes with a default template (`bootyprint/default.html`) that you can extend or override. Your templates should be valid HTML that WeasyPrint can render to PDF.

Example template:

```html
{% extends "bootyprint/default.html" %}

{% block content %}
<h1>{{ title }}</h1>
<p>{{ content }}</p>

<table>
    <thead>
        <tr>
            <th>Item</th>
            <th>Price</th>
        </tr>
    </thead>
    <tbody>
        {% for item in items %}
        <tr>
            <td>{{ item.name }}</td>
            <td>${{ item.price }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}

{% block footer %}
    Generated on {{ generation_date|date:"F j, Y" }}
{% endblock %}
```

## License

MIT
