__all__ = ("BotError", "TaskManagerExit", "APIError")

from abc import ABCMeta, abstractmethod
class BotError(Exception, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args: object) -> None:
        try:
            super().add_note("你可以提交Issues来反馈这个问题")
        except:
            pass

class TaskManagerExit(BotError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class APIError(BotError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CIError(Exception):
    pass