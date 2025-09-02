场景 API
==========

.. module:: metacar.sceneapi

这个模块提供了与仿真环境交互的主要接口，用于建立连接、获取场景数据以及向场景发送控制命令。

类参考
---------------

.. autoclass:: metacar.SceneAPI
   :members:

基本使用流程
---------------

使用 SceneAPI 的一般流程如下：

1. 创建 SceneAPI 实例
2. 调用 connect() 与仿真环境建立连接
3. 调用 get_scene_static_data() 获取场景静态信息
4. 使用 main_loop() 生成器获取实时数据
5. 在循环中调用 set_vehicle_control() 发送控制命令

示例
------

.. code-block:: python

    from metacar import SceneAPI, VehicleControl
    
    # 创建 API 并连接
    api = SceneAPI()
    api.connect()
    
    # 获取静态数据
    static_data = api.get_scene_static_data()
    print(f"路线点数: {len(static_data.route)}")
    
    # 主循环
    for sim_car_msg, frames in api.main_loop():
        # 创建控制命令
        vc = VehicleControl()
        vc.throttle = 0.5
        
        # 发送控制命令
        api.set_vehicle_control(vc)
