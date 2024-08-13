from dataclasses import dataclass
from typing import List


class Vector:
    pass


@dataclass
class StopVector(Vector):
    pass


@dataclass
class BoundingBox:
    x: int
    y: int
    width: int
    height: int


@dataclass
class Velocity:
    vx: float
    vy: float


@dataclass
class Prediction:
    prediction: str
    percent: float


@dataclass
class DataVector(Vector):
    timestamp: float
    frame_id: int
    bounding_box: BoundingBox


@dataclass
class MotionVector(DataVector):
    velocity_vector: Velocity


@dataclass
class DetectionVector(DataVector):
    class_prediction_vector: List[Prediction]
