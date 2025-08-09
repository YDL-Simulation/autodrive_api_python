import logging
from pathlib import Path
from pydantic import TypeAdapter, Field
from typing import Annotated
from .sockets import ModelSocket, StreamingSocket, ConnectionClosedError
from .geometry import Vector3
from .models import (
    SimCarMsgOutput,
    VehicleControl,
    VehicleControlDTO,
    RoadInfo,
    SceneStaticData,
    Code1,
    Code2,
    Code3,
    Code4,
    Code5,
)

logger = logging.getLogger(__name__)


class SceneAPI:
    """SceneAPI 是与仿真环境通信的主要接口。

    该类封装了与仿真环境建立连接、获取场景信息、读取车辆状态以及发送控制命令等功能。
    使用流程通常是：创建实例 -> 连接 -> 获取静态数据 -> 进入主循环获取动态数据并发送控制命令。
    """

    def __init__(self):
        """初始化 SceneAPI 实例，但不会立即连接。
        需要调用 connect() 方法与仿真环境建立连接。
        """
        self._move_to_start = 0
        self._move_to_end = 0
        self._model_socket = ModelSocket("127.0.0.1", 5061)
        self._streaming_socket = StreamingSocket("127.0.0.1", 5063)

    def _load_static_data(self, code1: Code1):
        """读取文件内容，组装场景静态信息。

        从指定的地图配置中读取路径文件和地图文件，解析后组装成场景静态信息。

        :param code1: 场景发送的 code1 消息
        """
        map_info = code1.map_info
        dir_path = Path(map_info.path)
        route_path = dir_path / map_info.route
        with route_path.open("rb") as route_file:
            route = TypeAdapter(list[Vector3]).validate_json(route_file.read())
        map_path = dir_path / map_info.map
        with map_path.open("rb") as map_file:
            road_lines = TypeAdapter(list[RoadInfo]).validate_json(map_file.read())
        self._scene_static_data = SceneStaticData(
            route=route,
            roads=road_lines,
            sub_scenes=map_info.sub_scenes,
        )

    def connect(self):
        """与场景建立连接，会产生阻塞，直到与场景连接成功。

        此方法会阻塞执行，直到成功与仿真环境建立连接并完成握手。
        连接成功后会加载场景静态数据，可通过 get_scene_static_data() 获取。
        """
        self._model_socket.accept()  # 连接 json socket
        self._streaming_socket.accept()  # 连接视频流
        code1: Code1 = self._model_socket.recv(Code1)
        self._load_static_data(code1)

    def get_scene_static_data(self):
        """获取场景静态信息，仅在 connect() 函数调用后可用

        此方法返回加载的场景静态数据，包括路线、道路信息和子场景信息。
        必须在调用 connect() 方法后才能使用。

        :return: 场景静态数据
        """
        return self._scene_static_data

    def main_loop(self):
        """生成器，每次迭代返回 :class:`~metacar.models.SimCarMsg` 和图像帧，场景结束时退出。

        此方法是一个生成器，每次迭代会返回当前的仿真车辆消息和摄像头图像帧。
        当场景结束或连接中断时，生成器会自动退出。

        :return: 元组 (sim_car_msg, frame)，其中:

            - sim_car_msg: :class:`~metacar.models.SimCarMsg` 对象，包含车辆状态、传感器数据等信息
            - frame: 当前相机视图，为 OpenCV 图像格式(numpy.ndarray)，BGR 颜色空间，
              通常分辨率为640x480像素
        """
        # 先发送 code2，告知场景已经就绪
        self._model_socket.send(Code2(code=2), Code2)
        # 进入主循环，持续从场景接收消息
        try:
            while True:
                message: Code3 | Code5 = self._model_socket.recv(
                    Annotated[Code3 | Code5, Field(discriminator="code")]
                )
                if isinstance(message, Code5):
                    logger.info("场景结束")
                    return
                sim_car_msg = message.sim_car_msg
                frame = self._streaming_socket.recv()
                yield sim_car_msg, frame
        except ConnectionClosedError:
            logger.warning("连接中断，退出场景")
            return
        finally:
            self._model_socket.close()
            self._streaming_socket.close()

    def set_vehicle_control(self, vc: VehicleControl):
        """发送车辆控制命令到仿真环境

        将给定的车辆控制命令发送到场景，用于控制车辆的油门、刹车、转向等行为。

        :param vc: 车辆控制命令，包含油门、刹车、转向等参数
        """
        vc_dto = VehicleControlDTO.model_validate(
            vc.model_dump()
            | {
                "move_to_start": self._move_to_start,
                "move_to_end": self._move_to_end,
            },
            by_name=True,
            by_alias=False,
        )
        sim_car_msg = SimCarMsgOutput(VehicleControl=vc_dto)
        self._model_socket.send(Code4(code=4, SimCarMsg=sim_car_msg), Code4)

    def retry_level(self):
        """重试关卡

        增加重试关卡计数器，在下一次发送控制命令时会通知场景重试当前关卡。
        """
        self._move_to_start += 1
        logger.info("重试关卡")

    def skip_level(self):
        """跳过关卡

        增加跳过关卡计数器，在下一次发送控制命令时会通知场景跳过当前关卡。
        """
        self._move_to_end += 1
        logger.info("跳过关卡")
