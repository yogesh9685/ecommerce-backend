import json
import asyncio
from aiokafka import AIOKafkaConsumer
from app.config import settings
from app.utils.logger import logger
from app.events.topics import ORDER_EVENTS, PAYMENT_EVENTS, NOTIFICATION_EVENTS


async def process_message(topic: str, message: dict) -> None:
    logger.info(f"Processing message from '{topic}': {message}")
    if topic == ORDER_EVENTS:
        event_type = message.get("event_type")
        if event_type == "order_placed":
            logger.info(f"Order placed: {message}")
    elif topic == PAYMENT_EVENTS:
        logger.info(f"Payment event: {message}")
    elif topic == NOTIFICATION_EVENTS:
        logger.info(f"Notification event: {message}")


async def start_consumer():
    consumer = AIOKafkaConsumer(
        ORDER_EVENTS,
        PAYMENT_EVENTS,
        NOTIFICATION_EVENTS,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="ecommerce-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )
    await consumer.start()
    logger.info("Kafka consumer started")
    try:
        async for msg in consumer:
            await process_message(msg.topic, msg.value)
    except Exception as e:
        logger.error(f"Consumer error: {e}")
    finally:
        await consumer.stop()
