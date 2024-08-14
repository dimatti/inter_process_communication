import multiprocessing
from typing import List

from application_business_rules.rules import (
    Log,
    Logger,
    MotionDetector,
    ProcessVector,
    Queue,
    SingleShotDetector,
    start_logger,
    start_motion_detector,
    start_single_shot_detector,
)
from entities.vectors import DetectionVector, MotionVector, Prediction, Vector


class LogAdapter(Log):
    def log(self, vector: Vector) -> None:
        print(vector, "\n")


class QueueAdapter(Queue):
    def __init__(self, queue: multiprocessing.Queue) -> None:
        self.queue = queue

    def put(self, vector: Vector) -> None:
        return self.queue.put(vector)

    def get(self) -> Vector:
        return self.queue.get()


class ProcessVectorAdapter(ProcessVector):
    """
    Adapter for processing motion vectors into detection vectors.

    This class simulates processing by generating dummy prediction data.

    Methods:
        process(motion_vector: MotionVector) -> DetectionVector: Processes a motion vector
        and returns a detection vector with dummy predictions.
    """

    def process(self, motion_vector: MotionVector) -> DetectionVector:
        return DetectionVector(
            timestamp=motion_vector.timestamp,
            frame_id=motion_vector.frame_id,
            bounding_box=motion_vector.bounding_box,
            class_prediction_vector=[
                Prediction(prediction="cat", percent=80.1),
                Prediction(prediction="human", percent=10.5),
            ],
        )


def get_motion_detector_process(
    detection_queue: Queue, logger_queue: Queue, vectors: List[Vector]
) -> multiprocessing.Process:
    """
    Creates a multiprocessing process for the MotionDetector.

    Args:
        detection_queue (Queue): The queue for sending vectors to the detector.
        logger_queue (Queue): The queue for sending vectors to the logger.
        vectors (List[Vector]): A list of vectors to be processed.

    Returns:
        multiprocessing.Process: A process running the motion detector.
    """
    motion_detector = MotionDetector(detection_queue, logger_queue)
    return multiprocessing.Process(
        target=start_motion_detector, args=(motion_detector, vectors)
    )


def get_single_shot_detector_process(
    detection_queue: Queue, logger_queue: Queue
) -> multiprocessing.Process:
    single_shot_detector = SingleShotDetector(
        detection_queue, logger_queue, ProcessVectorAdapter()
    )
    return multiprocessing.Process(
        target=start_single_shot_detector, args=(single_shot_detector,)
    )


def get_logger_process(logger_queue: Queue) -> multiprocessing.Process:
    logger = Logger(logger_queue, LogAdapter())
    return multiprocessing.Process(target=start_logger, args=(logger,))
