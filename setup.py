from setuptools import setup, find_packages

setup(
    name="pdf_image_processor",
    version="0.1.0",
    description="Document Authentication Pipeline",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "google-cloud-documentai>=2.10.0",
        "google-cloud-storage>=2.0.0",
        "click>=8.0.0",
        "PyPDF2>=3.0.0",
        "Pillow>=9.0.0",
        "pytesseract>=0.3.10",
        "python-dotenv>=0.21.0",
        "requests>=2.28.0",
        "pytest>=7.0.0",  # include pytest for testing
    ],
    entry_points={
        "console_scripts": [
            "docauth=cli:cli",
        ],
    },
)