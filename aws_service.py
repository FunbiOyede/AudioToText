import logging
import os
import typing
from botocore.exceptions import ClientError
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
           url = create_presigned_url(client,bucket_name,object_name)
           
           return {'message': 'File Upload Successful', 'url': f'{url}'}

        return { 'message': str(response), 'url': None}

    except ClientError as e:
        logging.error(str(e))


def create_presigned_url(client, bucket_name, object_name, expiration=3600):
    try:

        response = client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
        return response
    except ClientError as e:
        logging.error(str(e))
