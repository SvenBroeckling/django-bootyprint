# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Released]

### [0.0.5] - 2025-09-20

#### Changed
- Changed the python requirement to 3.11+ to allow for the latest PyPy version
- Added initial utility functions for "font kits"

### [0.0.4] - 2025-06-27

#### Changed
- Updated bootyprint to v0.0.11
- Removed unnecessary WeasyPrint import check from `utils.py`

### [0.0.3] - 2025-06-25

#### Changed
- Updated bootyprint to v0.0.10

### [0.0.2]

#### Added
- Template tag: `bootyprint_css`
- Template tag: `local_static`
- Added encoding argument to `generate_pdf()`

#### Changed
- Changed the PDF_OPTIONS to be WeasyPrint `write_pdf()` options.
- Removed `filename` argument from `generate_pdf()` function.

### [0.0.1]

#### Added
- Initial release of django-bootyprint
- PDF generation utilities with WeasyPrint integration
- Configurable settings with reasonable defaults
- Caching support for generated PDFs
- Default template with basic styling
- Helper views for PDF responses
- Example implementation
- Comprehensive documentation

#### Changed
