快速入门
========

本指南将帮助您开始使用 MetaCar 库，通过简单的步骤与仿真环境建立连接并控制车辆。

基本用法
--------

以下是使用 MetaCar 的基本步骤：

1. 导入必要的包和类
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from metacar import SceneAPI, VehicleControl, GearMode

2. 创建 SceneAPI 实例并连接到仿真环境
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    api = SceneAPI()
    api.connect()  # 这将阻塞直到与仿真环境成功连接

3. 获取场景静态数据
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    static_data = api.get_scene_static_data()
    # 静态数据包含路线、道路信息和子场景信息

4. 进入主循环，获取实时数据并控制车辆
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    for sim_car_msg, frames in api.main_loop():
        # sim_car_msg 包含车辆状态、传感器数据、障碍物信息等
        # frames 是当前相机视图的列表，每个元素为 CameraFrame 对象
        
        # 创建控制命令
        control = VehicleControl()
        control.throttle = 0.5  # 设置油门 (0-1)
        control.steering = 0.0  # 设置方向盘 (-1 左, 0 中, 1 右)
        
        # 发送控制命令到仿真环境
        api.set_vehicle_control(control)

完整示例
------------

以下是一个完整的示例，展示了如何创建一个简单的控制循环：

.. code-block:: python

    import logging
    from metacar import SceneAPI, GearMode, VehicleControl

    # 设置日志
    logging.basicConfig(filename="autodrive.log", level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    def main():
        # 创建 API 实例
        api = SceneAPI()
        
        # 连接到仿真环境
        api.connect()
        logger.info("已连接到仿真环境")
        
        # 获取静态数据
        static_data = api.get_scene_static_data()
        logger.info(f"路线点数量: {len(static_data.route)}")
        
        # 进入主循环
        for sim_car_msg, frames in api.main_loop():
            # 这里可以添加图像处理、决策逻辑等

            # 创建简单的前进控制
            vc = VehicleControl()
            vc.gear = GearMode.DRIVE
            vc.throttle = 0.3  # 30% 油门
            
            # 发送控制命令
            api.set_vehicle_control(vc)
            
            # 记录信息
            logger.info(f"当前速度: {sim_car_msg.data_main_vehicle.speed}")
            
        logger.info("仿真结束")

    if __name__ == "__main__":
        main()

VLA 场景（可选）
------------------

如遇到 VLA（Vision-Language-Action）特殊场景，需要在每个子场景中识别指示牌上的文字并提交一次解析结果，详见 :doc:`/vla`。

下一步
----------

* 查看 :doc:`API 文档 <api/index>` 了解更多详细功能
* 阅读 :doc:`示例代码 <examples>` 了解更多高级用法
