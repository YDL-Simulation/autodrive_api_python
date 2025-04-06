网络通信
========

.. module:: metacar.sockets

网络模块实现了与仿真环境通信所需的各种 Socket 类，包括基础 Socket、JSON Socket 以及视频流 Socket。通常，这些类会被 SceneAPI 内部使用，无需直接调用。

异常类
-------

.. autoclass:: metacar.sockets.ConnectionClosedError
   :show-inheritance:

Socket 基类
------------

.. autoclass:: metacar.sockets.SocketBase
   :members:

基础 Socket 提供了以下功能：

* 创建 TCP 服务器并监听连接
* 接受客户端连接
* 发送和接收带长度前缀的数据
* 关闭连接

JSON Socket
-----------

.. autoclass:: metacar.sockets.JsonSocket
   :members:
   :show-inheritance:
   
JSON Socket 在基础 Socket 的基础上提供了：

* 发送 Python 对象，自动转换为 JSON 并编码
* 接收 JSON 数据并自动解码为 Python 对象

视频流 Socket
--------------

.. autoclass:: metacar.sockets.StreamingSocket
   :members:
   :show-inheritance:

视频流 Socket 在基础 Socket 的基础上提供了：

* 接收二进制图像数据并转换为 OpenCV 图像
* 返回的图像可直接用于图像处理和显示
