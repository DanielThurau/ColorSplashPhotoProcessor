import json
import re
import requests
import os
import cv2
from dotenv import load_dotenv
from s3_helper import S3Helper
import numpy as np


def lambda_handler(event, context):

    # import cv2
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    """

    # logging.getLogger().setLevel(logging.INFO)
    load_dotenv(".env")

    stage = os.getenv('STAGE')

    s3 = S3Helper("colorsplash")
    result = s3.list_items()

    bs = s3.get_item(result[0])
    cv2.imdecode(np.asarray(bytearray(bs)), cv2.IMREAD_COLOR)


    output = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Dan rocks his socks",
        }),
    }

    return output
