from flask import Flask, request, jsonify
from helper import *
from service import *
import os
import boto3
import logging
import openai

s3_client = boto3.client('s3')

openai.api_key = os.getenv('API_KEY')

app = Flask(__name__)



BASE_DIRECTORY = 'uploads'

AUDIO_BASE_DIRECTORY = 'audio'


os.makedirs(BASE_DIRECTORY, exist_ok=True)
os.makedirs(AUDIO_BASE_DIRECTORY, exist_ok=True)


def process_audio(BASE_DIRECTORY:str, AUDIO_BASE_DIRECTORY:str, client:any) -> str:

    files = os.listdir(BASE_DIRECTORY)
    content = ''

    for file in files:
        file_path = f'{BASE_DIRECTORY}/{file}'
        audio_file_url = f'{AUDIO_BASE_DIRECTORY}/generate_unique_id({file}.mp3'

        file_ext = get_file_extension(file_path)
        file_content = read_txt_file_content(file_path) if file_ext == 'txt' else read_pdf_file_content(file_path)

        response = convert_text_to_speech(file_content, client)
        write_audio_to_file(response, audio_file_url)

        content +=  file_content

    return content 




@app.route('/')
def index():
    return  jsonify({'Message': 'Hello TextToAudio API'})


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file part is in the request
    if 'file' not in request.files:
        return jsonify({'message': 'no file in request'}), 400

    f = request.files['file']
    
    # Ensure a file is selected
    if f.filename == '':
        return jsonify({'message': 'No file is selected'}), 400
    
    if not is_file_extension_valid(f.filename):
        return jsonify({'message': 'Invalid file type. Only .txt files allowed.'}), 400

    # Save the file
    try:
        logging.info("Uploading Text File.....")
        f.save(os.path.join(BASE_DIRECTORY, generate_unique_id(f.filename)))
        
        logging.info("Generating audio file")
        content = process_audio(BASE_DIRECTORY, AUDIO_BASE_DIRECTORY, openai)
        return jsonify({'message': 'File uploaded successfully', 'data': f'{content}'}), 200
    
    except Exception as e:

        return jsonify({'Message':'File upload error', 'Error':  str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
