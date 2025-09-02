import logging
import keyboard
import math
from metacar import SceneAPI, GearMode, VehicleControl, Vector3, SimCarMsg

# 是否使用 GUI 界面
USE_GUI = True

if USE_GUI:
    from gui import Dashboard

logging.basicConfig(
    filename="autodrive.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)
logger = logging.getLogger(__name__)

current_gear = GearMode.DRIVE
use_keyboard = True


def set_gear(gear: GearMode):
    global current_gear
    current_gear = gear


def toggle_keyboard():
    global use_keyboard
    use_keyboard = not use_keyboard


def get_vehicle_control_from_keyboard() -> VehicleControl:
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
    pos: Vector3, yaw: float, speed: float, trajectory: list[Vector3]
) -> float:
    K = 0.5
    for traj_pos in trajectory:
        if math.dist(traj_pos, pos) > K * speed:
            target_pos = traj_pos
            break
    else:
        target_pos = trajectory[-1]
    theta = (target_pos - pos).yaw_rad()
    steering_angle = (theta - yaw) % (2 * math.pi)
    if steering_angle > math.pi:
        steering_angle -= 2 * math.pi
    steering = math.degrees(-steering_angle) / 45
    return max(min(steering, 1), -1)


def get_vehicle_control_from_algorithm(msg: SimCarMsg) -> VehicleControl:
    vc = VehicleControl()
    vc.gear = GearMode.DRIVE
    # 目前只支持固定速度
    vc.throttle, vc.brake = calc_throttle_brake(msg.main_vehicle.speed, 15)
    vc.steering = calc_steering(
        Vector3(
            msg.pose_gnss.pos_x,
            msg.pose_gnss.pos_y,
            msg.pose_gnss.pos_z,
        ),
        -math.radians(msg.pose_gnss.ori_z),
        msg.main_vehicle.speed,
        msg.trajectory,
    )
    return vc


def main():
    api = SceneAPI()

    keyboard.add_hotkey("space", api.retry_level)
    keyboard.add_hotkey("n", api.skip_level)

    keyboard.add_hotkey("r", lambda: set_gear(GearMode.REVERSE))
    keyboard.add_hotkey("f", lambda: set_gear(GearMode.DRIVE))
    keyboard.add_hotkey("t", lambda: set_gear(GearMode.NEUTRAL))
    keyboard.add_hotkey("g", lambda: set_gear(GearMode.PARKING))

    keyboard.add_hotkey("c", toggle_keyboard)

    api.connect()
    static_data = api.get_scene_static_data()
    if USE_GUI:
        dashboard = Dashboard(static_data)
        logger.info("启动 GUI 界面")
    logger.info("开始场景")

    for sim_car_msg, frames in api.main_loop():
        if use_keyboard:
            vehicle_control = get_vehicle_control_from_keyboard()
        else:
            vehicle_control = get_vehicle_control_from_algorithm(sim_car_msg)
        api.set_vehicle_control(vehicle_control)
        if USE_GUI:
            dashboard.update(sim_car_msg)
    logger.info("结束场景")
    if USE_GUI:
        dashboard.quit()
        logger.info("关闭 GUI 界面")


if __name__ == "__main__":
    main()
