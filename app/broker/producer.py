from dataclasses import dataclass
import json
from aiokafka import AIOKafkaProducer


@dataclass
class BrokerProducer:
    producer: AIOKafkaProducer
    email_topic: str

    async def kafka_connect(self) -> None:
        await self.producer.start()

    async def close_connect(self) -> None:
        await self.producer.stop()

    async def send_welkome_email(self, email_data: dict) -> None:
        await self.kafka_connect()
        encode_email_data = json.dumps(email_data).encode()
        try:
            await self.producer.send(topic=self.email_topic, value=encode_email_data)
        finally:
            await self.close_connect()
