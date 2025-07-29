import base64

import boto3
import random
import mimetypes

s3 = boto3.client('s3')
ALLOWED_LABEL = ["cat", "dog"]
BUCKET_NAME = "pet-image-storage"

def random_handler(event, context):
    try:
        label = event["queryStringParameters"].get("label")
        if label not in ALLOWED_LABEL:
            return {
                "statusCode": 400,
                "body": "Invalid label. Must be 'cat' or 'dog'"
            }

        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{label}/")
        objects = response.get("Contents")
        if not objects:
            return{
                "statusCode": 404,
                "body": "No images found for this label"
            }

        chosen = random.choice(objects)["Key"]
        image_obj = s3.get_object(Bucket=BUCKET_NAME, Key=chosen)
        image_bytes = image_obj["Body"].read()
        content_type = image_obj.get("ContentType") or mimetypes.guess_type(chosen)[0]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": content_type
            },
            "body": base64.b64encode(image_bytes).decode("utf-8"),
            "isBase64Encoded": True
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
