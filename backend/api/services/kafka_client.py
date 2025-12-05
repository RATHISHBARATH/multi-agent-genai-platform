"""Kafka producer/consumer wrapper with in-memory fallback for local dev."""
import os, json, logging, threading, time
logger = logging.getLogger("autoscillab.kafka")

try:
    from kafka import KafkaProducer, KafkaConsumer
    KAFKA_AVAILABLE = True
except Exception:
    KAFKA_AVAILABLE = False

from queue import Queue, Empty

class InMemoryQueue:
    def __init__(self):
        self.q = Queue()

    def push(self, topic, message: dict):
        self.q.put((topic, message))

    def poll(self, timeout=1.0):
        try:
            return self.q.get(timeout=timeout)
        except Empty:
            return None

class KafkaClient:
    def __init__(self, bootstrap_servers=None):
        self.bootstrap = bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP', 'kafka:9092')
        if KAFKA_AVAILABLE:
            try:
                self.producer = KafkaProducer(bootstrap_servers=self.bootstrap,
                                              value_serializer=lambda v: json.dumps(v).encode('utf-8'))
                logger.info("Kafka producer connected to %s", self.bootstrap)
            except Exception as e:
                logger.exception("Kafka init failed, falling back to in-memory: %s", e)
                self.producer = None
        else:
            self.producer = None
        self._inmem = InMemoryQueue()

    def send(self, topic: str, message: dict):
        if self.producer:
            try:
                fut = self.producer.send(topic, message)
                fut.get(timeout=10)
                return True
            except Exception as e:
                logger.exception("Kafka send failed: %s", e)
                # fallback to memory
        self._inmem.push(topic, message)
        return True

    def consume_loop(self, topics, handler, stop_event):
        """Start a blocking consumer loop calling handler(topic,msg)"""
        if KAFKA_AVAILABLE:
            try:
                consumer = KafkaConsumer(*topics, bootstrap_servers=self.bootstrap,
                                         value_deserializer=lambda b: json.loads(b.decode('utf-8')),
                                         auto_offset_reset='earliest', enable_auto_commit=True)
                for msg in consumer:
                    if stop_event.is_set(): break
                    handler(msg.topic, msg.value)
            except Exception as e:
                logger.exception("Kafka consume failed, switching to in-memory: %s", e)
        # fall back to processing in-memory queue
        while not stop_event.is_set():
            item = self._inmem.poll(timeout=1.0)
            if item is None: continue
            t, m = item
            if t in topics:
                handler(t, m)
