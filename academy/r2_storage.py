import boto3
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class R2Storage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None):
        if expire is None:
            expire = getattr(settings, 'R2_URL_EXPIRE', 3600)
        client = boto3.client(
            's3',
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY'),
            endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL'),
            region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1'),
        )
        return client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': getattr(settings, 'AWS_STORAGE_BUCKET_NAME'),
                'Key': name,
            },
            ExpiresIn=expire,
        )
