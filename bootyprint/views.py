from django.http import HttpResponse
from django.utils import timezone
from django.template.response import TemplateResponse

from bootyprint.utils import generate_pdf, generate_cache_key


class PDFResponse(HttpResponse):
    """
    A HttpResponse that renders content to a PDF.
    """
    def __init__(self, content, filename=None, *args, **kwargs):
        content_type = 'application/pdf'

        if filename:
            disposition = f'attachment; filename="{filename}"'
            kwargs.setdefault('headers', {})['Content-Disposition'] = disposition

        super().__init__(content=content, content_type=content_type, *args, **kwargs)


class PDFTemplateResponse(TemplateResponse):
    """
    A TemplateResponse that renders a template to PDF.
    """
    def __init__(self, request, template, context=None, filename=None, *args, **kwargs):
        super().__init__(request, template, context, *args, **kwargs)
        self.filename = filename

        if 'generation_date' not in self.context_data:
            self.context_data['generation_date'] = timezone.now()

    @property
    def rendered_content(self):
        cache_key = generate_cache_key(self.template_name, self.context_data)
        pdf_content = generate_pdf(
            template_name=self.template_name,
            context=self.context_data,
            filename=self.filename,
            cache_key=cache_key
        )
        return pdf_content

    def render(self):
        response = HttpResponse(content_type='application/pdf')
        if self.filename:
            response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        response.content = self.rendered_content
        return response
