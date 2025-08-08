import logging
import pika
import json


class RabbitMQHandler(logging.Handler):
    def __init__(self, host='host.docker.internal', port=5672, queue='logs'):
        super().__init__()
        self.host = host
        self.port = port
        self.queue = queue
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)
        except Exception as e:
            print(f"[RabbitMQHandler] Connection error:"
                  f" {e.__class__.__name__}: {e}")
            self.connection = None

    def emit(self, record):
        print("Check: RabbitMQHandler.emit() called")
        try:
            if self.connection is None or self.connection.is_closed:
                self.connect()
            if self.connection is None or self.connection.is_closed:
                return  # Fail silently if rabbit not connected

            message = self.format(record)
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=json.dumps({'log': message}),
                properties=pika.BasicProperties(delivery_mode=2)
            )
        except Exception as e:
            print(f"[RabbitMQHandler] Emit failed: {e}")
