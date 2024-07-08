import logging
from enum import Enum
import json
import math
from .json_socket import JsonSocket
from .geometry import Vector3

logger = logging.getLogger(__name__)


def _ori_z_to_radians(ori_z: float) -> float:
    """
    将场景中给出的 oriZ （单位：角度，正方向为顺时针）转换为正常的 yaw （单位：弧度，正方向为逆时针）。
    """
    return math.radians(-ori_z)


class GearMode(Enum):
    NEUTRAL = 0
    DRIVE = 1
    REVERSE = 2
    PARK = 3


class VehicleControl:
    def __init__(
        self,
        throttle=0.0,
        brake=0.0,
        steering=0.0,
        handbrake=False,
        is_manual_gear=False,
        gear=GearMode.DRIVE,
    ):
        self.throttle = throttle
        self.brake = brake
        self.steering = steering
        self.handbrake = handbrake
        self.is_manual_gear = is_manual_gear
        self.gear = gear


class ObjectInfo:
    def __init__(
        self,
        pos: Vector3,
        vel: Vector3,
        ori_x: float,
        ori_y: float,
        ori_z: float,
        length: float,
        width: float,
        height: float,
    ):
        self.pos = pos
        self.vel = vel
        self.yaw = _ori_z_to_radians(ori_z)
        self.length = length
        self.width = width
        self.height = height


class ObstacleInfo(ObjectInfo):
    def __init__(
        self,
        pos: Vector3,
        vel: Vector3,
        ori_x: float,
        ori_y: float,
        ori_z: float,
        length: float,
        width: float,
        height: float,
        obstacle_type: str,
    ):
        super().__init__(pos, vel, ori_x, ori_y, ori_z, length, width, height)
        self.type = obstacle_type


class RoadLineType(Enum):
    NULL = 0
    MIDDLE_LINE = 1
    SIDE_LINE = 2
    SOLID_LINE = 3
    STOP_LINE = 4
    ZEBRA_CROSSING = 5
    DASH_LINE = 6


class RoadLineInfo:
    def __init__(self, type: RoadLineType, points: list[Vector3]):
        self.type = type
        self.points = points


class TrajectoryInfo:
    def __init__(self, points: list[Vector3]):
        self.points = points


class SceneInfo:
    def __init__(
        self,
        vehicle_control: VehicleControl,
        main_vehicle: ObjectInfo,
        main_vehicle_speed: float,
        obstacles: list[ObstacleInfo],
        trajectory: TrajectoryInfo,
    ):
        self.vehicle_control = vehicle_control
        self.main_vehicle_info = main_vehicle
        self.main_vehicle_speed = main_vehicle_speed
        self.obstacles = obstacles
        self.trajectory = trajectory


def _get_scene_info_from_sim_car_msg(sim_car_msg: dict) -> SceneInfo:
    vc = sim_car_msg["VehicleControl"]
    vehicle_control = VehicleControl(
        throttle=vc["throttle"],
        brake=vc["brake"],
        steering=vc["steering"],
        handbrake=vc["handbrake"],
        is_manual_gear=vc["isManualGear"],
        gear=GearMode(vc["gear"]),
    )

    gnss = sim_car_msg["DataGnss"]["poseGnss"]
    pos = Vector3(gnss["posX"], gnss["posY"], gnss["posZ"])
    vel = Vector3(gnss["velX"], gnss["velY"], gnss["velZ"])
    ori_x = gnss["oriX"]
    ori_y = gnss["oriY"]
    ori_z = gnss["oriZ"]
    data = sim_car_msg["DataMainVehilce"]
    length = data["length"]
    width = data["width"]
    height = data["height"]
    main_vehicle_info = ObjectInfo(pos, vel, ori_x, ori_y, ori_z, length, width, height)
    main_vehicle_speed = data["speed"]

    obstacles = []
    for obstacle in sim_car_msg["ObstacleEntryList"]:
        pos = Vector3(obstacle["posX"], obstacle["posY"], obstacle["posZ"])
        vel = Vector3(obstacle["velX"], obstacle["velY"], obstacle["velZ"])
        ori_x = obstacle["oriX"]
        ori_y = obstacle["oriY"]
        ori_z = obstacle["oriZ"]
        length = obstacle["length"]
        width = obstacle["width"]
        height = obstacle["height"]
        obstacle_type = obstacle["type"]
        obstacles.append(
            ObstacleInfo(
                pos, vel, ori_x, ori_y, ori_z, length, width, height, obstacle_type
            )
        )

    trajectory_points = []
    for pt in sim_car_msg["Trajectory"]["trajectory"]:
        point = pt["P"]
        trajectory_points.append(Vector3(point["x"], point["y"], point["z"]))
    trajectory = TrajectoryInfo(trajectory_points)

    return SceneInfo(
        vehicle_control, main_vehicle_info, main_vehicle_speed, obstacles, trajectory
    )


class SceneAPI:
    def __init__(self):
        self._move_to_start = 0
        self._move_to_end = 0
        self._socket = JsonSocket()
        self._road_lines = []

    def _read_road_lines(self, road_line_list_file: str):
        with open(road_line_list_file, "r") as f:
            road_lines_data = json.load(f)
        for road_line in road_lines_data:
            road_line_type = RoadLineType(road_line["Type"])
            points = [
                Vector3(point["x"], point["y"], point["z"])
                for point in road_line["PointPath"]
            ]
            self._road_lines.append(RoadLineInfo(road_line_type, points))
        logger.info(f"读取到 {len(self._road_lines)} 条车道线")

    def connect(self):
        self._socket.connect()
        raw_msg = self._socket.recv()
        code = raw_msg["code"]
        if code != 1:
            logger.error(f"握手失败，code: {code}")
            raise RuntimeError("握手失败")
        msg = raw_msg["SimCarMsg"]
        road_line_list_file = msg["MapInfo"]["path"] + "/rd"
        self._read_road_lines(road_line_list_file)
    
    def ready(self):
        code2 = {"code": 2}
        self._socket.send(code2)

    def get_road_lines(self) -> list[RoadLineInfo]:
        """由于车道线信息较大，不适合每次都发送，因此在这里单独给出"""
        return self._road_lines

    def get_scene_info(self):
        message = self._socket.recv()
        code = message["code"]
        if code == 5:
            logger.info("场景结束")
            self._socket.close()
            return None
        sim_car_msg = message["SimCarMsg"]
        scene_info = _get_scene_info_from_sim_car_msg(sim_car_msg)
        return scene_info

    def set_vehicle_control(self, vc: VehicleControl):
        vc_dict = {
            "throttle": vc.throttle,
            "brake": vc.brake,
            "steering": vc.steering,
            "handbrake": vc.handbrake,
            "isManualGear": vc.is_manual_gear,
            "gear": vc.gear.value,
            "movetostart": self._move_to_start,
            "movetoend": self._move_to_end,
        }
        message = {
            "code": 4,
            "SimCarMsg": {
                "VehicleControl": vc_dict,
            },
        }
        self._socket.send(message)

    def retry_level(self):
        self._move_to_start += 1
        logger.info("重试关卡")

    def skip_level(self):
        self._move_to_end += 1
        logger.info("跳过关卡")
