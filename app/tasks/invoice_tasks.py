from celery import Celery
from app.config import settings

celery_app = Celery(
    "ecommerce",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


@celery_app.task(name="tasks.generate_invoice", bind=True, max_retries=3)
def generate_invoice_task(self, order_id: int):
    """Generate PDF invoice for an order and upload to S3."""
    try:
        # TODO: Use reportlab or weasyprint to generate PDF
        from app.utils.logger import logger
        logger.info(f"Generating invoice for order {order_id}")
    except Exception as exc:
        raise self.retry(exc=exc, countdown=120)
