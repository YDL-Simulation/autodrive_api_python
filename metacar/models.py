from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import TypeVar, Any, get_origin, get_args
import types
from .geometry import Vector2, Vector3

T = TypeVar("T")


def _normalize_member_name(name: str) -> str:
    """将成员名称规则化，去掉下划线并转小写，
    用于匹配 dataclass 中的字段和原始的 JSON 数据"""
    return name.replace("_", "").lower()


def parse_data(cls: type[T], data: Any) -> T:
    """解析数据，将 JSON 数据转换为指定类型的对象。
    支持基本类型、枚举、列表和 dataclass 类型的转换。

    :param cls: 目标类型
    :param data: 原始数据
    :return: 转换后的对象
    """
    if cls is type(None) and data is None:
        return None
    if cls in (int, float, bool, str) and isinstance(data, cls):
        return cls(data)
    if isinstance(cls, type) and issubclass(cls, Enum):
        return cls(data)
    if get_origin(cls) is list and isinstance(data, list):
        return [parse_data(get_args(cls)[0], i) for i in data]
    if is_dataclass(cls) and isinstance(data, dict):
        normalized_data = {_normalize_member_name(k): v for k, v in data.items()}
        cleaned_data = {}
        for field in fields(cls):
            try:
                value = normalized_data[_normalize_member_name(field.name)]
            except KeyError:
                raise KeyError(f"Key '{field.name}' not found when parsing {cls}")
            cleaned_data[field.name] = parse_data(field.type, value)
        return cls(**cleaned_data)
    if get_origin(cls) is types.UnionType:
        # 尝试每一种类型，如果都不匹配，则抛出异常
        for optional_type in get_args(cls):
            try:
                return parse_data(optional_type, data)
            except Exception:
                pass
        raise TypeError(f"Cannot convert type {type(data)} to union type {cls}")
    raise TypeError(f"Unsupported conversion from {type(data)} to {cls}")


@dataclass
class SubSceneInfo:
    sub_scene_name: str  #: 子场景名称
    start_point: Vector3  #: 起点
    end_point: Vector3  #: 终点


@dataclass
class MapConfig:
    path: str  #: 地图目录路径
    route: str  #: 路线文件名
    map: str  #: 地图文件名
    sub_scene_info: list[SubSceneInfo]  #: 子场景信息


class LineType(Enum):
    MIDDLE_LINE = 1  #: 中线
    SIDE_LINE = 2  #: 侧线
    SOLID_LINE = 3  #: 实线
    STOP_LINE = 4  #: 停止线
    ZEBRA_CROSSING = 5  #: 斑马线
    DASH_LINE = 6  #: 虚线


@dataclass
class BorderInfo:
    """车道边界信息"""

    border_type: LineType  #: 边界类型
    path_point: list[Vector2]  #: 组成边界线的点，相邻点间隔约 3~5 米


@dataclass
class LaneInfo:
    """车道信息"""

    id: str  #: 车道 ID
    left_border: BorderInfo  #: 左侧边界
    right_border: BorderInfo  #: 右侧边界
    left_lane: str  #: 左侧车道 ID
    right_lane: str  #: 右侧车道 ID
    width: float  #: 车道宽度
    path_point: list[Vector2]  #: 车道中心线


class DrivingType(Enum):
    MOTOR_VEHICLE_ALLOWED = 1  #: 机动车可行驶
    NON_MOTOR_VEHICLE_ALLOWED = 2  #: 非机动车可行驶
    PEDESTRIAN_ALLOWED = 3  #: 行人可行


class TrafficSign(Enum):
    """交通标志"""

    NO_SIGN = 0  #: 无标志
    SPEED_LIMIT_SIGN = 1  #: 限速标志
    STOP_SIGN = 2  #: 停止标志
    V2X_SIGN = 3  #: V2X 标志


@dataclass
class RoadInfo:
    """道路信息，一条道路(Road)由一个或多个车道(Lane)组成"""

    id: str  #: 道路 ID
    begin_pos: Vector3  #: 起点
    end_pos: Vector3  #: 终点
    driving_type: DrivingType  #: 行驶类型
    traffic_sign: TrafficSign  #: 交通标志
    stop_line: list[Vector2]  #: 停止线位置
    predecessor: list[str]  #: 前驱道路 ID
    successor: list[str]  #: 后继道路 ID
    lane_data: list[LaneInfo]  #: 车道信息


@dataclass
class SceneStaticData:
    """场景静态信息"""

    route: list[Vector3]  #: 路线
    road_lines: list[RoadInfo]  #: 道路信息
    sub_scenes: list[SubSceneInfo]  #: 子场景信息


@dataclass
class PoseGnss:
    """车辆位姿信息"""

    pos_x: float  #: 位置 X
    pos_y: float  #: 位置 Y
    pos_z: float  #: 位置 Z
    vel_x: float  #: 速度 X
    vel_y: float  #: 速度 Y
    vel_z: float  #: 速度 Z
    ori_x: float  #: 欧拉角 X（单位：角度）
    ori_y: float  #: 欧拉角 Y（单位：角度）
    ori_z: float  #: 欧拉角 Z（单位：角度）


@dataclass
class DataGnss:
    """GNSS数据"""

    pose_gnss: PoseGnss  #: 车辆位姿信息


class GearMode(Enum):
    """档位模式"""

    NEUTRAL = 0  #: 空档
    DRIVE = 1  #: 前进档
    REVERSE = 2  #: 倒车档
    PARKING = 3  #: 停车档


@dataclass
class MainVehicleInfo:
    """主车信息"""

    main_vehicle_id: int  #: 主车 ID
    speed: float  #: 车速
    gear: GearMode  #: 档位
    throttle: float  #: 油门
    brake: float  #: 刹车
    steering: float  #: 方向盘
    length: float  #: 长度
    width: float  #: 宽度
    height: float  #: 高度
    signal_light_left_blinker: bool  #: 左转向灯
    signal_light_right_blinker: bool  #: 右转向灯
    signal_light_double_flash: bool  #: 双闪
    signal_light_brake_light: bool  #: 刹车灯
    signal_light_front_light: bool  #: 前灯


@dataclass
class EulerAngle:
    """欧拉角"""

    ori_x: float  #: 欧拉角 X（单位：角度）
    ori_y: float
    ori_z: float


@dataclass
class CamaraInfo:
    """摄像头信息"""

    id: str  #: 摄像头 ID
    position: Vector3  #: 位置
    angle: EulerAngle  #: 角度
    fov: float  #: 视场角
    intrinsic_matrix: list[float]  #: 内参矩阵
    image_w: int  #: 图像宽度
    image_h: int  #: 图像高度


@dataclass
class SensorInfo:
    """传感器信息"""

    ego_rgb_cams: list[CamaraInfo]  #: 主车摄像头
    v2x_cams: list[CamaraInfo]  #: V2X 摄像头


class ObstacleType(Enum):
    """障碍物类型"""

    UNKNOWN = 0  #: 未知障碍物
    PEDESTRIAN = 4  #: 行人
    CAR = 6  #: 小汽车
    STATIC = 7  #: 静态障碍物
    BICYCLE = 8  #: 自行车
    ROAD_MARK = 12  #: 道路标记
    TRAFFIC_SIGN = 13  #: 交通标志
    TRAFFIC_LIGHT = 15  #: 交通信号灯
    RIDER = 17  #: 骑手
    TRUCK = 18  #: 卡车
    BUS = 19  #: 公交车
    SPECIAL_VEHICLE = 20  #: 特种车辆
    MOTORCYCLE = 21  #: 摩托车
    DYNAMIC = 22  #: 动态障碍物
    SPEED_LIMIT_SIGN = 26  #: 限速标志
    BICYCLE_STATIC = 27  #: 静止自行车
    ROAD_OBSTACLE = 29  #: 道路障碍物
    PARKING_SLOT = 30  #: 停车位


@dataclass
class ObstacleInfo:
    """障碍物信息"""

    id: int  #: 障碍物 ID
    type: ObstacleType  #: 障碍物类型
    pos_x: float  #: 位置 X
    pos_y: float  #: 位置 Y
    pos_z: float  #: 位置 Z
    vel_x: float  #: 速度 X
    vel_y: float  #: 速度 Y
    vel_z: float  #: 速度 Z
    ori_x: float  #: 欧拉角 X（单位：角度）
    ori_y: float  #: 欧拉角 Y（单位：角度）
    ori_z: float  #: 欧拉角 Z（单位：角度）
    length: float  #: 长度
    width: float  #: 宽度
    height: float  #: 高度
    redundant_value: str | None  #: 冗余值（包含限速标志的限速值）


class TrafficLightState(Enum):
    """交通灯状态"""

    RED = 1  #: 红灯
    GREEN = 2  #: 绿灯
    YELLOW = 3  #: 黄灯


@dataclass
class TrafficLightInfo:
    """一排交通灯的信息"""

    id: str  #: 交通灯 ID
    road_id: str  #: 道路 ID
    position: Vector3  #: 位置
    turn_left_state: TrafficLightState  #: 左转状态
    turn_left_remainder: float  #: 左转剩余时间
    turn_right_state: TrafficLightState  #: 右转状态
    turn_right_remainder: float  #: 右转剩余时间
    straight_state: TrafficLightState  #: 直行状态
    straight_remainder: float  #: 直行剩余时间


@dataclass
class TrafficLightGroupInfo:
    """交通灯组信息"""

    id: str  #: 交通灯组 ID
    traffic_light_state: list[TrafficLightInfo]  #: 交通灯信息


@dataclass
class SceneStatus:
    """场景状态信息"""

    sub_scene_name: str  #: 子场景名称
    used_time: float  #: 已用时间
    time_limit: float  #: 时间限制
    end_point: Vector3  #: 终点


@dataclass
class SimCarMsg:
    """仿真动态信息"""

    trajectory: list[Vector3]  #: 推荐轨迹
    data_gnss: DataGnss  #: GNSS 数据
    data_main_vehicle: MainVehicleInfo  #: 主车信息
    sensor: SensorInfo  #: 传感器信息
    obstacle_entry_list: list[ObstacleInfo]  #: 障碍物信息
    traffic_light_state_lists: list[TrafficLightGroupInfo]  #: 交通灯组信息
    scene_status: SceneStatus  #: 场景状态信息


@dataclass
class VehicleControl:
    throttle: float = 0.0  #: 油门（0~1）
    brake: float = 0.0  #: 刹车（0~1）
    steering: float = 0.0  #: 方向盘（-1~1）
    gear: GearMode = GearMode.DRIVE  #: 档位
    left_blinker: bool = False  #: 左转向灯
    right_blinker: bool = False  #: 右转向灯
    double_flash: bool = False  #: 双闪
    front_light: bool = False  #: 前灯
