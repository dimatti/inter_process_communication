import multiprocessing

import pytest

from inter_process_communication.entities.vectors import (
    BoundingBox,
    MotionVector,
    Velocity,
)
from inter_process_communication.interface_adapters.adapters import (
    ProcessVectorAdapter,
    QueueAdapter,
)


def create_test_motion_vector():
    return MotionVector(
        timestamp=1625077800.0,
        frame_id=1,
        bounding_box=BoundingBox(x=10, y=20, width=50, height=50),
        velocity_vector=Velocity(vx=1.5, vy=2.5),
    )


@pytest.fixture
def queue_adapter():
    queue = multiprocessing.Queue()
    return QueueAdapter(queue)


def test_queue_adapter_put_get(queue_adapter):
    motion_vector = create_test_motion_vector()

    # Put the motion vector in the queue
    queue_adapter.put(motion_vector)

    # Get the motion vector from the queue
    result = queue_adapter.get()

    assert (
        result == motion_vector
    ), "The vector retrieved from the queue should be identical to the one put into it."


def test_process_vector_adapter():
    motion_vector = create_test_motion_vector()
    process_vector_adapter = ProcessVectorAdapter()

    # Process the motion vector to generate a detection vector
    detection_vector = process_vector_adapter.process(motion_vector)

    assert not isinstance(
        detection_vector, MotionVector
    ), "The result should not be an instance of MotionVector."
    assert (
        detection_vector.timestamp == motion_vector.timestamp
    ), "Timestamps should match."
    assert (
        detection_vector.frame_id == motion_vector.frame_id
    ), "Frame IDs should match."
    assert (
        detection_vector.bounding_box == motion_vector.bounding_box
    ), "Bounding boxes should match."
