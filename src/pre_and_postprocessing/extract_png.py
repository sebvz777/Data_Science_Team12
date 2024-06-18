import cv2
import pytesseract
from pytesseract import Output
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Function to preprocess the image
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return binary_image


# Function to extract text with positions using Tesseract
def extract_text_positions(image):
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config)
    return data


# Function to estimate the average font size
def estimate_average_font_size(data):
    heights = [data['height'][i] for i in range(len(data['level'])) if int(data['conf'][i]) > 0]
    if heights:
        return sum(heights) / len(heights)
    else:
        return 0


# Function to group text into paragraphs based on spatial separation and identify questions
def identify_paragraphs(data, line_spacing_multiplier=2):
    average_font_size = estimate_average_font_size(data)
    line_spacing_threshold = line_spacing_multiplier * average_font_size

    paragraphs = []
    current_paragraph = ""
    paragraph_position = None
    n_boxes = len(data['level'])

    for i in range(n_boxes):
        text = data['text'][i].strip()
        if text:
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])

            if current_paragraph == "":
                current_paragraph = text
                paragraph_position = (x, y, w, h)
            else:
                # Check if the current text is spatially separated from the last line in the current paragraph
                if abs(y - paragraph_position[1] - paragraph_position[3]) <= line_spacing_threshold:
                    current_paragraph += " " + text
                    paragraph_position = (
                        min(paragraph_position[0], x),
                        min(paragraph_position[1], y),
                        max(paragraph_position[0] + paragraph_position[2], x + w) - min(paragraph_position[0], x),
                        max(paragraph_position[1] + paragraph_position[3], y + h) - min(paragraph_position[1], y)
                    )
                else:
                    if '?' in current_paragraph:
                        paragraphs.append((current_paragraph.strip(), paragraph_position))
                    current_paragraph = text
                    paragraph_position = (x, y, w, h)

            if i == n_boxes - 1 and '?' in current_paragraph:
                paragraphs.append((current_paragraph.strip(), paragraph_position))

    return paragraphs


# Main function to process the image and extract questions
def get_questions_from_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    data = extract_text_positions(preprocessed_image)
    questions = identify_paragraphs(data)
    return questions


# Example usage
image_path = 'questionnaire2.png'
questions = get_questions_from_image(image_path)

for question in questions:
    print(f"Question: {question[0]}, Position: {question[1]}")

# If needed, display the image with question boxes
import matplotlib.pyplot as plt


def display_questions(image_path, questions):
    image = cv2.imread(image_path)
    for question in questions:
        _, (x, y, w, h) = question
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


display_questions(image_path, questions)


def png_answer_questions(file_path):

    """
    questions = extract_questions_from_docx(file_path)

    if not questions:
        print(f"No questions found in file: {file_path}.")
        return

    os.makedirs(os.path.dirname("./answered_questions.txt"), exist_ok=True)
    with open("./answered_questions.txt", 'w', encoding='utf-8') as file:

        for i, question in enumerate(questions, 1):
            answer, src = get_best_answer(question)
            file.write(f"Question {i}: {question}\n")
            file.write(f"\tAnswer: {answer}, {src}.\n\n")
    """
