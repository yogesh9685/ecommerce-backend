from app.utils.logger import logger


class NotificationService:
    async def send_push(
        self, user_id: int, title: str, body: str, data: dict = None
    ) -> None:
        """Send push notification (integrate with FCM/APNs here)."""
        logger.info(f"Push notification to user {user_id}: {title} - {body}")

    async def send_sms(self, phone: str, message: str) -> None:
        """Send SMS (integrate with Twilio/MSG91 here)."""
        logger.info(f"SMS to {phone}: {message}")

    async def notify_order_placed(self, user_id: int, order_number: str) -> None:
        await self.send_push(
            user_id=user_id,
            title="Order Placed! 🎉",
            body=f"Your order #{order_number} has been placed successfully.",
        )

    async def notify_order_shipped(
        self, user_id: int, order_number: str, tracking: str
    ) -> None:
        await self.send_push(
            user_id=user_id,
            title="Order Shipped 🚚",
            body=f"Order #{order_number} is on its way! Tracking: {tracking}",
        )

    async def notify_order_delivered(self, user_id: int, order_number: str) -> None:
        await self.send_push(
            user_id=user_id,
            title="Order Delivered ✅",
            body=f"Order #{order_number} has been delivered. Enjoy your purchase!",
        )

    async def notify_payment_success(self, user_id: int, amount: float) -> None:
        await self.send_push(
            user_id=user_id,
            title="Payment Successful 💳",
            body=f"Payment of ₹{amount:.2f} was successful.",
        )
