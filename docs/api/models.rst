数据模型
========

.. module:: metacar.models

MetaCar 库使用了丰富的数据模型来表示场景中的各种元素，包括道路、车辆、交通灯等。这些数据模型都是使用 Python 的 dataclass 实现的，提供了类型提示、自动生成的初始化方法以及更好的代码可读性，使得开发者能够更清晰地理解和使用这些数据结构。

数据解析工具
---------------

.. autofunction:: metacar.models.parse_data

场景和道路相关
----------------

子场景信息
~~~~~~~~~~~~~

.. autoclass:: metacar.SubSceneInfo
   :members:

地图配置
~~~~~~~~~~~

.. autoclass:: metacar.models.MapConfig
   :members:

道路标记类型
~~~~~~~~~~~~~~

.. autoclass:: metacar.LineType
   :members:
   :member-order: bysource
   :show-inheritance:

边界信息
~~~~~~~~~~~

.. autoclass:: metacar.BorderInfo
   :members:

车道信息
~~~~~~~~~~~

.. autoclass:: metacar.LaneInfo
   :members:

道路驾驶类型
~~~~~~~~~~~~~~

.. autoclass:: metacar.DrivingType
   :members:
   :member-order: bysource
   :show-inheritance:

交通标志类型
~~~~~~~~~~~~~~

.. autoclass:: metacar.TrafficSign
   :members:
   :member-order: bysource
   :show-inheritance:

道路信息
~~~~~~~~~~~

.. autoclass:: metacar.RoadInfo
   :members:

场景静态数据
~~~~~~~~~~~~~~

.. autoclass:: metacar.SceneStaticData
   :members:

车辆和位置相关
----------------

位姿信息
~~~~~~~~~~~

.. autoclass:: metacar.PoseGnss
   :members:

档位模式
~~~~~~~~~~~

.. autoclass:: metacar.GearMode
   :members:
   :member-order: bysource
   :show-inheritance:

主车信息
~~~~~~~~~~~

.. autoclass:: metacar.MainVehicleInfo
   :members:

欧拉角
~~~~~~~

.. autoclass:: metacar.models.EulerAngle
   :members:

传感器相关
------------

摄像头信息
~~~~~~~~~~~

.. autoclass:: metacar.CamaraInfo
   :members:

传感器信息
~~~~~~~~~~~

.. autoclass:: metacar.SensorInfo
   :members:

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

.. autoclass:: metacar.ObstacleInfo
   :members:

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

.. autoclass:: metacar.TrafficLightInfo
   :members:

交通灯组信息
~~~~~~~~~~~~~~

.. autoclass:: metacar.TrafficLightGroupInfo
   :members:

场景状态与控制
---------------

场景状态
~~~~~~~~~~~

.. autoclass:: metacar.SceneStatus
   :members:

仿真动态信息
~~~~~~~~~~~~~~

.. autoclass:: metacar.SimCarMsg
   :members:

车辆控制
~~~~~~~~~~~

.. autoclass:: metacar.VehicleControl
   :members:
