import json
import os
import cv2
from dotenv import load_dotenv
from s3_helper import S3Helper
from color_splash_rgb_table_helper import ColorSplashRGBTableHelper
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_colors(image, number_of_colors):
    
   modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
   modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
   
   clf = KMeans(n_clusters = number_of_colors)
   labels = clf.fit_predict(modified_image)
   
   counts = Counter(labels)
   # sort to ensure correct color percentage
   counts = dict(sorted(counts.items()))
   
   center_colors = clf.cluster_centers_
   # We get ordered colors by iterating through the keys
   ordered_colors = [center_colors[i] for i in counts.keys()]
   hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
   rgb_colors = [ordered_colors[i] for i in counts.keys()]
   
   return rgb_colors

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
    degree_of_rounding = 0
    number_of_colors = 3


    s3 = S3Helper("colorsplash")
    ddb = ColorSplashRGBTableHelper("ColorSplashRGB")
    results = s3.list_items()
    print(results)
    image_dict = {}

    for result in results:
        image_byte_stream = s3.get_item(result)
        print("Processing file: " + result)

        image = cv2.imdecode(np.asarray(bytearray(image_byte_stream)), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    
        colors = get_colors(image, number_of_colors)

        for color in colors:
            color_list = color.tolist()
            for i in range(len(color_list)):
                color_list[i] = round(color_list[i], degree_of_rounding)
            color_tuple = str(color_list)

            if color_tuple not in image_dict:
                image_dict[color_tuple] = set()
            image_dict[color_tuple].add(os.path.splitext(result)[0])# Adds just the id not the file extension
    
    print(image_dict)

    
    ddb.update_rgb_values(image_dict)

    for result in results:
        s3.delete_item(result)

    output = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Dan rocks his socks",
        }),
    }

    return output
