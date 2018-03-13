import boto3
import requests
import uuid
from app import app
from PIL import Image


class ImagesStorage():
    def __init__(self):
        self.__s3 = boto3.client('s3')

    def __get_unique_key(self):
        return "image-" + uuid.uuid4().hex

    def put_image(self, image):
        unique_key = self.__get_unique_key()
        app.logger.debug(unique_key)
        post = self.__s3.generate_presigned_post(
            Bucket='intern-olga',
            Key=unique_key
        )
        app.logger.debug("Image to save: %s", image)
        files = {"file": image}
        app.logger.debug(files)
        response = requests.post(post["url"], data=post["fields"], files=files)
        app.logger.debug("Response: %s", response)
        if response.status_code != 204:
            msg = "Image upload post request with status " + str(response.status_code)
            app.logger.error(msg)
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
        app.logger.debug("Image url: %s", url)
        return url
        #response = requests.get(url)
        #if response.status_code != 200:
        #    msg = "Image get request with status " + str(response.status_code)
        #    app.logger.error(msg)
        #    raise ValueError(msg)
        #else:
        #    return response.text
