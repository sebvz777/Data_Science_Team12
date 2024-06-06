import pandas as pd
import openpyxl

# Schlüsselwörter zur Identifizierung der Fragen
keywords = {"Frag", "Fragen", "Question", "Questions", "Guidelines", "Guideline"}
# Datei laden
file_path = "/Users/philipp/PycharmProjects/pythonProject/2023-07 VDMA-SCS-Lieferantenselbstauskunft-2023_FINAL (1) (1).xlsx"
df = pd.read_excel(file_path)

# Schlüsselwörter für die Identifizierung der Fragen
keywords2 = [
    "Erklären", "Beschreiben", "Formulieren", "Liefern", "Diskutieren",
    "Veranschaulichen", "Klären", "Definieren", "Umreißen", "Zusammenfassen",
    "Begründen", "Vergleichen", "Kontrastieren", "Analysieren", "Bewerten",
    "Ausarbeiten", "Identifizieren", "Erkunden", "Interpretieren", "Untersuchen"
]

keywords_responses = [
            "Antwort", "Antworten", "Lösung", "Answer", "Answers", "Solution", "Solutions", "Lösungen"
]


# Funktion zum Extrahieren der Fragen
def extract_questions_xlsx(df, keywords):
    questions = []
    for index, row in df.iterrows():
        for col in df.columns:
            for keyword in keywords:
                if keyword in col:
                    text = str(row[col])
                    if pd.notna(text) and isinstance(text, str) and text != "nan":
                        questions.append((index, col, text))
    return questions


# Funktion zur Bestimmung der Antwortspalte
def check_keywords_in_header(df, keywords):
    for idx, col in enumerate(df.columns):
        for keyword in keywords:
            if keyword in col:
                return col, idx
    return None, None


# Funktion zum Einfügen der Antworten
def insert_answers(worksheet, questions, answers, answer_column_idx):
    if len(questions) != len(answers):
        raise ValueError("Die Anzahl der Fragen und Antworten muss übereinstimmen.")

    #if answer_column_name not in df.columns:
    #   df[answer_column_name] = ""

    for (index, col, question), answer in zip(questions, answers):
        mycell = worksheet.cell(row=index + 2, column = answer_column_idx + 1)
        mycell.value = answer
       # df.at[index, answer_column_name] = answer

   # return df


def get_keywords():
    user_keywords = input("Please enter additional keywords, separated by commas: ").split(',')
    user_keywords = [keyword.strip() for keyword in user_keywords]
    return user_keywords


# Beispielnutzung
questions = extract_questions_xlsx(df, keywords)

# Beispielantworten
answers = ["Test2.0"] * len(questions)

# Bestimmen der Antwortspalte
answer_column, answer_column_idx = check_keywords_in_header(df, keywords_responses)
if not answer_column:
    answer_column = get_keywords()[0]
    answer_column_idx = len(df.columns)  # Neue Spalte wird am Ende hinzugefügt

print(answer_column_idx)
output_file_path = "/Users/philipp/PycharmProjects/pythonProject/2023-07 VDMA-SCS-Lieferantenselbstauskunft-2023_FINAL_with_answers.xlsx"

myworkbook=openpyxl.load_workbook(file_path)
worksheet = myworkbook.active


# Antworten einfügen
#df_with_answers = insert_answers(df, questions, answers, answer_column)
insert_answers(worksheet, questions, answers, answer_column_idx)

# Datei speichern
myworkbook.save(file_path)
# Datei speichern

#df_with_answers.to_excel(output_file_path, index=False)



print(f"Fragen wurden erfolgreich extrahiert und Antworten in {output_file_path} gespeichert.")

def fill_out_xlsx(file_path, worksheet, questions, answers, answer_column_idx):
    answer_column, answer_column_idx = check_keywords_in_header(df, keywords_responses)
    if not answer_column:
        answer_column = get_keywords()[0]
        answer_column_idx = len(df.columns)  # Neue Spalte wird am Ende hinzugefügt

    myworkbook=openpyxl.load_workbook(file_path)
    worksheet = myworkbook.active


    # Antworten einfügen
    #df_with_answers = insert_answers(df, questions, answers, answer_column)
    insert_answers(worksheet, questions, answers, answer_column_idx)

    # Datei speichern
    myworkbook.save(file_path)
