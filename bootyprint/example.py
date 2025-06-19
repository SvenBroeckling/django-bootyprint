# This file demonstrates usage examples for the bootyprint package
from django.http import HttpResponse
from django.views.generic import View

from bootyprint.utils import generate_pdf, generate_cache_key
from bootyprint.views import PDFResponse, PDFTemplateResponse


def simple_pdf_view(request):
    """Simple view that generates a PDF and returns it as a response"""
    # Example context data
    context = {
        'title': 'Sample Document',
        'content': '<p>This is a sample PDF document generated with BootyPrint.</p>',
        'generation_date': '2025-06-19',
    }

    # Generate PDF using default template
    pdf_content = generate_pdf(context=context)

    # Return PDF as a response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sample.pdf"'
    response.content = pdf_content

    return response


def pdf_response_view(request):
    """View that uses PDFResponse for a cleaner implementation"""
    context = {
        'title': 'Sample Document',
        'content': '<p>This is a sample PDF document generated with BootyPrint.</p>',
        'generation_date': '2025-06-19',
    }

    # Generate PDF
    pdf_content = generate_pdf(context=context)

    # Return using PDFResponse
    return PDFResponse(pdf_content, filename='sample.pdf')


def pdf_template_view(request):
    """View that uses PDFTemplateResponse for the cleanest implementation"""
    context = {
        'title': 'Sample Document',
        'content': '<p>This is a sample PDF document generated with BootyPrint.</p>',
    }

    # Use PDFTemplateResponse which handles rendering and response
    return PDFTemplateResponse(
        request=request,
        template='bootyprint/default.html',  # Default template
        context=context,
        filename='sample.pdf'
    )


class PDFView(View):
    """Class-based view for PDF generation"""
    template_name = 'bootyprint/default.html'
    filename = 'document.pdf'

    def get_context_data(self):
        """Get context data for the template"""
        return {
            'title': 'Class-based View Document',
            'content': '<p>This PDF was generated from a class-based view.</p>',
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=context,
            filename=self.filename
        )
