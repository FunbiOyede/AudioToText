from dotenv import load_dotenv
import uuid
import pymupdf
import logging
import requests

load_dotenv()




ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def is_file_extension_valid(filename:str) -> bool:
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename:str) -> str:

    return filename.rsplit('.', 1)[1].lower()

def generate_unique_id(file_name:str) -> str:

    return f"{uuid.uuid4()}_{file_name}"


def read_txt_file_content(file_path:str) -> str:

    try:
        with open(file_path, 'r') as f:
            content = f.read()
            return content
        
    except Exception as e:
        logging.info(f'Unable to extract text from txt {str(e)}')


def read_pdf_file_content(file_path:str) -> str:

    text = ''
    try:
        doc = pymupdf.open(file_path)
        for page in doc:
            text = page.get_text()
        return text
    
    except Exception as e:
        logging.info(f'Unable to extract text from pdf- {e}')


def convert_text_to_speech(content:str, client:any):

    try:
        response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content
        )
        return response.content
    
    except requests.exceptions.HTTPError as e:
        logging.info(f"HTTP error: {e}")


def write_audio_to_file(data:any, file_url:str):
    
    try:

        with open(file_url, 'wb') as audio_file:
            audio_file.write(data)

    except Exception as e:
        logging.info(f'Unable to write audio to file{e}')

