from dataclasses import dataclass
from typing import List


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
class Vector:
    timestamp: float
    frame_id: int
    bounding_box: BoundingBox


@dataclass
class StopVector(Vector):
    pass


@dataclass
class MotionVector(Vector):
    velocity_vector: Velocity


@dataclass
class DetectionVector(Vector):
    class_prediction_vector: List[Prediction]
