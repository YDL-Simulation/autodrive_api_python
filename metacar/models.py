from typing import Literal
from pydantic import BaseModel, Field
from enum import Enum
import numpy as np
from dataclasses import dataclass
from .geometry import Vector2, Vector3


class BuildingInfo(BaseModel):
    """建筑物信息"""

    id: str = Field(description="建筑物 ID")
    name: str = Field(alias="displayName", description="建筑物名称")
    pos_x: float = Field(alias="posX", description="位置 X")
    pos_y: float = Field(alias="posY", description="位置 Y")
    pos_z: float = Field(alias="posZ", description="位置 Z")
    ori_x: float = Field(alias="oriX", description="欧拉角 X（单位：角度）")
    ori_y: float = Field(alias="oriY", description="欧拉角 Y（单位：角度）")
    ori_z: float = Field(alias="oriZ", description="欧拉角 Z（单位：角度）")
    length: float = Field(description="长度")
    width: float = Field(description="宽度")
    height: float = Field(description="高度")


class RegionType(Enum):
    """区域类型"""

    NORMAL_PARKING = 0  #: 正常停车区
    RESTRICTED_PARKING = 1  #: 禁停区
    FUNCTION_ZONE = 2  #: 功能区


class RegionInfo(BaseModel):
    """区域信息"""

    id: str = Field(description="区域 ID")
    type: RegionType = Field(description="区域类型")
    pos_x: float = Field(alias="posX", description="位置 X")
    pos_y: float = Field(alias="posY", description="位置 Y")
    pos_z: float = Field(alias="posZ", description="位置 Z")
    ori_x: float = Field(alias="oriX", description="欧拉角 X（单位：角度）")
    ori_y: float = Field(alias="oriY", description="欧拉角 Y（单位：角度）")
    ori_z: float = Field(alias="oriZ", description="欧拉角 Z（单位：角度）")
    length: float = Field(description="长度")
    width: float = Field(description="宽度")


class VLAExtension(BaseModel):
    """VLA 扩展信息"""

    buildings: list[BuildingInfo] = Field(
        alias="BuildingInfos", description="建筑物信息"
    )
    regions: list[RegionInfo] = Field(alias="Regions", description="区域信息")


class VLATextOutput(BaseModel):
    """VLA 场景的文本输出"""

    ocr_text: str = Field(serialization_alias="OcrText", description="OCR 文本")
    time_phrase: str = Field(serialization_alias="TimeText", description="时间相关片段")
    location_phrase: str = Field(
        serialization_alias="LocationText", description="位置相关片段"
    )
    action_phrase: str = Field(
        serialization_alias="ActionText", description="动作相关片段"
    )


class FunctionZoneViolation(BaseModel):
    """功能区违规信息"""

    rule_code: str = Field(alias="ruleCode", description="规则代码")
    sticker_ids: list[str] = Field(alias="stickerIds", description="违规贴纸 ID 列表")


class FunctionZoneResult(BaseModel):
    """功能区检测结果"""

    violations: list[FunctionZoneViolation] = Field(description="违规列表")


class ParkingResult(BaseModel):
    """停车区检测结果"""

    violating_sticker_ids: list[str] = Field(
        alias="violatingStickerIds", description="违规贴纸 ID 列表"
    )


class VLAExtensionOutput(BaseModel):
    """VLA 场景的扩展输出"""

    text_info: VLATextOutput | None = Field(
        default=None, serialization_alias="TextInfo", description="文本相关输出"
    )
    function_zone_result: FunctionZoneResult | None = Field(
        default=None,
        serialization_alias="FunctionZoneResult",
        description="功能区检测结果",
    )
    parking_result: ParkingResult | None = Field(
        default=None, serialization_alias="ParkingResult", description="停车区检测结果"
    )


class SubSceneInfo(BaseModel):
    """子场景信息"""

    name: str = Field(alias="SubSceneName", description="子场景名称")
    start_point: Vector3 | None = Field(
        alias="StartPoint", description="起点（VLA 场景为 None）"
    )
    end_point: Vector3 | None = Field(
        alias="EndPoint", description="终点（VLA 场景为 None）"
    )


class MapConfig(BaseModel):
    """地图配置"""

    path: str = Field(description="地图目录路径")
    route: str = Field(description="路线文件名")
    map: str = Field(description="地图文件名")
    sub_scenes: list[SubSceneInfo] = Field(
        alias="SubSceneInfo", description="子场景信息"
    )


class LineType(Enum):
    """道路线类型"""

    MIDDLE_LINE = 1  #: 中线
    SIDE_LINE = 2  #: 侧线
    SOLID_LINE = 3  #: 实线
    STOP_LINE = 4  #: 停止线
    ZEBRA_CROSSING = 5  #: 斑马线
    DASH_LINE = 6  #: 虚线


class BorderInfo(BaseModel):
    """车道边界信息"""

    type: LineType = Field(alias="borderType", description="边界类型")
    path_points: list[Vector2] = Field(
        alias="pathPoint", description="组成边界线的点，相邻点间隔约 3~5 米"
    )


class LaneInfo(BaseModel):
    """车道信息"""

    id: str = Field(description="车道 ID")
    left_border: BorderInfo = Field(alias="LeftBorder", description="左侧边界")
    right_border: BorderInfo = Field(alias="RightBorder", description="右侧边界")
    left_lane_id: str = Field(alias="leftLane", description="左侧车道 ID")
    right_lane_id: str = Field(alias="rightLane", description="右侧车道 ID")
    width: float = Field(description="车道宽度")
    path_points: list[Vector2] = Field(alias="pathPoint", description="车道中心线")


class DrivingType(Enum):
    """行驶类型"""

    MOTOR_VEHICLE_ALLOWED = 1  #: 机动车可行驶
    NON_MOTOR_VEHICLE_ALLOWED = 2  #: 非机动车可行驶
    PEDESTRIAN_ALLOWED = 3  #: 行人可行


class TrafficSignType(Enum):
    """交通标志"""

    NO_SIGN = 0  #: 无标志
    SPEED_LIMIT_SIGN = 1  #: 限速标志
    STOP_SIGN = 2  #: 停止标志
    V2X_SIGN = 3  #: V2X 标志


class RoadInfo(BaseModel):
    """道路信息，一条道路(Road)由一个或多个车道(Lane)组成"""

    id: str = Field(description="道路 ID")
    begin_pos: Vector3 = Field(alias="beginPos", description="起点")
    end_pos: Vector3 = Field(alias="endPos", description="终点")
    driving_type: DrivingType = Field(alias="drivingType", description="行驶类型")
    traffic_sign_type: TrafficSignType = Field(
        alias="trafficSign", description="交通标志"
    )
    stop_line: list[Vector2] = Field(alias="stopLine", description="停止线位置")
    predecessor_ids: list[str] = Field(alias="predecessor", description="前驱道路 ID")
    successor_ids: list[str] = Field(alias="successor", description="后继道路 ID")
    lanes: list[LaneInfo] = Field(alias="laneData", description="车道信息")


class SceneStaticData(BaseModel):
    """场景静态信息"""

    route: list[Vector3] = Field(description="路线（VLA 场景为空列表）")
    roads: list[RoadInfo] = Field(description="道路信息（VLA 场景为空列表）")
    sub_scenes: list[SubSceneInfo] = Field(description="子场景信息")
    vla_extension: VLAExtension | None = Field(
        description="VLA 扩展信息，该字段不为 None 时表示是 VLA 场景",
    )


class PoseGnss(BaseModel):
    """车辆位姿信息"""

    pos_x: float = Field(alias="posX", description="位置 X")
    pos_y: float = Field(alias="posY", description="位置 Y")
    pos_z: float = Field(alias="posZ", description="位置 Z")
    vel_x: float = Field(alias="velX", description="速度 X")
    vel_y: float = Field(alias="velY", description="速度 Y")
    vel_z: float = Field(alias="velZ", description="速度 Z")
    ori_x: float = Field(alias="oriX", description="欧拉角 X（单位：角度）")
    ori_y: float = Field(alias="oriY", description="欧拉角 Y（单位：角度）")
    ori_z: float = Field(alias="oriZ", description="欧拉角 Z（单位：角度）")


class GearMode(Enum):
    """档位模式"""

    NEUTRAL = 0  #: 空档
    DRIVE = 1  #: 前进档
    REVERSE = 2  #: 倒车档
    PARKING = 3  #: 停车档


class MainVehicleInfo(BaseModel):
    """主车信息"""

    id: int = Field(alias="mainVehicleId", description="主车 ID")
    speed: float = Field(description="车速")
    gear: GearMode = Field(description="档位")
    throttle: float = Field(description="油门")
    brake: float = Field(description="刹车")
    steering: float = Field(description="方向盘")
    length: float = Field(description="长度")
    width: float = Field(description="宽度")
    height: float = Field(description="高度")
    left_blinker_on: bool = Field(
        alias="Signal_Light_LeftBlinker", description="左转向灯"
    )
    right_blinker_on: bool = Field(
        alias="Signal_Light_RightBlinker", description="右转向灯"
    )
    hazard_lights_on: bool = Field(alias="Signal_Light_DoubleFlash", description="双闪")
    brake_lights_on: bool = Field(alias="Signal_Light_BrakeLight", description="刹车灯")
    headlights_on: bool = Field(alias="Signal_Light_FrontLight", description="前灯")


class EulerAngle(BaseModel):
    """欧拉角"""

    # 场景传来的字段严谨一点应该为 oriX, oriY, oriZ，但实际是 orix, oriy, oriz
    # 这里先兼容一下，否则需要修改场景代码
    ori_x: float = Field(alias="orix", description="欧拉角 X（单位：角度）")
    ori_y: float = Field(alias="oriy", description="欧拉角 Y（单位：角度）")
    ori_z: float = Field(alias="oriz", description="欧拉角 Z（单位：角度）")


class CameraInfo(BaseModel):
    """摄像头信息"""

    id: str = Field(alias="Id", description="摄像头 ID")
    position: Vector3 = Field(alias="Position", description="位置")
    orientation: EulerAngle = Field(alias="Angle", description="角度")
    fov: float = Field(alias="Fov", description="视场角")
    intrinsic_matrix: list[float] = Field(
        alias="IntrinsicMatrix", description="内参矩阵"
    )
    image_width: int = Field(alias="ImageW", description="图像宽度")
    image_height: int = Field(alias="ImageH", description="图像高度")


class SensorInfo(BaseModel):
    """传感器信息"""

    ego_rgb_cams: list[CameraInfo] = Field(alias="egoRGBCams", description="主车摄像头")
    v2x_cams: list[CameraInfo] = Field(alias="v2xCams", description="V2X 摄像头")


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
    SPEED_LIMIT_SIGN = 26  #: 限速标志（限速值以 "SpeedLimit|30"(单位：km/h) 的格式在 :attr:`ObstacleInfo.extra_info` 中给出）
    BICYCLE_STATIC = 27  #: 静止自行车
    ROAD_OBSTACLE = 29  #: 道路障碍物
    PARKING_SLOT = 30  #: 停车位


class ObstacleInfo(BaseModel):
    """障碍物信息"""

    id: int = Field(description="障碍物 ID")
    type: ObstacleType = Field(description="障碍物类型")
    pos_x: float = Field(alias="posX", description="位置 X")
    pos_y: float = Field(alias="posY", description="位置 Y")
    pos_z: float = Field(alias="posZ", description="位置 Z")
    vel_x: float = Field(alias="velX", description="速度 X")
    vel_y: float = Field(alias="velY", description="速度 Y")
    vel_z: float = Field(alias="velZ", description="速度 Z")
    ori_x: float = Field(alias="oriX", description="欧拉角 X（单位：角度）")
    ori_y: float = Field(alias="oriY", description="欧拉角 Y（单位：角度）")
    ori_z: float = Field(alias="oriZ", description="欧拉角 Z（单位：角度）")
    length: float = Field(description="长度")
    width: float = Field(description="宽度")
    height: float = Field(description="高度")
    extra_info: str | None = Field(alias="RedundantValue", description="额外信息")


class TrafficLightState(Enum):
    """交通灯状态"""

    RED = 1  #: 红灯
    GREEN = 2  #: 绿灯
    YELLOW = 3  #: 黄灯


class TrafficLightInfo(BaseModel):
    """一排交通灯的信息"""

    id: str = Field(description="交通灯 ID")
    road_id: str = Field(alias="roadId", description="道路 ID")
    position: Vector3 = Field(alias="Position", description="位置")
    left_state: TrafficLightState = Field(alias="turnLeftState", description="左转状态")
    left_remaining_time: float = Field(
        alias="turnLeftRemainder", description="左转剩余时间"
    )
    right_state: TrafficLightState = Field(
        alias="turnRightState", description="右转状态"
    )
    right_remaining_time: float = Field(
        alias="turnRightRemainder", description="右转剩余时间"
    )
    straight_state: TrafficLightState = Field(
        alias="straightState", description="直行状态"
    )
    straight_remaining_time: float = Field(
        alias="straightRemainder", description="直行剩余时间"
    )


class TrafficLightGroupInfo(BaseModel):
    """交通灯组信息，一组交通灯共同表示一个路口的信号灯信息。"""

    id: str = Field(description="交通灯组 ID")
    traffic_lights: list[TrafficLightInfo] = Field(
        alias="trafficLightState", description="交通灯信息"
    )


class SceneStatus(BaseModel):
    """场景状态信息"""

    sub_scene_name: str = Field(alias="SubSceneName", description="子场景名称")
    used_time: float = Field(alias="UsedTime", description="已用时间")
    time_limit: float = Field(alias="TimeLimit", description="时间限制")
    end_point: Vector3 | None = Field(
        alias="EndPoint", description="终点（VLA 场景为 None）"
    )


class SimCarMsg(BaseModel):
    """仿真动态信息"""

    trajectory: list[Vector3] = Field(alias="Trajectory", description="推荐轨迹")
    pose_gnss: PoseGnss = Field(alias="PoseGnss", description="GNSS 数据")
    main_vehicle: MainVehicleInfo = Field(
        alias="DataMainVehicle", description="主车信息"
    )
    sensor: SensorInfo = Field(alias="Sensor", description="传感器信息")
    obstacles: list[ObstacleInfo] = Field(
        alias="ObstacleEntryList", description="障碍物信息"
    )
    traffic_light_groups: list[TrafficLightGroupInfo] = Field(
        alias="TrafficLightStateLists", description="交通灯组信息"
    )
    scene_status: SceneStatus = Field(alias="SceneStatus", description="场景状态信息")


class VehicleControl(BaseModel):
    """车辆控制信息"""

    throttle: float = Field(default=0.0, description="油门（0~1）")
    brake: float = Field(default=0.0, description="刹车（0~1）")
    steering: float = Field(default=0.0, description="方向盘（-1~1）")
    gear: GearMode = Field(default=GearMode.DRIVE, description="档位")
    left_blinker_on: bool = Field(default=False, description="左转向灯")
    right_blinker_on: bool = Field(default=False, description="右转向灯")
    hazard_lights_on: bool = Field(default=False, description="双闪")
    headlights_on: bool = Field(default=False, description="前灯")


class VehicleControlDTO(BaseModel):
    """车辆控制场景接口模型"""

    throttle: float = Field(default=0.0, description="油门（0~1）")
    brake: float = Field(default=0.0, description="刹车（0~1）")
    steering: float = Field(default=0.0, description="方向盘（-1~1）")
    gear: GearMode = Field(default=GearMode.DRIVE, description="档位")
    left_blinker_on: bool = Field(
        serialization_alias="Signal_Light_LeftBlinker",
        default=False,
        description="左转向灯",
    )
    right_blinker_on: bool = Field(
        serialization_alias="Signal_Light_RightBlinker",
        default=False,
        description="右转向灯",
    )
    hazard_lights_on: bool = Field(
        serialization_alias="Signal_Light_DoubleFlash",
        default=False,
        description="双闪",
    )
    headlights_on: bool = Field(
        serialization_alias="Signal_Light_FrontLight", default=False, description="前灯"
    )
    move_to_start: int = Field(serialization_alias="movetostart", description="重开")
    move_to_end: int = Field(serialization_alias="movetoend", description="跳关")


class SimCarMsgOutput(BaseModel):
    """code4 中使用的输出结构"""

    vehicle_control: VehicleControlDTO = Field(serialization_alias="VehicleControl")
    vla_extension: VLAExtensionOutput | None = Field(
        serialization_alias="VLAExtension",
        description="VLA 相关的输出，非 VLA 场景时为 None",
    )


class Code1(BaseModel):
    """code1 接口模型，接收静态信息"""

    code: Literal[1]
    map_info: MapConfig = Field(alias="MapInfo")
    vla_extension: VLAExtension | None = Field(
        default=None,
        alias="VLAExtension",
        description="VLA 扩展信息，如果为 None 则表示不是 VLA 场景",
    )


class Code2(BaseModel):
    """code2 接口模型，发送API已就绪"""

    code: Literal[2]


class Code3(BaseModel):
    """code3 接口模型，接收仿真动态信息"""

    code: Literal[3]
    sim_car_msg: SimCarMsg = Field(alias="SimCarMsg")


class Code4(BaseModel):
    """code4 接口模型，发送控制信息"""

    code: Literal[4]
    sim_car_msg: SimCarMsgOutput = Field(serialization_alias="SimCarMsg")


class Code5(BaseModel):
    """code5 接口模型，接收场景结束信息"""

    code: Literal[5]


@dataclass
class CameraFrame:
    """摄像头图像数据"""

    id: str  #: 对应 :attr:`CameraInfo.id`
    frame: np.ndarray  #: 图像数据
