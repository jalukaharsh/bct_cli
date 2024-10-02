"""Module for base64 function for BCT CLI"""

from PyInquirer import prompt
import base64


def base64_encoder(): 
    questions = [
        {
            'type': 'list',
            'name': 'encode_decode',
            'choices': ['Encode', 'Decode'],
            'message': 'Would you like to encode or decode?',
        },
        {
            'type': 'input',
            'name': 'path',
            'message': 'Please input the file path of the private key',
        }
    ]   

    answers = prompt(questions)
    path = answers['path']
    encode = answers['encode_decode']

    extracted_text = extract_text(path)

    if encode == 'E':
        b = base64.b64encode(bytes(extracted_text, 'utf-8'))  # bytes
        base64_str = b.decode('utf-8')  # convert bytes to string
        print(base64_str)
    else:
        b = base64.b64decode(extracted_text)
        plaintext = b.decode('utf-8')  # convert bytes to string
        print(plaintext)


def extract_text(filepath: str) -> str:
    with open(filepath, 'r') as f:
        my_txt = f.read()

    return my_txt


if __name__ == '__main__': 
    base64_encoder()
