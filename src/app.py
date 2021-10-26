import json
import os
import cv2
import logging
from dotenv import load_dotenv
from s3_helper import S3Helper
from colorsplash_common.rgb import RGBTableHelper
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

def get_env_context():
    env_context = {}
    load_dotenv('.env')

    env_context['STAGE'] = os.environ.get('STAGE', 'development')
    env_context['DEGREE_OF_ROUNDING'] = os.environ.get('DEGREE_OF_ROUNDING', 0)
    env_context['NUMBER_OF_COLORS'] = os.environ.get('NUMBER_OF_COLORS', 3)
    env_context['LOGGING_LEVEL'] = os.environ.get('LOGGING_LEVEL', 'INFO')

    return env_context

def rgb_to_hex(color):
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
   rgb_colors = [ordered_colors[i] for i in counts.keys()]
   
   return rgb_colors

def round_rgb_list(rgb_list, degree_of_rounding):
    for i in range(len(rgb_list)):
        rgb_list[i] = round(rgb_list[i], degree_of_rounding)
    return rgb_list

def handle(env_context):
    degree_of_rounding = env_context.get("DEGREE_OF_ROUNDING")
    number_of_colors = env_context.get("NUMBER_OF_COLORS")

    s3 = S3Helper("colorsplash", max_keys=20)
    ddb = RGBTableHelper()

    image_ids = s3.list_items()
    logging.debug('ImageIds to be processed: %s', str(image_ids))
    image_dict = {}

    for image_id in image_ids:
        image_byte_stream = s3.get_item(image_id)
        logging.info("Processing file: " + image_id)

        imde_image = cv2.imdecode(np.asarray(bytearray(image_byte_stream)), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(imde_image, cv2.COLOR_BGR2RGB)
    
        colors = get_colors(image, number_of_colors)

        for color in colors:
            color_list = round_rgb_list(color.tolist(), degree_of_rounding)
            color_tuple = str(color_list)

            if color_tuple not in image_dict:
                image_dict[color_tuple] = set()
            image_dict[color_tuple].add(os.path.splitext(image_id)[0])# Adds just the id not the file extension
    
    logging.info("Processed iamge structure: %s", str(image_dict))

    ddb.update_rgb_values(image_dict)

    for image_id in image_ids:
        s3.delete_item(image_id)


def lambda_handler(event, context):

    env_context = get_env_context()
    logger = logging.getLogger()
    logger.setLevel(env_context['LOGGING_LEVEL'])
    status_code = 200

    try:
        handle(env_context)
    except Exception as e:
        logging.error("Error when processing images", exc_info=True)
        status_code = 500

    output = {
        "statusCode": status_code,
    }

    return output
