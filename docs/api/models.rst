数据模型
========

.. module:: metacar.models

MetaCar 库使用了丰富的数据模型来表示场景中的各种元素，包括道路、车辆、交通灯等。这些数据模型都是使用 pydantic 的 BaseModel 实现的，提供了类型提示、自动生成的初始化方法以及更好的代码可读性，使得开发者能够更清晰地理解和使用这些数据结构。

单位说明
--------

除特别说明外，文档中涉及的物理量默认使用以下单位：

- 长度（Length）：米 (m)
- 时间（Time）：秒 (s)
- 速度（Speed）：米每秒 (m/s)

场景和道路相关
----------------

子场景信息
~~~~~~~~~~~~~

.. autopydantic_model:: metacar.SubSceneInfo

道路线类型
~~~~~~~~~~~~~~

.. autoclass:: metacar.LineType
   :members:
   :member-order: bysource
   :show-inheritance:

边界信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.BorderInfo

车道信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.LaneInfo

道路驾驶类型
~~~~~~~~~~~~~~

.. autoclass:: metacar.DrivingType
   :members:
   :member-order: bysource
   :show-inheritance:

交通标志类型
~~~~~~~~~~~~~~

.. autoclass:: metacar.TrafficSignType
   :members:
   :member-order: bysource
   :show-inheritance:

道路信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.RoadInfo

场景静态数据
~~~~~~~~~~~~~~

.. autopydantic_model:: metacar.SceneStaticData

车辆和位置相关
----------------

位姿信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.PoseGnss

档位模式
~~~~~~~~~~~

.. autoclass:: metacar.GearMode
   :members:
   :member-order: bysource
   :show-inheritance:

主车信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.MainVehicleInfo

传感器相关
------------

欧拉角
~~~~~~~

.. autopydantic_model:: metacar.models.EulerAngle

摄像头信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.CameraInfo

传感器信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.SensorInfo

障碍物相关
------------

障碍物类型
~~~~~~~~~~~

.. autoclass:: metacar.ObstacleType
   :members:
   :member-order: bysource
   :show-inheritance:

障碍物信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.ObstacleInfo

交通灯相关
------------

交通灯状态
~~~~~~~~~~~

.. autoclass:: metacar.TrafficLightState
   :members:
   :member-order: bysource
   :show-inheritance:

交通灯信息
~~~~~~~~~~~

.. autopydantic_model:: metacar.TrafficLightInfo

交通灯组信息
~~~~~~~~~~~~~~

.. autopydantic_model:: metacar.TrafficLightGroupInfo

场景状态与控制
---------------

场景状态
~~~~~~~~~~~

.. autopydantic_model:: metacar.SceneStatus

仿真动态信息
~~~~~~~~~~~~~~

.. autopydantic_model:: metacar.SimCarMsg

车辆控制信息
~~~~~~~~~~~~~~

.. autopydantic_model:: metacar.VehicleControl

摄像头图像数据
~~~~~~~~~~~~~~~~

.. autoclass:: metacar.CameraFrame
   :members:

VLA 场景相关
--------------

VLA场景是一类特殊场景，详细说明和使用方法请参见 :doc:`../vla`。

VLA 场景扩展信息
~~~~~~~~~~~~~~~~~~

.. autopydantic_model:: metacar.VLAExtension

VLA 场景文本输出
~~~~~~~~~~~~~~~~~~

.. autopydantic_model:: metacar.VLATextOutput

VLA 场景扩展输出
~~~~~~~~~~~~~~~~~~

.. autopydantic_model:: metacar.VLAExtensionOutput
