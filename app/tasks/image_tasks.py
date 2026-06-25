from celery import Celery
from app.config import settings

celery_app = Celery(
    "ecommerce",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


@celery_app.task(name="tasks.resize_image", bind=True, max_retries=3)
def resize_image_task(self, image_url: str, sizes: list[tuple] = None):
    """Resize uploaded image to multiple resolutions."""
    try:
        from app.utils.logger import logger

        sizes = sizes or [(800, 800), (400, 400), (100, 100)]
        logger.info(f"Resizing image {image_url} to sizes {sizes}")
        # TODO: Use Pillow to resize and re-upload to S3
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
