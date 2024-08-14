import abc
from typing import List

from entities.vectors import DetectionVector, MotionVector, StopVector, Vector


class Queue(abc.ABC):
    @abc.abstractmethod
    def put(self, vector: Vector) -> None: ...

    @abc.abstractmethod
    def get(self) -> Vector: ...


class Log(abc.ABC):
    @abc.abstractmethod
    def log(self, vector: Vector) -> None: ...


class ProcessVector(abc.ABC):
    @abc.abstractmethod
    def process(self, motion_vector: MotionVector) -> DetectionVector: ...


class MotionDetector:
    def __init__(self, detection_queue: Queue, logger_queue: Queue) -> None:
        self.detection_queue = detection_queue
        self.logger_queue = logger_queue

    def execute(self, vector: Vector) -> None:
        self.detection_queue.put(vector)
        self.logger_queue.put(vector)


class SingleShotDetector:
    def __init__(
        self, detection_queue: Queue, logger_queue: Queue, processor: ProcessVector
    ) -> None:
        self.detection_queue = detection_queue
        self.logger_queue = logger_queue
        self.processor = processor

    def execute(self) -> None:
        while True:
            vector = self.detection_queue.get()
            if isinstance(vector, StopVector):
                return
            processed = self.processor.process(vector)
            self.logger_queue.put(processed)


class Logger:
    def __init__(self, queue: Queue, log: Log) -> None:
        self.queue = queue
        self.log = log

    def execute(self) -> None:
        while True:
            vector = self.queue.get()
            self.log.log(vector)
            if isinstance(vector, StopVector):
                return
