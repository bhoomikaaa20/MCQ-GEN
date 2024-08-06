import os
from PyPDF2 import PdfReader
import json
import traceback

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    elif file.name.endswith('.txt'):
        try:
            return file.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
    else:
        raise Exception("Unsupported file format. Only PDF and TXT are supported.")

def get_table_data(quiz_str):
    try:
        # Convert the quiz from str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # Iterate over quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "N/A")
            options = "||".join([
                f"{option}->{option_value}" for option, option_value in value.get("options", {}).items()
            ])
            correct = value.get("correct", "N/A")
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    except json.JSONDecodeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise Exception(f"Error parsing JSON: {str(e)}")
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise Exception(f"Error processing quiz data: {str(e)}")
