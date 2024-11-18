from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return jsonify({'message': 'File uploaded successfully'})


@app.route('/document', methods=['GET'])
def get_file():

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'message': f'The first file in the folders is - {files[0]}'}), 200





if __name__ == "__main__":
    app.run(debug=True)
