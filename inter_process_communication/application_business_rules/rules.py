import abc
import time

from entities.vectors import DetectionVector, MotionVector, StopVector, Vector


class Queue(abc.ABC):
    """
    Abstract base class for a message queue.

    This class defines the interface for a queue that can store and retrieve vectors.

    Methods:
        put(vector: Vector): Abstract method to put a vector into the queue.
        get() -> Vector: Abstract method to retrieve a vector from the queue.
    """

    @abc.abstractmethod
    def put(self, vector: Vector) -> None: ...

    @abc.abstractmethod
    def get(self) -> Vector: ...


class Log(abc.ABC):
    """
    Abstract base class for logging vectors.

    This class defines the interface for logging vectors.

    Methods:
        log(vector: Vector): Abstract method to log a provided vector.
    """

    @abc.abstractmethod
    def log(self, vector: Vector) -> None: ...


class ProcessVector(abc.ABC):
    """
    Abstract base class for processing motion vectors into detection vectors.

    This class defines the interface for processing a motion vector and converting it into a detection vector.

    Methods:
        process(motion_vector: MotionVector) -> DetectionVector: Abstract method to process a motion vector.
    """

    @abc.abstractmethod
    def process(self, motion_vector: MotionVector) -> DetectionVector: ...


class MotionDetector:
    """
    Class representing a motion detector that sends vectors to detection and logging queues.

    This class is responsible for forwarding vectors to both the detection and logging queues.

    Methods:
        execute(vector: Vector): Sends a vector to both the detection and logging queues.
    """

    def __init__(self, detection_queue: Queue, logger_queue: Queue) -> None:
        self.detection_queue = detection_queue
        self.logger_queue = logger_queue

    def execute(self, vector: Vector) -> None:
        self.detection_queue.put(vector)
        self.logger_queue.put(vector)


class SingleShotDetector:
    """
    Class representing a single-shot detector that processes motion vectors into detection vectors.

    This class processes vectors from the detection queue and sends the results to the logger queue.

    Methods:
        execute(): Continuously processes vectors from the detection queue and stops when a StopVector is received.
    """

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
    """
    Class representing a logger that logs vectors from a queue.

    This class logs all vectors it receives from the queue and stops when a StopVector is received.

    Methods:
        execute(): Continuously logs vectors from the queue and stops when a StopVector is received.
    """

    def __init__(self, queue: Queue, log: Log) -> None:
        self.queue = queue
        self.log = log

    def execute(self) -> None:
        while True:
            vector = self.queue.get()
            self.log.log(vector)
            if isinstance(vector, StopVector):
                return


def start_motion_detector(motion_detector: MotionDetector, vectors: Vector):
    """
    Starts the motion detector process by sending vectors.

    Args:
        motion_detector (MotionDetector): The motion detector instance.
        vectors (Vector): The vectors to process.
    """
    for vector in vectors:
        motion_detector.execute(vector)
        time.sleep(0.1)


def start_single_shot_detector(single_shot_detector: SingleShotDetector):
    """
    Starts the single-shot detector process.

    Args:
        single_shot_detector (SingleShotDetector): The single-shot detector instance.
    """
    single_shot_detector.execute()


def start_logger(logger: Logger):
    """
    Starts the logger process.

    Args:
        logger (Logger): The logger instance.
    """
    logger.execute()
