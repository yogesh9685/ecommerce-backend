from celery import Celery
from app.config import settings
from app.services.email_service import EmailService

celery_app = Celery(
    "ecommerce",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

email_service = EmailService()


@celery_app.task(name="tasks.send_otp_email", bind=True, max_retries=3)
def send_otp_email_task(self, to_email: str, otp_code: str, purpose: str):
    try:
        email_service.send_otp_email(to_email, otp_code, purpose)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(name="tasks.send_order_confirmation", bind=True, max_retries=3)
def send_order_confirmation_task(self, to_email: str, order_number: str, total: float):
    try:
        email_service.send_order_confirmation(to_email, order_number, total)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
