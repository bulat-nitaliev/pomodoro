from dataclasses import dataclass
from aiokafka import AIOKafkaConsumer


@dataclass
class BrokerConsumer:
    consumer: AIOKafkaConsumer

    async def start_connection(self) -> None:
        await self.consumer.start()

    async def stop_conection(self) -> None:
        await self.consumer.stop()

    async def consume_callback_message(self) -> None:
        print("consumer")
        await self.start_connection()

        try:
            async for message in self.consumer:
                print(message.value)
        finally:
            await self.stop_conection()
