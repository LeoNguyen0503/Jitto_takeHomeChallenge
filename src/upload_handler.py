import boto3
import base64
import uuid

s3 = boto3.client('s3')
ALLOWED_LABEL = ["cat", "dog"]
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
BUCKET_NAME = "pet-image-storage"

def lambda_handler(event, context):
    try:
        label = event["queryStringParameters"].get("label")
        if label not in ALLOWED_LABEL:
            return {
                "statusCode": 400,
                "body": "Invalid label. Must be 'cat' or 'dog'"
            }

        content_type = event["headers"].get("content-type") or event["headers"].get("Content-Type")
        if content_type not in ALLOWED_TYPES:
            return {
                "statusCode": 400,
                "body": "Invalid content type. Must be 'jpeg', 'png', or 'webp'"
            }

        file_data = base64.b64decode(event["body"])
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
            "body": f"Image uploaded successfully. Key: {key}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }



