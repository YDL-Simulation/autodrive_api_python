# MetaCar - 智能网联平台API

MetaCar 是一个用于智能网联汽车仿真平台的 Python API，提供了与仿真环境通信、获取场景数据以及发送车辆控制命令的功能。

## 功能特性

- 与仿真环境的 TCP 通信
- 获取场景静态数据（道路、路径等）
- 实时获取车辆状态和传感器数据
- 发送车辆控制命令（油门、刹车、转向等）
- 摄像头视频流处理
- 矢量计算和几何工具
- 丰富的数据模型

## 安装

```bash
pip install metacar
```

## 基本使用

```python
from metacar import SceneAPI, VehicleControl, GearMode

# 创建 API 实例并连接
api = SceneAPI()
api.connect()

# 获取场景静态数据
static_data = api.get_scene_static_data()

# 主循环
for sim_car_msg, frames in api.main_loop():
    # 创建控制命令
    vc = VehicleControl()
    vc.throttle = 0.5  # 设置油门 (0-1)
    vc.steering = 0.0  # 设置方向盘 (-1 左, 0 中, 1 右)
    
    # 发送控制命令
    api.set_vehicle_control(vc)
```

## 示例代码

在 `examples` 目录中包含了多个示例：

- `main.py` - 基础的键盘控制示例
- `gui.py` - 带图形界面的状态显示示例

## 文档

完整的文档可以在以下方式获取：

1. [在线文档](https://autodrive-api-python.readthedocs.io/zh-cn/latest/) - 查看最新的 API 文档
2. 本地构建：
   ```bash
   cd docs
   pip install -r requirements.txt
   make html
   ```

## 系统要求

- Python 3.10 或更高版本

## 许可证

本项目使用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
