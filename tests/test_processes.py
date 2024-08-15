import multiprocessing

import pytest

from inter_process_communication.entities.vectors import (
    BoundingBox,
    MotionVector,
    Velocity,
)
from inter_process_communication.interface_adapters.adapters import (
    QueueAdapter,
    get_motion_detector_process,
    get_single_shot_detector_process,
)


def create_test_motion_vector():
    return MotionVector(
        timestamp=1625077800.0,
        frame_id=1,
        bounding_box=BoundingBox(x=10, y=20, width=50, height=50),
        velocity_vector=Velocity(vx=1.5, vy=2.5),
    )


@pytest.fixture
def queues():
    m = multiprocessing.Manager()
    detection_queue = QueueAdapter(m.Queue())
    logger_queue = QueueAdapter(m.Queue())
    return detection_queue, logger_queue


def test_process_communication(queues):
    detection_queue, logger_queue = queues

    # Create dummy motion vectors
    motion_vectors = [create_test_motion_vector() for _ in range(5)]

    # Initialize processes
    motion_detector_process = get_motion_detector_process(
        detection_queue, logger_queue, motion_vectors
    )
    single_shot_detector_process = get_single_shot_detector_process(
        detection_queue, logger_queue
    )

    # Start processes
    motion_detector_process.start()
    single_shot_detector_process.start()

    # Wait for processes to finish
    motion_detector_process.join(timeout=2)
    single_shot_detector_process.join(timeout=2)

    if motion_detector_process.is_alive():
        motion_detector_process.terminate()

    if single_shot_detector_process.is_alive():
        single_shot_detector_process.terminate()

    # Check results
    # Ensure the logger queue received messages
    assert not logger_queue.queue.empty(), "Logger queue should not be empty"
    assert logger_queue.queue.qsize() == 10, "Logger queue should be equal 10 (5*2)"

    # Ensure detection queue was consumed by SingleShotDetector
    assert detection_queue.queue.empty(), "Detection queue should be empty"
