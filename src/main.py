import sys
from pre_and_postprocessing.extract_docx import docx_answer_questions
from pre_and_postprocessing.extract_pdf import pdf_answer_questions
from pre_and_postprocessing.extract_png import png_answer_questions
from pre_and_postprocessing.extract_xlsx import xlsx_answer_questions
from model.run_request import get_best_answer


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path> [sheet_name] [question_column] [answer_column]")
        return

    file_path = sys.argv[1]

    if file_path.endswith('.pdf'):
        pdf_answer_questions(file_path)

    elif file_path.endswith('.docx'):
        docx_answer_questions(file_path)

    elif file_path.endswith('.xlsx'):
        if len(sys.argv) != 5:
            print("Usage for Excel files: python script.py <file_path> <sheet_name> <question_column> <answer_column>")
            return
        sheet_name = sys.argv[2]
        question_column = sys.argv[3]
        answer_column = sys.argv[4]
        xlsx_answer_questions(file_path, sheet_name, question_column)


    elif file_path.endswith('.png'):
        png_answer_questions(file_path)

    else:
        print("Unsupported file format. Supported formats are: .pdf, .docx, .xlsx, .png")


if __name__ == "__main__":
    main()
