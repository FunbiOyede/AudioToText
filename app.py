from flask import Flask, request, jsonify
from helper import *


app = Flask(__name__)



BASE_DIRECTORY = 'uploads'

AUDIO_BASE_DIRECTORY = 'audio'


os.makedirs(BASE_DIRECTORY, exist_ok=True)
os.makedirs(AUDIO_BASE_DIRECTORY, exist_ok=True)



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
        return jsonify({'message': 'No file is selected'})
    
    # Save the file
    f.save(os.path.join(BASE_DIRECTORY, f.filename))
    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route('/content', methods=['GET'])
def get_file():

    files = os.listdir(BASE_DIRECTORY)
    content = ''

    for file in files:
        file_path = f'{BASE_DIRECTORY}/{file}'
        audio_file_url = f'{AUDIO_BASE_DIRECTORY}/{file}.mp3'

        file_content = read_file_content(file_path)
        convert_text_to_speech(file_content,audio_file_url)

        content +=  file_content
    
    return jsonify({'message': f'The content of the file is  - {content}'}), 200


if __name__ == "__main__":
    app.run(debug=True)
