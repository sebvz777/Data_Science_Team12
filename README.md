# Automated Questionnaire Filling

Official code and data of the paper "tba".

## Overview

- We propose a model to automatically fill out questionnaires using [Elasticsearch](https://www.elastic.co/de/elasticsearch) and [Azure AI](https://ai.azure.com/).
- We introduce a technique for extracting questions from differen file formats (pdf, xlsx, docx, png) as well as processing relevant data in order to automatically answer the extracted questions with link to source file.
- More detailed information of the design process can be found in the pdf tba.

## Data

Using the files tba and tba we aim to test and present our model (see Video tba).
Coming Soon (at latest 21.06.)

## Installation

### Requirements

```plaintext
azure_storage==0.37.0
docx==0.2.4
elasticsearch==8.14.0
fitz==0.0.1.dev2
matplotlib==3.8.2
opencv_python==4.9.0.80
openpyxl==3.1.3
pandas==2.2.2
pytesseract==0.3.10
```

## Folder Structure
```plaintext
/project_root
├── src/
│   ├── pre- and postprocessing/
|   |   ├── extract_docx.py
|   |   ├── extract_xlsx.py
|   |   ├── extract_pdf.py
|   |   └── extract_png.py
│   └── model/
|       ├── Elasticsearch Database
|       └── Azure AI Model
├── tests/
|   └── tba
└── README.md
```
