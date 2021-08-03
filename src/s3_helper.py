import boto3
from botocore.retries import bucket
from botocore.vendored.six import b

class S3Helper:
    def __init__(self, bucket_name, max_keys=10):
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.max_keys = max_keys

    def list_items(self):
        response = self.client.list_objects(Bucket=self.bucket_name)
        return [item.get('Key') for item in response.get('Contents')]
        

    def get_item(self, key):
        response = self.client.get_object(Bucket=self.bucket_name, Key=key)
        return response.get('Body').read()

    def delete_item():
        pass