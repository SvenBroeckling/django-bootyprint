from django.test import RequestFactory, TestCase
from unittest.mock import patch

from bootyprint.views import PDFResponse, PDFTemplateResponse


class TestPDFResponse(TestCase):

    def test_pdf_response(self):
        """Test PDF response with filename"""
        content = b'PDF_CONTENT'
        response = PDFResponse(content, filename='test.pdf')

        self.assertEqual(response.content, content)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="test.pdf"')

    def test_pdf_response_without_filename(self):
        """Test PDF response without filename"""
        content = b'PDF_CONTENT'
        response = PDFResponse(content)

        self.assertEqual(response.content, content)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertNotIn('Content-Disposition', response)


class TestPDFTemplateResponse(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('bootyprint.views.generate_pdf')
    def test_pdf_template_response(self, mock_generate_pdf):
        """Test PDF template response"""
        # Setup
        mock_generate_pdf.return_value = b'PDF_CONTENT'
        request = self.factory.get('/pdf')

        # Execute
        response = PDFTemplateResponse(
            request=request,
            template='test.html',
            context={'title': 'Test'},
            filename='test.pdf'
        )
        response = response.render()

        # Assert
        self.assertEqual(response.content, b'PDF_CONTENT')
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="test.pdf"')

        # Verify generate_pdf was called with correct parameters
        mock_generate_pdf.assert_called_once()
