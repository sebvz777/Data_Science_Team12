import fitz  # PyMuPDF
import re
from model.run_request import get_best_answer

# Define common German question words
german_question_words = [
    r'\bwer\b', r'\bwas\b', r'\bwo\b', r'\bwann\b', r'\bwarum\b', r'\bwie\b',
    r'\bwessen\b', r'\bwelche\b', r'\bwem\b', r'\bwessen\b'
]

# Compile a regex pattern that matches lines starting with German question words
question_pattern = re.compile(r'^(' + '|'.join(german_question_words) + r')\b', re.IGNORECASE)


def extract_questions_from_pdf(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)

    questions = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")

        # Split the text by newlines
        lines = text.split('\n')

        # Initialize flag to indicate if the previous line was part of a question
        prev_question = False

        # Iterate through each line
        for line in lines:
            # Check if the line is not empty and doesn't contain only underscores
            if line.strip() and line.strip().replace('_', ''):
                # If the previous line was part of a question, append the current line to the previous question
                if prev_question:
                    questions[-1] = (questions[-1][0] + ' ' + line.strip(), questions[-1][1])
                else:
                    # Otherwise, consider it as a new question
                    questions.append((line.strip(), (page_num + 1, text.index(line))))
                prev_question = True
            else:
                # Reset the flag if the line is empty or contains text
                prev_question = False
    print(questions)
    return questions


def generate_answer(question):
    # Generate an answer for the given question
    return get_best_answer(question)


def find_placeholder_positions(page):
    text_instances = []
    # Example placeholder text
    placeholder = "_____"  # or other unique marker

    for block in page.get_text("dict")["blocks"]:
        for line in block["lines"]:
            for span in line["spans"]:
                if placeholder in span["text"]:
                    print(span["bbox"])
                    x0, y0 = span["bbox"][:2]  # Top-left corner of the placeholder
                    y0 = y0 + 5
                    text_instances.append((x0, y0, span["text"]))
    return text_instances


"""
# Example usage
input_pdf_path = "SECQuestionaire3.pdf"
output_pdf_path = "output.pdf"
doc = fitz.open(input_pdf_path)
placeholder_positions = []
for page_num in range(len(doc)):
    page = doc[page_num]
    placeholders = find_placeholder_positions(page)
    for pos in placeholders:
        placeholder_positions.append((page_num, pos[0], pos[1]))

questions = extract_questions_from_pdf(input_pdf_path)
questions = questions[:-1]
for i, question in enumerate(questions):
    answer = generate_answer(question[0])

    (page_num, x, y) = placeholder_positions[i]
    page = doc[page_num]
    page.insert_text((x, y), answer, fontsize=12, color=(0, 0, 0))

doc.save(output_pdf_path)
"""


def pdf_answer_questions(file_path):
    questions = extract_questions_from_pdf(doc)

    if not questions:
        print(f"No questions found in file: {file_path}.")
        return

    os.makedirs(os.path.dirname("./answered_questions.txt"), exist_ok=True)
    with open("./answered_questions.txt", 'w', encoding='utf-8') as file:

        for i, question in enumerate(questions, 1):
            answer, src = get_best_answer(question)
            file.write(f"Question {i}: {question}\n")
            file.write(f"\tAnswer: {answer}, {src}.\n\n")
