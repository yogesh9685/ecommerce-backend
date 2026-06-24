import json
from aiokafka import AIOKafkaProducer
from app.config import settings
from app.utils.logger import logger

_producer = None


async def get_producer() -> AIOKafkaProducer:
    global _producer
    if _producer is None:
        _producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await _producer.start()
    return _producer


async def publish_event(topic: str, event: dict, key: str = None) -> None:
    try:
        producer = await get_producer()
        key_bytes = key.encode("utf-8") if key else None
        await producer.send_and_wait(topic, event, key=key_bytes)
        logger.info(f"Published event to topic '{topic}': {event}")
    except Exception as e:
        logger.error(f"Failed to publish event to '{topic}': {e}")


async def stop_producer() -> None:
    global _producer
    if _producer:
        await _producer.stop()
        _producer = None
