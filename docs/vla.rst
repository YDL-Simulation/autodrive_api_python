VLA 场景指南
============

简介
----

VLA（Vision-Language-Action）场景是一类特殊场景。在该类场景中，用户需要根据相机画面中的交通指示牌等视觉内容，完成多种类型的感知与决策任务，包括文本指令理解、违停车辆检测以及功能区合规性审查。

如何辨别 VLA 场景
------------------

- 通过 :meth:`metacar.SceneAPI.get_scene_static_data` 获取到的 :class:`~metacar.SceneStaticData` 中，:attr:`~metacar.SceneStaticData.vla_extension` 不为 ``None`` 即可判断为 VLA 场景。
- 与普通场景的主要差异如下：

  - :attr:`metacar.SceneStaticData.route` 和 :attr:`metacar.SceneStaticData.roads` 为空列表；
  - :attr:`metacar.SceneStatus.end_point` 为 ``None``；
  - :attr:`metacar.SubSceneInfo.start_point` 与 :attr:`metacar.SubSceneInfo.end_point` 为 ``None``。

任务类型与提交内容
------------------

VLA 场景包含三种不同的任务类型，用户需要根据当前场景的具体任务提交相应的结果。在每个子场景中，用户通过 :class:`metacar.VLAExtensionOutput` 提交结果。

1. 文本指令任务
~~~~~~~~~~~~~~~

在此类任务中，用户需要识别场景中的文字指令，并解析出关键信息。

**提交字段：** :attr:`~metacar.VLAExtensionOutput.text_info` (:class:`~metacar.VLATextOutput`)

- :attr:`~metacar.VLATextOutput.ocr_text`: 识别到的整句 OCR 指令文本（例如“100秒内去到B栋一单元门口”）。
- :attr:`~metacar.VLATextOutput.time_phrase`: 从指令中抽取的时间相关片段（例如“100秒内”）。
- :attr:`~metacar.VLATextOutput.location_phrase`: 从指令中抽取的地点相关片段（例如“B栋一单元门口”）。
- :attr:`~metacar.VLATextOutput.action_phrase`: 从指令中抽取的动作相关片段（例如“去到”）。

2. 停车区违规检测任务
~~~~~~~~~~~~~~~~~~~~~

在此类任务中，用户需要识别停车区域内的车辆，判断其是否位于限制区域，并上报违停车辆的贴纸编号。

**提交字段：** :attr:`~metacar.VLAExtensionOutput.parking_result` (:class:`~metacar.ParkingResult`)

- :attr:`~metacar.ParkingResult.violating_sticker_ids`: 检测到的违停车辆贴纸编号列表（例如 ``["B-01", "B-03"]``）。

3. 功能区合规检测任务
~~~~~~~~~~~~~~~~~~~~~

在此类任务中，用户需要结合规则文本与车辆贴纸类别，判断车辆是否合规，并上报违规信息。

**提交字段：** :attr:`~metacar.VLAExtensionOutput.function_zone_result` (:class:`~metacar.FunctionZoneResult`)

- :attr:`~metacar.FunctionZoneResult.violations`: 违规列表，包含多个 :class:`~metacar.FunctionZoneViolation` 对象。
- :class:`~metacar.FunctionZoneViolation` 包含：
    - :attr:`~metacar.FunctionZoneViolation.rule_code`: 违反的规则代码（例如 "R01"）。
    - :attr:`~metacar.FunctionZoneViolation.sticker_ids`: 违反该规则的车辆贴纸 ID 列表。

如何提交
--------

使用 :meth:`metacar.SceneAPI.set_vehicle_control` 发送车辆控制命令时，可将 :class:`metacar.VLAExtensionOutput` 通过参数 ``vla_extension`` 传入。

根据任务不同，只需填充 :class:`metacar.VLAExtensionOutput` 中对应的字段，其他字段保持为 ``None`` 即可。

**示例 1：提交文本指令结果**

.. code-block:: python

    from metacar import SceneAPI, VehicleControl, VLAExtensionOutput, VLATextOutput

    # ... 初始化代码 ...

    vla_payload = VLAExtensionOutput(
        text_info=VLATextOutput(
            ocr_text="100秒内去到B栋一单元门口",
            time_phrase="100秒内",
            location_phrase="B栋一单元门口",
            action_phrase="去到",
        )
    )
    api.set_vehicle_control(vc, vla_extension=vla_payload)

**示例 2：提交停车区违规结果**

.. code-block:: python

    from metacar import SceneAPI, VehicleControl, VLAExtensionOutput, ParkingResult

    # ... 初始化代码 ...

    vla_payload = VLAExtensionOutput(
        parking_result=ParkingResult(
            violating_sticker_ids=["B-01", "B-03"]
        )
    )
    api.set_vehicle_control(vc, vla_extension=vla_payload)

**示例 3：提交功能区合规结果**

.. code-block:: python

    from metacar import SceneAPI, VehicleControl, VLAExtensionOutput, FunctionZoneResult, FunctionZoneViolation

    # ... 初始化代码 ...

    vla_payload = VLAExtensionOutput(
        function_zone_result=FunctionZoneResult(
            violations=[
                FunctionZoneViolation(rule_code="R01", sticker_ids=["C-02"]),
                FunctionZoneViolation(rule_code="R02", sticker_ids=["C-01", "C-03"])
            ]
        )
    )
    api.set_vehicle_control(vc, vla_extension=vla_payload)

**说明：** 每个子场景仅需要提交一次 ``vla_extension``，同一子场景如多次提交，以最后一次提交为准。

相关模型
--------

VLA 相关数据模型定义见：

- :class:`metacar.VLAExtension`
- :class:`metacar.VLAExtensionOutput`
- :class:`metacar.VLATextOutput`
- :class:`metacar.ParkingResult`
- :class:`metacar.FunctionZoneResult`
- :class:`metacar.FunctionZoneViolation`
