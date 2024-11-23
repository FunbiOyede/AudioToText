from dotenv import load_dotenv
import os
import uuid
from typing import Dict
import pymupdf

load_dotenv()




ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename) -> Dict[str, str]:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def generate_unique_id(file_name) -> str:
    return f"{uuid.uuid4()}_{file_name}"

def read_file_content(file):
    try:
        with open(file, 'r') as f:
            content = f.read()
            return content
    except Exception as e:
        print(f'File processing error {str(e)}')

def pdf_reader(file):
    text = ''
    try:
        doc = pymupdf.open(file)
        for page in doc:
            text = page.get_text()
        return text
    except Exception as e:
        print(f'Unable to extract text from pdf')


def convert_text_to_speech(content, file_url, client):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content
    )
    with open(file_url, 'wb') as audio_file:
        audio_file.write(response.content)


def generate_audio(BASE_DIRECTORY, AUDIO_BASE_DIRECTORY, client):
    files = os.listdir(BASE_DIRECTORY)
    content = ''

    for file in files:
        file_path = f'{BASE_DIRECTORY}/{file}'
        audio_file_url = f'{AUDIO_BASE_DIRECTORY}/generate_unique_id({file}.mp3'

        file_ext = file_extension(file_path)
        file_content = read_file_content(file_path) if file_ext == 'txt' else pdf_reader(file_path)
        convert_text_to_speech(file_content,audio_file_url, client)

        content +=  file_content

    return content 


    