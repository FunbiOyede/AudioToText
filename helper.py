from dotenv import load_dotenv
import os
import openai
load_dotenv()

openai.api_key = os.getenv('API_KEY')


def read_file_content(file):
    with open(file, 'r') as f:
        content = f.read()
        return content
    


def convert_text_to_speech(content, file_url):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content
    )
    with open(file_url, 'wb') as audio_file:
        audio_file.write(response.content)



    