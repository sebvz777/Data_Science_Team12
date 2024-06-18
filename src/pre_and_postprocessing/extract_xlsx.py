import os

import pandas as pd
import openpyxl

from src.model.run_request import get_best_answer


# Funktion zum Extrahieren der Fragen
def extract_questions_xlsx(df, question_column):
    questions = []
    for index, row in df.iterrows():
        for col in df.columns:
            if question_column in col:
                text = str(row[col])
                if pd.notna(text) and isinstance(text, str) and text != "nan":
                    questions.append((index, col, text))
    return questions


def xlsx_answer_questions(file_path, sheet_name, question_column):
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    questions = extract_questions_xlsx(df, question_column)

    if not questions:
        print(f"No questions found in file: {file_path}.")
        return

    os.makedirs(os.path.dirname("./answered_questions.txt"), exist_ok=True)
    with open("./answered_questions.txt", 'w', encoding='utf-8') as file:

        for i, question in enumerate(questions, 1):
            answer, src = get_best_answer(question)
            file.write(f"Question {i}: {question}\n")
            file.write(f"\tAnswer: {answer}, {src}.\n\n")


# print(f"Fragen wurden erfolgreich extrahiert und Antworten in {output_txt_path} gespeichert.")
