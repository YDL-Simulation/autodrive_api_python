"""
使用 tkinter 和多进程实现的车辆信息显示界面。
之前也尝试过使用多线程，但是 tkinter 的组件只能在创建它的线程中使用，所以只能使用多进程。
"""

from tkinter import *
from tkinter import ttk
from multiprocessing import Process, Queue
import queue
import time
from enum import Enum, auto
import math

from scene_api import SceneInfo, Vector2, ObjectInfo, RoadLineType, RoadLineInfo


class Message(Enum):
    UPDATE = auto()
    QUIT = auto()


def tk_process_func(
    message_queue: Queue, road_lines: list[RoadLineInfo], refresh_interval: int
):
    ROADLINE_COLOR_MAP = {
        RoadLineType.NULL: "black",  # 没有类型
        RoadLineType.MIDDLE_LINE: "dark orange",  # 中线
        RoadLineType.SIDE_LINE: "black",  # 边线
        RoadLineType.SOLID_LINE: "black",  # 实线
        RoadLineType.STOP_LINE: "dark red",  # 停车线
        RoadLineType.ZEBRA_CROSSING: "dark blue",  # 斑马线
        RoadLineType.DASH_LINE: "grey",  # 虚线
    }

    def update(scene_info: SceneInfo):
        string_vars[0].set("{:.3f}".format(scene_info.vehicle_control.throttle))
        string_vars[1].set("{:.3f}".format(scene_info.vehicle_control.brake))
        string_vars[2].set("{:.3f}".format(scene_info.vehicle_control.steering))
        string_vars[3].set(scene_info.vehicle_control.gear.name)
        string_vars[4].set("{:.3f}".format(scene_info.main_vehicle_speed))
        string_vars[5].set("{:.2f}".format(scene_info.main_vehicle_info.pos.x))
        string_vars[6].set("{:.2f}".format(scene_info.main_vehicle_info.pos.y))
        string_vars[7].set(
            "{:.2f}".format(math.degrees(scene_info.main_vehicle_info.yaw) % 360.0)
        )
        # clear canvas
        map_canvas.delete("all")
        canvas_width = map_canvas.winfo_width()
        canvas_height = map_canvas.winfo_height()
        main_vehicle_pos = Vector2(
            scene_info.main_vehicle_info.pos.x, scene_info.main_vehicle_info.pos.y
        )

        def convert_pos(pos: Vector2) -> tuple[float, float]:
            """将场景中的坐标转换为画布上的坐标。"""
            SCALE = 10
            vec = (pos - main_vehicle_pos) * SCALE
            return (canvas_width / 2 + vec.x, canvas_height / 2 - vec.y)

        def should_render(x, y) -> bool:
            """判断坐标是否在二倍画布的范围内。"""
            return (
                -1 * canvas_width <= x < 2 * canvas_width
                and -1 * canvas_height <= y < 2 * canvas_height
            )

        def cut_road_line(
            road_line: RoadLineInfo,
        ) -> tuple[RoadLineType, list[tuple[float, float]]]:
            """裁剪车道线，使其在画布内。"""
            start_index = -1
            end_index = -1
            idx_list = list(range(0, len(road_line.points), 20)) + [
                len(road_line.points) - 1
            ]
            for i in idx_list:
                pt = convert_pos(Vector2(road_line.points[i].x, road_line.points[i].y))
                if should_render(*pt):
                    if start_index == -1:
                        start_index = i
                    end_index = i
            if start_index == -1:
                return road_line.type, []
            return road_line.type, [
                convert_pos(Vector2(point.x, point.y))
                for point in road_line.points[start_index : end_index + 1]
            ]

        def draw_rectangle(
            center_pos: Vector2,
            length: float,
            width: float,
            rotate_rad: float,
            outline_color: str,
        ):
            """绘制带有旋转角度的矩形。"""
            a = Vector2(length / 2, width / 2)
            b = Vector2(length / 2, -width / 2)
            c = Vector2(-length / 2, -width / 2)
            d = Vector2(-length / 2, width / 2)
            a, b, c, d = map(
                lambda v: convert_pos(v.rotate_rad(rotate_rad) + center_pos),
                (a, b, c, d),
            )
            # 绘制无填充的多边形
            map_canvas.create_polygon(a, b, c, d, fill="", outline=outline_color)

        def draw_object(obj: ObjectInfo, color: str):
            pos = Vector2(obj.pos.x, obj.pos.y)
            length = obj.length
            width = obj.width
            yaw = obj.yaw
            draw_rectangle(
                pos,
                length,
                width,
                yaw,
                color,
            )

        # 绘制主车
        draw_object(scene_info.main_vehicle_info, "green")

        # 绘制障碍物
        for obstacle in scene_info.obstacles:
            draw_object(obstacle, "red")

        # 绘制行驶路线
        trajectory_points = [
            convert_pos(Vector2(pt.x, pt.y)) for pt in scene_info.trajectory.points
        ]
        if len(trajectory_points) > 1:
            map_canvas.create_line(trajectory_points, fill="blue")

        # 绘制车道线
        for road_line in road_lines:
            road_line_type, points = cut_road_line(road_line)
            if len(points) > 1:
                map_canvas.create_line(points, fill=ROADLINE_COLOR_MAP[road_line_type])

        # # 绘制停车位
        # parkinglot = message["perceptive_parkinglot"]
        # # 没有停车位时，perceptive_parkinglot 的所有值都为 0
        # if parkinglot["size_length"] != 0 and parkinglot["size_width"] != 0:
        #     pos = Vector2(parkinglot["pos_x"], parkinglot["pos_y"])
        #     length = parkinglot["size_length"]
        #     width = parkinglot["size_width"]
        #     yaw = parkinglot["rot_yaw"]
        #     draw_rectangle(
        #         pos,
        #         length,
        #         width,
        #         yaw_to_radians(yaw),
        #         "dark green",
        #     )

    def check_queue():
        """检查消息队列，如果有消息则处理。"""
        start_time = time.time()
        try:
            message = message_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            match message["type"]:
                case Message.UPDATE:
                    update(message["value"])
                case Message.QUIT:
                    root.destroy()

        # 计算下一次调用 check_queue 的时间
        elapsed_time = time.time() - start_time
        next_interval = max(0, refresh_interval - int(elapsed_time * 1000))
        root.after(next_interval, check_queue)

    root = Tk()
    root.title("仪表盘")

    mainframe = ttk.Frame(root, padding="4 4 4 4")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # 设置数值列的最小宽度，使得数值列的宽度不会随着数值的变化而变化
    mainframe.grid_columnconfigure(1, minsize=60)

    # 仪表盘的各个组件
    labels = ["油门", "刹车", "方向盘", "档位", "速度", "x坐标", "y坐标", "航向角"]
    string_vars = [StringVar() for _ in range(len(labels))]

    for row, (label_str, string_var) in enumerate(zip(labels, string_vars)):
        ttk.Label(mainframe, text=label_str).grid(column=0, row=row, sticky=E)
        ttk.Label(mainframe, textvariable=string_var).grid(column=1, row=row, sticky=W)

    # 在这里设置画布的默认大小
    map_canvas = Canvas(
        mainframe,
        width=480,
        height=480,
        borderwidth=2,
        relief="groove",
        background="white",
    )
    map_canvas.grid(column=2, row=0, rowspan=len(labels), sticky=(N, W, E, S))

    # 窗口大小改变时，将空间分配给画布
    mainframe.grid_columnconfigure(2, weight=1)
    for row in range(len(labels)):
        mainframe.grid_rowconfigure(row, weight=1)

    # 将仪表盘窗口置顶
    root.wm_attributes("-topmost", True)

    root.after_idle(check_queue)
    root.mainloop()


class Dashboard:
    """
    显示车辆信息的仪表盘。
    使用多进程实现，使用 multiprocessing.Queue 作为进程间通信的方式。
    """

    def __init__(self, road_lines: list[RoadLineInfo], refresh_interval: int = 20):
        """
        refresh_interval: 刷新间隔，单位毫秒，一定要比 update 方法的调用频率高。
        """
        self._message_queue = Queue()
        self._tk_process = Process(
            target=tk_process_func,
            args=(self._message_queue, road_lines, refresh_interval),
        )
        self._tk_process.start()

    def update(self, scene_info: SceneInfo):
        """更新仪表盘的方法。"""
        if self._tk_process.is_alive():
            self._message_queue.put({"type": Message.UPDATE, "value": scene_info})

    def quit(self):
        """退出仪表盘的方法。"""
        if self._tk_process.is_alive():
            self._message_queue.put({"type": Message.QUIT})
        self._tk_process.join()
        # 这里需要使用这种方式清空队列，否则可能导致进程无法退出
        while self._message_queue.qsize() > 0:
            self._message_queue.get()
