import multiprocessing
from typing import List
from application_business_rules.rules import Log, Logger, MotionDetector, ProcessVector, Queue, SingleShotDetector
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
    def process(self, motion_vector: MotionVector) -> DetectionVector:
        return DetectionVector(
            timestamp=motion_vector.timestamp,
            frame_id=motion_vector.frame_id,
            bounding_box=motion_vector.bounding_box,
            class_prediction_vector=[Prediction(prediction="cat", percent=80.1), Prediction(prediction="human", percent=10.5)]
        )
