import boto3
import base64
import uuid
import json

s3 = boto3.client('s3')
ALLOWED_LABEL = ["cat", "dog"]
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
BUCKET_NAME = "pet-image-storage"

def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])

        label = data.get("label")
        content_type = data.get("content_type")
        image_base64 = data.get("image_data")

        if content_type not in ALLOWED_TYPES:
            return {
                "statusCode": 400,
                "body": "Invalid content type. Must be 'jpeg', 'png', or 'webp'"
            }

        if label not in ALLOWED_LABEL:
            return {
                "statusCode": 400,
                "body": json.dump({"Invalid label. Must be 'cat' or 'dog'"})
            }

        if not image_base64:
            return {
                "statusCode": 400,
                "body": json.dump({"Missing image data type in body"})
            }

        try:
            file_data = base64.b64decode(image_base64)
        except Exception:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid base64 image data"})
            }

        file_ext = content_type.split("/")[-1]
        image_id = str(uuid.uuid4())
        key = f"{label}/{image_id}.{file_ext}"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=file_data,
            ContentType=content_type
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Image uploaded successfully", "key": key})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }



