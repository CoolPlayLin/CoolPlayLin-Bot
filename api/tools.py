from threading import Thread
import time
import json
from pathlib import Path

__all__ = ("TaskManager", "Logger")

DefaultJSON = {"Root": None, "Admin": [], "BotQQ": None,"NotAllowUser":[], "BadWords": [], "AcceptPort": 5120, "PostIP": "127.0.0.1:5700", "@Me": None, "AdminGroup": []}
class TaskManager:
    __slots__ = ("Perform_QueuingTask", "Perform_RunningTask")
    def __init__(self) -> None:
        self.Perform_QueuingTask:list[Thread] = []
        self.Perform_RunningTask:list[Thread] = []
    
    def __call__(self):
        while True:
            if len(self.Perform_QueuingTask)+len(self.Perform_RunningTask) > 0:
                for each in self.Perform_QueuingTask:
                    if not isinstance(each, Thread):
                        self.Perform_QueuingTask.remove(each)
                for each in self.Perform_QueuingTask:
                    self.Perform_RunningTask.append(each)
                    self.Perform_QueuingTask.remove(each)
                for each in self.Perform_RunningTask:
                    each.start()
                for each in self.Perform_RunningTask:
                    each.join()
                    self.Perform_RunningTask.remove(each)
    def AddTask(self, Task:Thread) -> bool:
        if isinstance(Task, Thread):
            self.Perform_QueuingTask.append(Task)
            return True
        else:
            return False

def Logger(Message:str):
    with open("Run.log", "a", encoding='utf-8') as f:
        f.write("{} Message".format(time.strftime("%H:%M:%S")))

def JsonAuto(Json:dict, Action:str, PATH:Path) -> bool|dict:
    if not PATH.exists():
        with open(PATH, "w+", encoding="utf-8") as f:
            f.write(json.dumps(DefaultJSON))
    if Action == "WRITE":
        try:
            with open(PATH, "w+", encoding="utf-8") as file:
                file.write(json.dumps(Json))
            return True
        except:
            return False
    elif Action == "READ":
        try:
            with open(PATH, "rt", encoding="utf-8") as file:
                return(json.loads(file.read()))
        except:
            return False
    else:
        return False

def BadWord(Message:str, BadWordList:list) -> bool:
    if len([each for each in BadWordList if each in Message]) > 0:
        return True
    else:
        return False