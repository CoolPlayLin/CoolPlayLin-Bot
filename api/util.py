from pathlib import Path

from threading import Thread, Lock
import json, os
from .typings import TaskManagerExit

__all__ = ("TaskManager", "Logger")

DefaultJSON = {"Root": None, "Admin": [], "BotQQ": None,"NotAllowUser":[], "BadWords": [], "AcceptPort": 5120, "PostIP": "127.0.0.1:5700", "@Me": None, "AdminGroup": []}

class TaskManager:
    __slots__ = ("Perform_QueuingTask", "Perform_RunningTask", "Status", "TaskLimit")
    def __init__(self, TaskLimit:int) -> None:
        self.Perform_QueuingTask:list[Thread] = []
        self.Perform_RunningTask:list[Thread] = []
        self.TaskLimit = TaskLimit
        self.Status = True
    
    def run(self):
        while self.Status:
            try:
                if len(self.Perform_QueuingTask)+len(self.Perform_RunningTask) > 0:
                    for each in self.Perform_QueuingTask:
                        self.Perform_RunningTask = [t for t in self.Perform_RunningTask if t.is_alive()]
                        if not isinstance(each, Thread):
                            self.Perform_QueuingTask.remove(each)
                            continue
                        elif self.TaskLimit:
                            if len(self.Perform_RunningTask) >= self.TaskLimit:
                                continue
                        self.Perform_RunningTask.append(each)
                        self.Perform_QueuingTask.remove(each)
                        self.Perform_RunningTask[-1].start()
            except BaseException as e:
                break
        if self.Status:
            raise TaskManagerExit
    def AddTask(self, Task:Thread) -> bool:
        if isinstance(Task, Thread):
            self.Perform_QueuingTask.append(Task)
            return True
        else:
            return False

FileLock = Lock()

def JsonAuto(Json:dict, Action:str, PATH:Path) -> bool|dict:
    if not PATH.exists():
        with FileLock:
            with open(PATH, "w+", encoding="utf-8") as f:
                f.write(json.dumps(DefaultJSON))
    if Action == "WRITE":
        try:
            with FileLock:
                with open(PATH, "w+", encoding="utf-8") as file:
                    file.write(json.dumps(Json))
                return True
        except:
            return False
    elif Action == "READ":
        try:
            with FileLock:
                with open(PATH, "rt", encoding="utf-8") as file:
                    Res:dict = json.loads(file.read())
            if Res.keys() == DefaultJSON.keys():
                return Res
            else:
                raise Exception
        except:
            os.remove(PATH)
            return DefaultJSON
    else:
        return False

def BadWord(Message:str, BadWordList:list) -> bool:
    if len([each for each in BadWordList if each in Message]) > 0:
        return True
    else:
        return False