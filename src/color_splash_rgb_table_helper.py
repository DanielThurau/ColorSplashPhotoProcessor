import boto3

class ColorSplashRGBTableHelper:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb')
        self.table_name = table_name

    def update_rgb_values(self, image_dict):
        for key, value in image_dict.items():
            rgb_ids = set()
            try:
                rgb_ids = self.get_key(key)
            except KeyError as error:
                print(error)
                pass

            rgb_ids |= value # Set join

            self.put_key(key, rgb_ids)

    def get_key(self, key):
        response = self.client.get_item(
            Key={
                'RGB': {
                    'S': key
                }
            },
            TableName=self.table_name
        )

        if 'Item' not in response:
            raise KeyError("No such key: " + key)
        else:
            return self.deserialize_ddb_list(response['Item'])

    def put_key(self, key, value):
        response = self.client.put_item(
            TableName=self.table_name,
            Item={
                'RGB': {
                    'S': key
                },
                'ImageIds': self.serialize_ddb_list(value)
            }
        )

        return response

    def deserialize_ddb_list(self, serialized_data):
        id_set = set()
        image_ids = serialized_data['ImageIds']
        if 'L' not in image_ids:
            raise KeyError('No such list key in serialized data provided')

        for item in image_ids['L']:
            id_set.add(item['S']) 

        return id_set

    def serialize_ddb_list(self, unserialized_list_data):
        l = []
        for item in unserialized_list_data:
            l.append({'S': item})
        return {'L': l}
