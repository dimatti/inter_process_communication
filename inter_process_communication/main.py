import argparse
import multiprocessing
import random
import time
from typing import List

from entities.vectors import BoundingBox, MotionVector, StopVector, Vector, Velocity
from interface_adapters.adapters import (
    QueueAdapter,
    get_logger_process,
    get_motion_detector_process,
    get_single_shot_detector_process,
)


def get_vectors(count: int = 5) -> List[Vector]:
    vectors = [
        MotionVector(
            timestamp=random.uniform(time.time() - 1000, time.time()),
            frame_id=random.randint(0, 100),
            bounding_box=BoundingBox(
                x=random.randint(0, 200),
                y=random.randint(0, 200),
                width=random.randint(0, 100),
                height=random.randint(0, 100),
            ),
            velocity_vector=Velocity(
                vx=random.uniform(0.0, 5.0), vy=random.uniform(0.0, 5.0)
            ),
        )
        for _ in range(count)
    ]
    vectors.append(StopVector())  # special technical vector to stop sending vectors
    return vectors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interprocessor communication testing program"
    )
    parser.add_argument(
        "count",
        type=int,
        help="The number of vectors that will be sent to the MotionDetector",
    )

    args = parser.parse_args()

    detection_queue = QueueAdapter(multiprocessing.Queue())
    logger_queue = QueueAdapter(multiprocessing.Queue())

    motion_detector_process = get_motion_detector_process(
        detection_queue, logger_queue, get_vectors(args.count)
    )
    single_shot_detector_process = get_single_shot_detector_process(
        detection_queue, logger_queue
    )
    logger_process = get_logger_process(logger_queue)

    motion_detector_process.start()
    single_shot_detector_process.start()
    logger_process.start()

    motion_detector_process.join()
    single_shot_detector_process.join()
    logger_process.join()
