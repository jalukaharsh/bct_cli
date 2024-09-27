"""Module for base64 function for BCT CLI"""

from PyInquirer import prompt
import base64


def base64_encoder(): 
    questions = [
        {
            'type': 'input',
            'name': 'path',
            'message': 'Please input the file path of private key',
        }
    ]   

    answers = prompt(questions)
    path = answers['path']

    extracted_text = extract_text(path)
    print(extracted_text)

    b = base64.b64encode(bytes(extracted_text, 'utf-8')) # bytes
    base64_str = b.decode('utf-8') # convert bytes to string

    print(base64_str)

def extract_text(filepath: str) -> str: 
    with open(filepath, 'r') as file: 
        my_txt = file.read()

    return my_txt


if __name__ == '__main__': 
    base64_encoder()