示例代码
========

本节包含一些使用 MetaCar 库的示例和教程，帮助您更快地理解如何实现自己的应用。

基础控制示例
--------------

以下是一个基础的车辆控制示例，展示了如何使用键盘输入来控制车辆：

.. literalinclude:: ../examples/main.py
   :language: python
   :linenos:
   :caption: 基础控制示例 (examples/main.py)

这个例子展示了：

1. 如何创建和连接 SceneAPI
2. 如何使用键盘输入控制车辆
3. 如何使用 Stanley 横向控制算法控制车辆
4. 如何在主循环中不断获取车辆状态并发送控制命令

GUI 界面示例
---------------

MetaCar 库还包含了一个使用 GUI 界面展示车辆状态的示例。您可以在以下位置找到完整代码：

* ``examples/gui.py`` - GUI 界面实现代码

这个示例展示了：

1. 如何创建图形界面展示车辆状态
2. 如何解析和显示车辆传感器数据
3. 如何实时更新界面中显示的内容

开发您的第一个应用
------------------

开发自己的应用程序时，建议按照以下流程进行：

1. 引入所需的模块和类
2. 初始化并连接 SceneAPI
3. 设计车辆控制算法
4. 在主循环中实时处理数据并发送控制指令

代码框架示例：

.. code-block:: python

    from metacar import SceneAPI, VehicleControl, GearMode
    import logging
    
    # 配置日志系统
    logging.basicConfig(filename="myapp.log", level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    def main():
        # 初始化 API
        api = SceneAPI()
        
        # 建立仿真连接
        api.connect()
        logger.info("成功连接仿真环境")
        
        # 获取场景静态信息
        static_data = api.get_scene_static_data()
        
        # 启动主循环
        for sim_car_msg, frame in api.main_loop():
            # 在此处实现控制算法
            vc = VehicleControl()
            
            # 向仿真环境发送控制指令
            api.set_vehicle_control(vc)
        
        logger.info("仿真任务完成")
