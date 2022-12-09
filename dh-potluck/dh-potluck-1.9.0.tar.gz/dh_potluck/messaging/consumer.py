import logging
from typing import Iterator, List, Optional

from confluent_kafka import Consumer

from dh_potluck.messaging import Message, MessageEnvelopeSchema
from dh_potluck.messaging.typings import ConsumerConfig
from dh_potluck.messaging.utils import build_consumer_config

LOG = logging.getLogger(__name__)


class MessageConsumer(object):

    _consumer: Consumer
    _is_consuming: bool = False
    _message_schema: MessageEnvelopeSchema = MessageEnvelopeSchema()

    def __init__(
        self,
        consumer_group: str,
        config_overrides: Optional[ConsumerConfig] = None,
    ):
        """
        :param str consumer_group: The kafka consumer group to use
        :param dict config_overrides: Any kafka configuration overrides
        """
        self._consumer = Consumer(build_consumer_config(consumer_group, config_overrides))

    def subscribe(self, topics: List[str]) -> None:
        """
        Subscribe to the list of topics, this makes the connection to Kafka
        :param topics: Topics to connect to
        :return: None
        """
        self._consumer.subscribe(topics)

    def get_messages(self, poll_timeout: float = 1.0) -> Iterator[Message]:
        """
        Get messages from topics

        :param float poll_timeout: Maximum time to block waiting for message. (Seconds)
        :return: Iterator[Message]
        """
        self._is_consuming = True
        while self._is_consuming:
            message = self._consumer.poll(poll_timeout)

            if message is None:
                continue
            if message.error():
                LOG.error(f'Consumer error: {message.error()}')
                continue

            message_value_string = message.value().decode('utf-8')
            LOG.debug(f'Received message: {message_value_string}')
            message_value = self._message_schema.loads(message_value_string)
            yield Message(message.topic(), message_value, message)

    def commit(self, message: Message) -> None:
        """
        Commit the message, this is done after successfully processing the message

        :param Message message: Message to commit
        :return: None
        """
        self._consumer.commit(message.raw_message())

    def shutdown(self) -> None:
        """
        Call when service is shutting down

        :return: None
        """
        LOG.info('Consumer shutting down...')
        self._is_consuming = False
        self._consumer.close()
        LOG.info('Consumer shut down')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
