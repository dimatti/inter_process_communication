from dataclasses import dataclass
from typing import List


class Vector:
    """
    Base class for all vector types.

    This class serves as a base for specific types of vectors such as MotionVector and DetectionVector.
    """

    pass


class StopVector(Vector):
    """
    Special vector used to signal the stop of vector transmission.

    This vector is used to indicate the end of a stream of vectors.
    """

    def __str__(self) -> str:
        return "StopVector"


@dataclass
class BoundingBox:
    """
    Represents a bounding box around a detected object.
    """

    x: int
    y: int
    width: int
    height: int


@dataclass
class Velocity:
    """
    Represents a velocity vector with speed and direction.
    """

    vx: float
    vy: float


@dataclass
class Prediction:
    """
    Represents a prediction result for a detected object.

    Attributes:
        prediction (str): The class prediction (e.g., 'car', 'bike').
        percent (float): The confidence level of the prediction.
    """

    prediction: str
    percent: float


@dataclass
class DataVector(Vector):
    """
    Base class for data vectors containing essential metadata.

    Attributes:
        timestamp (float): The time at which the vector was generated.
        frame_id (int): The identifier of the frame associated with this vector.
        bounding_box (BoundingBox): The bounding box around the detected object.
    """

    timestamp: float
    frame_id: int
    bounding_box: BoundingBox


@dataclass
class MotionVector(DataVector):
    """
    Represents a motion vector that includes velocity information.

    Attributes:
        velocity_vector (Velocity): The velocity vector of the detected motion.
    """

    velocity_vector: Velocity


@dataclass
class DetectionVector(DataVector):
    """
    Represents a detection vector that includes class prediction information.

    Attributes:
        class_prediction_vector (List[Prediction]): A list of predictions with confidence levels.
    """

    class_prediction_vector: List[Prediction]
