VLA 场景指南
============

简介
----

VLA（Vision-Language-Action）场景是一类特殊场景。在该类场景中，用户需要根据相机画面中的交通指示牌等视觉内容，识别文字指令，并向场景输出识别到的完整指令文本以及从中解析出的语义片段。

如何辨别 VLA 场景
------------------

- 通过 :meth:`metacar.SceneAPI.get_scene_static_data` 获取到的 :class:`~metacar.SceneStaticData` 中，:attr:`~metacar.SceneStaticData.vla_extension` 不为 ``None`` 即可判断为 VLA 场景。
- 与普通场景的主要差异如下：

  - :attr:`metacar.SceneStaticData.route` 和 :attr:`metacar.SceneStaticData.roads` 为空列表；
  - :attr:`metacar.SceneStatus.end_point` 为 ``None``；
  - :attr:`metacar.SubSceneInfo.start_point` 与 :attr:`metacar.SubSceneInfo.end_point` 为 ``None``。

需要提交什么
--------------

在每个子场景中，用户需要提交一次 :class:`metacar.VLAExtensionOutput`，其结构如下：

- :attr:`~metacar.VLATextOutput.ocr_text`: 识别到的整句 OCR 指令文本（例如“100秒内去到B栋一单元门口”）。
- :attr:`~metacar.VLATextOutput.time_phrase`: 从指令中抽取的时间相关片段（例如“100秒内”）。
- :attr:`~metacar.VLATextOutput.location_phrase`: 从指令中抽取的地点相关片段（例如“B栋一单元门口”）。
- :attr:`~metacar.VLATextOutput.action_phrase`: 从指令中抽取的动作相关片段（例如“去到”）。

如何提交
--------

使用 :meth:`metacar.SceneAPI.set_vehicle_control` 发送车辆控制命令时，可将 :class:`metacar.VLAExtensionOutput` 通过参数 ``vla_extension`` 传入：

.. code-block:: python

    from metacar import SceneAPI, VehicleControl, VLAExtensionOutput, VLATextOutput

    api = SceneAPI()
    api.connect()

    for sim_car_msg, frames in api.main_loop():
        vc = VehicleControl(throttle=0.3)
        vla_payload = VLAExtensionOutput(
            text_info=VLATextOutput(
                ocr_text="100秒内去到B栋一单元门口",
                time_phrase="100秒内",
                location_phrase="B栋一单元门口",
                action_phrase="去到",
            )
        )
        api.set_vehicle_control(vc, vla_extension=vla_payload)

说明：每个子场景仅需要提交一次 ``vla_extension``，同一子场景如多次提交，以最后一次提交为准。

相关模型
--------

VLA 相关数据模型定义见：

- :class:`metacar.VLAExtension`
- :class:`metacar.VLATextOutput`
- :class:`metacar.VLAExtensionOutput`
