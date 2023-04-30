from platform import python_version_tuple

_ = [int(each) for each in python_version_tuple()]
NOTES = _[0] >= 3 and _[1] >= 11


class BotError(Exception):
    """
    本项目所有自定义错误的基类
    """

    def __init__(self, *args: object) -> None:
        _ = [int(each) for each in python_version_tuple()]
        if NOTES:
            super().add_note("你可以提交issues来反馈这个问题")
        super().__init__(*args)


class TaskManagerExit(BotError):
    pass


class APIError(BotError):
    pass


class CIError(BotError):
    pass


class InitializationError(BotError):
    def __init__(self, *args: object) -> None:
        if NOTES:
            super().add_note("数据初始化错误，可能是数据遭到损坏或者意外丢失")
        super().__init__(*args)


class InternalDataProtect(BotError):
    def __init__(self, *args: object) -> None:
        if NOTES:
            super().add_note("内部数据收到保护，当前操作不被允许")
        super().__init__(*args)


class ActionNotAllowed(InternalDataProtect):
    pass
