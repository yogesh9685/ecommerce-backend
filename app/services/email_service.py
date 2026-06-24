import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import settings
from app.utils.logger import logger


class EmailService:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAIL_FROM

    def _send(self, to_email: str, subject: str, html_body: str) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.from_email, to_email, msg.as_string())
        except Exception as e:
            logger.error(f"Email sending failed to {to_email}: {e}")

    def send_otp_email(self, to_email: str, otp_code: str, purpose: str) -> None:
        subject = f"Your OTP for {purpose.replace('_', ' ').title()}"
        body = f"""
        <h2>Your OTP Code</h2>
        <p>Use the following code for <strong>{purpose.replace('_', ' ')}</strong>:</p>
        <h1 style="letter-spacing:6px; color:#4f46e5;">{otp_code}</h1>
        <p>This code expires in 10 minutes. Do not share it with anyone.</p>
        """
        self._send(to_email, subject, body)

    def send_order_confirmation(self, to_email: str, order_number: str, total: float) -> None:
        subject = f"Order Confirmed - #{order_number}"
        body = f"""
        <h2>Thank you for your order!</h2>
        <p>Order Number: <strong>{order_number}</strong></p>
        <p>Total: <strong>₹{total:.2f}</strong></p>
        <p>We'll notify you when your order is shipped.</p>
        """
        self._send(to_email, subject, body)
