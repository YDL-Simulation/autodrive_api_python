from dataclasses import dataclass, astuple
import math


@dataclass
class Vector2:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        return iter(astuple(self))

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector2(*(-a for a in self))

    def __add__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Vector2' and '{type(other).__name__}'"
            )
        return Vector2(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Vector2' and '{type(other).__name__}'"
            )
        return Vector2(*(a - b for a, b in zip(self, other)))

    def __mul__(self, other):
        """标量乘法。"""
        return Vector2(*(a * other for a in self))

    def __rmul__(self, other):
        """标量乘法。"""
        return self * other

    def __truediv__(self, other):
        """标量除法。"""
        return Vector2(*(a / other for a in self))

    def rotate_rad(self, radians) -> "Vector2":
        """绕原点旋转 radians 弧度。"""
        x = self.x * math.cos(radians) - self.y * math.sin(radians)
        y = self.x * math.sin(radians) + self.y * math.cos(radians)
        return Vector2(x, y)

    def angle_rad(self) -> float:
        """计算向量与 x 轴的夹角，单位：弧度。"""
        return math.atan2(self.y, self.x)


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __iter__(self):
        return iter(astuple(self))

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector3(*(-a for a in self))

    def __add__(self, other):
        if not isinstance(other, Vector3):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Vector3' and '{type(other).__name__}'"
            )
        return Vector3(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        if not isinstance(other, Vector3):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Vector3' and '{type(other).__name__}'"
            )
        return Vector3(*(a - b for a, b in zip(self, other)))

    def __mul__(self, other):
        """标量乘法。"""
        return Vector3(*(a * other for a in self))

    def __rmul__(self, other):
        """标量乘法。"""
        return self * other

    def __truediv__(self, other):
        """标量除法。"""
        return Vector3(*(a / other for a in self))

    def yaw_rad(self) -> float:
        """计算向量在 xOy 平面上的投影与 x 轴的夹角，单位：弧度。"""
        return math.atan2(self.y, self.x)

    def to_vector2(self) -> Vector2:
        """返回向量的前两个分量。"""
        return Vector2(self.x, self.y)
