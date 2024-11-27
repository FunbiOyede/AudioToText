import logging
import os
import typing

""" Generate public URL when audio files are uploaded to S3 Bucket

:param audio_file_path: string
:return response: dict -> message, url
:return: None if error 

"""
def upload_to_s3( client:object, filePath, bucket_name, object_name=None ) -> dict[str, str] :

    if object_name is None:
        object_name = os.path.basename(filePath)

    try:
        
        response = client.upload_file(filePath,bucket_name,object_name)
        if response is None:
           return {'message': 'File Upload Successful', 'url': ''}

        return { 'message': str(response), 'url': None}

    except Exception as e:
        logging.error(str(e))