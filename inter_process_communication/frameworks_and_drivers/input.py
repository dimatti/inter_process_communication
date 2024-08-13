import random
import time
from typing import List

from application_business_rules.rules import Logger, MotionDetector, SingleShotDetector
from entities.vectors import BoundingBox, MotionVector, StopVector, Vector, Velocity


def start_motion_detector(motion_detector: MotionDetector, vectors: Vector):
    for vector in vectors:
        motion_detector.execute(vector)
        time.sleep(0.1)


def start_single_shot_detector(single_shot_detector: SingleShotDetector):
    single_shot_detector.execute()


def start_logger(logger: Logger):
    logger.execute()
