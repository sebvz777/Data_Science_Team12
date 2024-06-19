# Automated Questionnaire Filling

Official code and data of the paper "Utilizing Elasticsearch and Azure AI for Efficient Questionnaire Completion".

## Overview

- We propose a model to automatically fill out questionnaires using [Elasticsearch](https://www.elastic.co/de/elasticsearch) and [Azure AI](https://ai.azure.com/).
- We introduce a technique for extracting questions from differen file formats (pdf, xlsx, docx, png) as well as processing relevant data in order to automatically answer the extracted questions with link to source file.
- More detailed information of the design process can be found in the pdf tba.

## Data

We will use the files in the `test/` directory to test and present our model. The questionnaires include:

- `test/Fragebogen_zum_Beispielunternhemen_Recplast_GmbH.pdf`
- `test/Fragebogen_zum_Beispielunternhemen_Recplast_GmbH.xlsx`
- `test/Fragebogen_zum_Beispielunternhemen_Recplast_GmbH.docx`

The answer data files are:

- `test/Richtline_Lenkung_von_Dokumenten_L`
- `test/Richtline_Lenkung_von_Dokumenten_L`
- `test/Sicherheitsleitlinie_L`

For more details, see the upcoming video (available by July 12).

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
|   ├── Data for answering
|   ├── Questionnairs in pdf, docx, xlsx
|   └── answered_questions.txt
└── README.md
```
