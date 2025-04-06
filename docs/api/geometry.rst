几何工具
========

.. module:: metacar.geometry

几何模块提供了二维和三维向量的实现，以及一系列相关的数学运算，用于处理位置、方向和变换等操作。

二维向量
-----------

.. autoclass:: metacar.Vector2
   :members:
   :member-order: bysource

二维向量支持以下操作：

* 加法、减法（向量与向量）
* 乘法、除法（向量与标量）
* 旋转
* 角度计算

示例
~~~~

.. code-block:: python

    from metacar import Vector2
    
    # 创建向量
    v1 = Vector2(3.0, 4.0)
    v2 = Vector2(1.0, 2.0)
    
    # 向量运算
    v3 = v1 + v2  # 结果: Vector2(4.0, 6.0)
    v4 = v1 * 2.0  # 结果: Vector2(6.0, 8.0)
    
    # 计算角度
    angle = v1.angle_rad()  # 弧度
    
    # 旋转向量
    rotated = v1.rotate_rad(1.57)  # 旋转约90度

三维向量
-----------

.. autoclass:: metacar.Vector3
   :members:
   :member-order: bysource

三维向量支持以下操作：

* 加法、减法（向量与向量）
* 乘法、除法（向量与标量）
* 偏航角计算
* 转换为二维向量

示例
~~~~

.. code-block:: python

    from metacar import Vector3
    
    # 创建向量
    v1 = Vector3(3.0, 4.0, 1.0)
    v2 = Vector3(1.0, 2.0, 3.0)
    
    # 向量运算
    v3 = v1 + v2  # 结果: Vector3(4.0, 6.0, 4.0)
    v4 = v1 * 2.0  # 结果: Vector3(6.0, 8.0, 2.0)
    
    # 计算偏航角
    yaw = v1.yaw_rad()  # 弧度
    
    # 转换为二维向量
    v2d = v1.to_vector2()  # 结果: Vector2(3.0, 4.0) 