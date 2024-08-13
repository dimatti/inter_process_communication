import argparse
import multiprocessing
import random
import time
from typing import List

from application_business_rules.rules import Logger, MotionDetector, SingleShotDetector
from frameworks_and_drivers.input import start_logger, start_motion_detector, start_single_shot_detector
from entities.vectors import BoundingBox, MotionVector, StopVector, Vector, Velocity
from interface_adapters.adapters import LogAdapter, ProcessVectorAdapter, QueueAdapter


def get_vectors(count: int = 5) -> List[Vector]:
    vectors = [MotionVector(
                timestamp=random.uniform(time.time()-1000, time.time()),
                frame_id=random.randint(0, 100),
                bounding_box=BoundingBox(x=random.randint(0, 200), y=random.randint(0, 200), width=random.randint(0, 100), height=random.randint(0, 100)),
                velocity_vector=Velocity(vx=random.uniform(0.0, 5.0), vy=random.uniform(0.0, 5.0))
            ) for _ in range(count)]
    vectors.append(StopVector()) # special technical vector to stop sending vectors
    return vectors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interprocessor communication testing program")
    parser.add_argument("count", type=int, help="The number of vectors that will be sent to the MotionDetector")
    
    args = parser.parse_args()
    
    detection_queue = QueueAdapter(multiprocessing.Queue())
    logger_queue = QueueAdapter(multiprocessing.Queue())

    motion_detector = MotionDetector(detection_queue, logger_queue)
    single_shot_detector = SingleShotDetector(detection_queue, logger_queue, ProcessVectorAdapter())
    logger = Logger(logger_queue, LogAdapter())

    motion_detector_process = multiprocessing.Process(target=start_motion_detector, args=(motion_detector, get_vectors(args.count)))
    single_shot_detector_process = multiprocessing.Process(target=start_single_shot_detector, args=(single_shot_detector,))
    logger_process = multiprocessing.Process(target=start_logger, args=(logger,))

    motion_detector_process.start()
    single_shot_detector_process.start()
    logger_process.start()

    motion_detector_process.join()
    single_shot_detector_process.join()
    logger_process.join()
