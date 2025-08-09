安装指南
========

系统要求
--------

* Python 3.10 或更高版本
* 网络连接，用于与服务器通信

通过 pip 安装
--------------

推荐使用 pip 安装最新版本的 MetaCar：

.. code-block:: bash

    pip install metacar

从源码安装
----------

您也可以通过克隆代码仓库并安装的方式获取最新开发版本：

.. code-block:: bash

    git clone https://github.com/YDL-Simulation/autodrive_api_python.git
    cd metacar
    pip install -e .

依赖项
------

MetaCar 依赖以下库，在安装过程中会自动安装：

* OpenCV (cv2) - 用于图像处理
* NumPy - 用于科学计算
* Pydantic - 用于数据模型

验证安装
--------

安装完成后，可以通过导入库来验证安装是否成功：

.. code-block:: python

    import metacar
    print(metacar.__version__)
