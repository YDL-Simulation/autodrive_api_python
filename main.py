import logging
import keyboard
import math
from scene_api import (
    SceneAPI,
    VehicleControl,
    GearMode,
    SceneInfo,
    ConnectionClosedError,
    Vector3,
    ObjectInfo,
)

USE_GUI = True

if USE_GUI:
    from gui import Dashboard

logging.basicConfig(filename="autodrive.log", level=logging.DEBUG, encoding="utf-8")
logger = logging.getLogger(__name__)

current_gear = GearMode.DRIVE
use_keyboard = False


def set_gear(gear: GearMode):
    global current_gear
    current_gear = gear


def toggle_keyboard():
    global use_keyboard
    use_keyboard = not use_keyboard


def get_vehicle_control_from_keyboard(scene_info: SceneInfo) -> VehicleControl:
    vc = VehicleControl()
    vc.gear = current_gear
    if keyboard.is_pressed("up") or keyboard.is_pressed("w"):
        value = 0.5 if keyboard.is_pressed("shift") else 1
        if current_gear == GearMode.DRIVE:
            vc.throttle = value
        elif current_gear == GearMode.REVERSE:
            vc.brake = value
    elif keyboard.is_pressed("down") or keyboard.is_pressed("s"):
        value = 0.5 if keyboard.is_pressed("shift") else 1
        if current_gear == GearMode.DRIVE:
            vc.brake = value
        elif current_gear == GearMode.REVERSE:
            vc.throttle = value
    if keyboard.is_pressed("left") or keyboard.is_pressed("a"):
        vc.steering = -1
    elif keyboard.is_pressed("right") or keyboard.is_pressed("d"):
        vc.steering = 1
    return vc


def calc_throttle_brake(
    current_speed: float, target_speed: float
) -> tuple[float, float]:
    K = 0.2
    B = 0.2
    acceleration = (target_speed - current_speed) * K + B
    if acceleration > 0:
        return min(acceleration, 1), 0
    return 0, min(-acceleration * 0.5, 1)


# Stanley 算法
def calc_steering(
    main_vehicle_info: ObjectInfo, speed: float, trajectory: list[Vector3]
) -> float:
    if len(trajectory) < 3:
        return 0
    K = 0.5
    # trajectory 的最后两个点都没什么用
    for pos in trajectory[:-2]:
        if math.dist(pos, main_vehicle_info.pos) > K * speed:
            target_pos = pos
            break
    else:
        target_pos = trajectory[-3]
    theta = (target_pos - main_vehicle_info.pos).yaw_rad()
    steering_angle = (theta - main_vehicle_info.yaw) % (2 * math.pi)
    if steering_angle > math.pi:
        steering_angle -= 2 * math.pi
    steering = math.degrees(-steering_angle) / 45 * 2  # 这个 2 是一个调整参数
    return max(min(steering, 1), -1)


def get_vehicle_control_from_algorithm(scene_info: SceneInfo) -> VehicleControl:
    vc = VehicleControl()
    vc.gear = GearMode.DRIVE
    # 目前只支持固定速度
    vc.throttle, vc.brake = calc_throttle_brake(scene_info.main_vehicle_speed, 15)
    vc.steering = calc_steering(
        scene_info.main_vehicle_info,
        scene_info.main_vehicle_speed,
        scene_info.trajectory.points,
    )
    return vc


def main():
    api = SceneAPI()

    keyboard.add_hotkey("space", api.retry_level)
    keyboard.add_hotkey("n", api.skip_level)

    keyboard.add_hotkey("r", lambda: set_gear(GearMode.REVERSE))
    keyboard.add_hotkey("f", lambda: set_gear(GearMode.DRIVE))
    keyboard.add_hotkey("t", lambda: set_gear(GearMode.NEUTRAL))
    keyboard.add_hotkey("g", lambda: set_gear(GearMode.PARK))

    keyboard.add_hotkey("c", toggle_keyboard)

    api.connect()
    if USE_GUI:
        dashboard = Dashboard(api.get_road_lines())
        logger.info("启动 GUI 界面")
    api.ready()
    logger.info("开始场景")

    while True:
        try:
            scene_info = api.get_scene_info()
        except ConnectionClosedError:
            logger.warning("连接中断，退出场景")
            break
        # scene_info 为 None 时表示场景结束
        if scene_info is None:
            break
        if use_keyboard:
            vehicle_control = get_vehicle_control_from_keyboard(scene_info)
        else:
            vehicle_control = get_vehicle_control_from_algorithm(scene_info)
        api.set_vehicle_control(vehicle_control)

        if USE_GUI:
            dashboard.update(scene_info)
    logger.info("结束场景")
    if USE_GUI:
        dashboard.quit()
        logger.info("关闭 GUI 界面")


if __name__ == "__main__":
    main()
