import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException, status
import uuid
import os

from app.config import settings
from app.utils.logger import logger


class UploadService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self.bucket = settings.AWS_S3_BUCKET

    async def upload_image(self, file: UploadFile, folder: str = "products") -> str:
        if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG, WebP images are allowed"
            )
        ext = file.filename.split(".")[-1]
        key = f"{folder}/{uuid.uuid4().hex}.{ext}"
        try:
            content = await file.read()
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=content,
                ContentType=file.content_type,
                ACL="public-read",
            )
            url = f"https://{self.bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
            return url
        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File upload failed")

    async def delete_file(self, url: str) -> None:
        key = url.split(f"{self.bucket}.s3.{settings.AWS_REGION}.amazonaws.com/")[-1]
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
        except ClientError as e:
            logger.error(f"S3 delete failed: {e}")
