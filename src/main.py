import sys
from pre_and_postprocessing.extract_docx import extract_questions_docx
from pre_and_postprocessing.extract_pdf import extract_questions_from_pdf
from pre_and_postprocessing.extract_png import get_questions_from_image
from pre_and_postprocessing.extract_xlsx import fill_out_xlsx
from model.run_request import get_best_answer

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path> [sheet_name] [question_column] [answer_column]")
        return

    file_path = sys.argv[1]

    if file_path.endswith('.pdf'):
        questions = extract_questions_from_pdf(file_path)
        answers = []
        for q in questions:
            answers.append(get_best_answer(q))

    elif file_path.endswith('.docx'):
        questions = extract_questions_docx
        answers = []
        for q in questions:
            answers.append(get_best_answer(q))

    elif file_path.endswith('.xlsx'):
        if len(sys.argv) != 5:
            print("Usage for Excel files: python script.py <file_path> <sheet_name> <question_column> <answer_column>")
            return
        sheet_name = sys.argv[2]
        question_column = sys.argv[3]
        answer_column = sys.argv[4]
        questions = fill_out_xlsx(file_path, sheet_name, question_column, answer_column)
        answers = []
        for q in questions:
            answers.append(get_best_answer(q))

    elif file_path.endswith('.png'):
        questions = get_questions_from_image(file_path)
        answers = []
        for q in questions:
            answers.append(get_best_answer(q))
    else:
        print("Unsupported file format. Supported formats are: .pdf, .docx, .xlsx, .png")

if __name__ == "__main__":
    main()