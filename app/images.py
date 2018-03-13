import uuid

import boto3
import requests


class ImagesStorage():
    def __init__(self):
        self.__s3 = boto3.client('s3')

    def __get_unique_key(self):
        return "image-" + uuid.uuid4().hex

    def put_image(self, image):
        unique_key = self.__get_unique_key()
        post = self.__s3.generate_presigned_post(
            Bucket='intern-olga',
            Key=unique_key
        )
        files = {"file": image}
        response = requests.post(post["url"], data=post["fields"], files=files)
        if response.status_code != 204:
            msg = "Image post request with status " + str(response.status_code)
            raise ValueError(msg)
        else:
            return unique_key

    def get_image(self, key):
        url = self.__s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'intern-olga',
                'Key': key
            }
        )
        return url
