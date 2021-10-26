import boto3
import logging

class S3Helper:
    def __init__(self, bucket_name, max_keys=10):
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.max_keys = max_keys

    def list_items(self):
        try:
            response = self.client.list_objects(Bucket=self.bucket_name, MaxKeys=self.max_keys)
            return [item.get('Key') for item in response.get('Contents')]
        except Exception as e:
            logging.error("Exception while listing items in bucket %s", self.bucket_name, exc_info=True)
            raise

    def get_item(self, key):
        response = self.client.get_object(Bucket=self.bucket_name, Key=key)
        return response.get('Body').read()

    def delete_item(self, key):
        logging.debug("Deleting item: " + key)
        self.client.delete_object(Bucket=self.bucket_name,Key=key)