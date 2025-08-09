from pydantic.dataclasses import dataclass
import math


@dataclass
class Vector2:
    x: float  #: x 坐标
    y: float  #: y 坐标

    def __iter__(self):
        return iter((self.x, self.y))

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector2(*(-a for a in self))

    def __add__(self, other: "Vector2"):
        return Vector2(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other: "Vector2"):
        return Vector2(*(a - b for a, b in zip(self, other)))

    def __mul__(self, other: float):
        """标量乘法。"""
        return Vector2(*(a * other for a in self))

    def __rmul__(self, other: float):
        """标量乘法。"""
        return self * other

    def __truediv__(self, other: float):
        """标量除法。"""
        return Vector2(*(a / other for a in self))

    def rotate_rad(self, radians: float) -> "Vector2":
        """绕原点旋转向量。

        将向量绕原点按逆时针方向旋转指定的弧度。

        :param radians: 旋转的角度，单位为弧度
        :type radians: float
        :return: 旋转后的新向量
        :rtype: Vector2
        """
        x = self.x * math.cos(radians) - self.y * math.sin(radians)
        y = self.x * math.sin(radians) + self.y * math.cos(radians)
        return Vector2(x, y)

    def angle_rad(self) -> float:
        """计算向量与 x 轴的夹角。

        计算二维向量与 x 轴正方向的夹角，返回值范围为 [-π, π]。

        :return: 向量与 x 轴的夹角
        :rtype: float
        """
        return math.atan2(self.y, self.x)


@dataclass
class Vector3:
    x: float  #: x 坐标
    y: float  #: y 坐标
    z: float  #: z 坐标

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector3(*(-a for a in self))

    def __add__(self, other: "Vector3"):
        return Vector3(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other: "Vector3"):
        return Vector3(*(a - b for a, b in zip(self, other)))

    def __mul__(self, other: float):
        """标量乘法。"""
        return Vector3(*(a * other for a in self))

    def __rmul__(self, other: float):
        """标量乘法。"""
        return self * other

    def __truediv__(self, other: float):
        """标量除法。"""
        return Vector3(*(a / other for a in self))

    def yaw_rad(self) -> float:
        """计算向量在 xOy 平面上的投影与 x 轴的夹角。

        :returns: 向量在 xOy 平面上的投影与 x 轴正方向的夹角，范围为 [-π, π]，单位为弧度
        :rtype: float
        """
        return math.atan2(self.y, self.x)

    def to_vector2(self) -> Vector2:
        """将三维向量转换为二维向量。

        该方法提取向量的 x 和 y 分量，忽略 z 分量，创建并返回一个新的二维向量。

        :returns: 包含原向量 x 和 y 分量的二维向量
        :rtype: Vector2
        """
        return Vector2(self.x, self.y)
