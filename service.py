import logging

""" Generate public URL when audio files are uploaded to S3 Bucket

:param audio_file_path: string
:return url: string
:return: None if error 

"""
def upload_to_s3( client:object, filePath:str ) -> str :

    try:
        print("Hello")
    except Exception as e:
        logging.error(str(e))