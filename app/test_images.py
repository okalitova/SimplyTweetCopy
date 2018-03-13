import boto3
import requests

# Get the service client
s3 = boto3.client('s3')

# Generate the POST attributes
post = s3.generate_presigned_post(
    Bucket='intern-olga',
    Key='image-1'
)

# Use the returned values to POST an object. Note that you need to use ALL
# of the returned fields in your post. You can use any method you like to
# send the POST, but we will use requests here to keep things simple.
files = {"file": "file_content"}
response = requests.post(post["url"], data=post["fields"], files=files)
print(response)
