__all__ = ("BotError", "TaskManagerExit", "APIError")

from abc import ABCMeta, abstractclassmethod
class BotError(Exception, metaclass=ABCMeta):
    @abstractclassmethod
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        try:
            self.add_note("你可以提交Issues来反馈这个问题")
        except:
            pass

class TaskManagerExit(BotError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class APIError(BotError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)