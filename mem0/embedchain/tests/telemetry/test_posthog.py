import logging  # 这行代码引入了一个叫logging的库，它用于记录程序运行时的信息。
import os       # 引入os库，这个库可以让程序和操作系统进行交互。

from embedchain.telemetry.posthog import AnonymousTelemetry  # 这行代码从embedchain库的telemetry.posthog模块中导入了AnonymousTelemetry类。

class TestAnonymousTelemetry:  # 定义一个测试类，用于检查AnonymousTelemetry类是否按预期工作。
    def test_init(self, mocker):  # 这个方法测试AnonymousTelemetry的初始化过程。
        # Enable telemetry specifically for this test  # 这个注释说明接下来的操作是为了特定的测试启用遥测功能。
        os.environ["EC_TELEMETRY"] = "true"  # 设置环境变量EC_TELEMETRY为"true"，告诉程序允许收集遥测数据。
        mock_posthog = mocker.patch("embedchain.telemetry.posthog.Posthog")  # 使用mocker创建一个模拟的Posthog对象，用于测试而不真正发送数据。
        telemetry = AnonymousTelemetry()  # 创建一个AnonymousTelemetry实例。
        assert telemetry.project_api_key == "phc_PHQDA5KwztijnSojsxJ2c1DuJd52QCzJzT2xnSGvjN2"  # 检查项目API密钥是否正确。
        assert telemetry.host == "https://app.posthog.com"  # 检查主机地址是否正确。
        assert telemetry.enabled is True  # 确认遥测功能已启用。
        assert telemetry.user_id  # 确认用户ID已被生成。
        mock_posthog.assert_called_once_with(project_api_key=telemetry.project_api_key, host=telemetry.host)  # 确认模拟的Posthog对象被正确调用。

    def test_init_with_disabled_telemetry(self, mocker):  # 测试当遥测功能被禁用时的初始化过程。
        mocker.patch("embedchain.telemetry.posthog.Posthog")  # 再次使用mocker模拟Posthog对象。
        telemetry = AnonymousTelemetry()  # 创建一个新的AnonymousTelemetry实例。
        assert telemetry.enabled is False  # 确认遥测功能未启用。
        assert telemetry.posthog.disabled is True  # 确认Posthog对象的disabled属性为True，表示不会发送数据。

    def test_get_user_id(self, mocker, tmpdir):  # 测试获取用户ID的方法。
        mock_uuid = mocker.patch("embedchain.telemetry.posthog.uuid.uuid4")  # 模拟uuid库的uuid4函数，用于生成用户ID。
        mock_uuid.return_value = "unique_user_id"  # 设置模拟的uuid4函数返回一个固定的用户ID。
        config_file = tmpdir.join("config.json")  # 在临时目录中创建一个配置文件。
        mocker.patch("embedchain.telemetry.posthog.CONFIG_FILE", str(config_file))  # 设置配置文件的位置。
        telemetry = AnonymousTelemetry()  # 创建一个AnonymousTelemetry实例。
        user_id = telemetry._get_user_id()  # 调用获取用户ID的方法。
        assert user_id == "unique_user_id"  # 确认返回的用户ID与预设的一致。
        assert config_file.read() == '{"user_id": "unique_user_id"}'  # 确认配置文件中存储的用户ID正确。

    def test_capture(self, mocker):  # 测试捕获事件并发送遥测数据的方法。
        os.environ["EC_TELEMETRY"] = "true"  # 启用遥测功能。
        mock_posthog = mocker.patch("embedchain.telemetry.posthog.Posthog")  # 模拟Posthog对象。
        telemetry = AnonymousTelemetry()  # 创建一个AnonymousTelemetry实例。
        event_name = "test_event"  # 设定事件名称。
        properties = {"key": "value"}  # 设定事件属性。
        telemetry.capture(event_name, properties)  # 调用capture方法发送事件数据。
        mock_posthog.assert_called_once_with(  # 确认模拟的Posthog对象被正确调用。
            project_api_key=telemetry.project_api_key,
            host=telemetry.host,
        )
        mock_posthog.return_value.capture.assert_called_once_with(  # 确认模拟的Posthog对象的capture方法被正确调用。
            telemetry.user_id,
            event_name,
            properties,
        )

    def test_capture_with_exception(self, mocker, caplog):  # 测试在发送遥测数据时遇到异常的情况。
        os.environ["EC_TELEMETRY"] = "true"  # 启用遥测功能。
        mock_posthog = mocker.patch("embedchain.telemetry.posthog.Posthog")  # 模拟Posthog对象。
        mock_posthog.return_value.capture.side_effect = Exception("Test Exception")  # 设置模拟的Posthog对象在调用capture方法时抛出异常。
        telemetry = AnonymousTelemetry()  # 创建一个AnonymousTelemetry实例。
        event_name = "test_event"  # 设定事件名称。
        properties = {"key": "value"}  # 设定事件属性。
        with caplog.at_level(logging.ERROR):  # 设置日志级别为ERROR，以便捕获错误信息。
            telemetry.capture(event_name, properties)  # 尝试发送遥测数据。
        assert "Failed to send telemetry event" in caplog.text  # 确认日志中包含了发送遥测数据失败的信息。
        caplog.clear()  # 清空日志，以便后续测试。

