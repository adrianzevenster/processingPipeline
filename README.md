# PDF-Image-Processor

[![CI](https://github.com/your-org/pdf-image-processor/actions/workflows/run_pipeline.yml/badge.svg)](https://github.com/your-org/pdf-image-processor/actions)

A Python-based document authentication pipeline for ingesting PDF and image files, extracting entities via Google Cloud Document AI or Gemini, and validating against custom patterns.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Automation](#automation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Ingest PDF and image files from local directories
- OCR text extraction with fallback if Tesseract is not installed
- Entity extraction via GCP Document AI or Gemini API
- Custom validation for dates and amounts using regex patterns
- Command-line interface for local execution
- Automated workflows via Cron, Docker Compose, or GitHub Actions

## Prerequisites

- Python 3.10 or newer
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (optional, for OCR)
- Google Cloud SDK for Application Default Credentials or service-account JSON
- Access to a Google Cloud project with Document AI permissions

## Installation

```bash
git clone https://github.com/your-org/pdf-image-processor.git
cd pdf-image-processor
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
cp .env.example .env  # fill in your credentials
```

## Usage

```bash
docauth run --input-dir data/input --output-dir data/output
```

Processed results will be saved as JSON files in `data/output`.

## Testing

Run the full suite of unit and integration tests:

```bash
pytest
```

## Automation

- **Cron**: Add to your crontab:
  ```cron
  0 * * * * cd /path/to/pdf-image-processor && docauth run --input-dir data/input --output-dir data/output
  ```

- **Docker Compose**: Build and run:
  ```bash
docker-compose up --build
  ```

- **GitHub Actions**: The workflow is defined in `.github/workflows/run_pipeline.yml`.

## Project Structure

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```markdown
# Document Authentication Pipeline

## Setup

1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd PDF-Image-Processor
   ```
2. Create a virtual env and activate:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies and package:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -e .
   ```
4. Verify with pytest:
   ```bash
   python -m pytest
   ```

## Usage

```bash
docauth run --input-dir data/input --output-dir data/output
```

## Automation

- **Cron**: `crontab -e` → `0 * * * * cd /path && docauth run`
- **Docker Compose**: `docker-compose up --build`
- **GitHub Actions**: `.github/workflows/run_pipeline.yml`