from flask import Flask, request, jsonify
import os
from helper import *

app = Flask(__name__)

# Configure upload folder
BASE_DIRECTORY = 'uploads'


os.makedirs(BASE_DIRECTORY, exist_ok=True)
app.config['UPLOAD_FOLDER'] = BASE_DIRECTORY

@app.route('/')
def index():
    return  jsonify({'Message': 'Hello TextToAudio'})

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file part is in the request
    if 'file' not in request.files:
        return jsonify({'message': 'no file in request'}), 200

    f = request.files['file']
    
    # Ensure a file is selected
    if f.filename == '':
        return jsonify({'message': 'No file is selected'})
    
    # Save the file
    f.save(os.path.join(BASE_DIRECTORY, f.filename))
    return jsonify({'message': 'File uploaded successfully'})


@app.route('/content', methods=['GET'])
def get_file():

    files = os.listdir(app.config['UPLOAD_FOLDER'])

    for file in files:
        file_path = f'{BASE_DIRECTORY}/{file}'
        content = read_file_content(file_path)
        print(content)

    return jsonify({'message': f'The content of the file is  - {content}'}), 200




if __name__ == "__main__":
    app.run(debug=True)
