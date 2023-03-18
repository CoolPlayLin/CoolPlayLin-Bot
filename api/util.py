"""
CoolPlayLin-Bot工具类
"""

from pathlib import Path
from threading import Thread, Lock
import json, time, requests, pickle, random
from . import typing as ts

class TaskManager:
    __slots__ = ("task", "status", "task_limit", "died_task")
    def __init__(self, task_limit:int=0, number:int=1) -> None:
        self.task:dict[str, list[list[Thread], list[Thread]]] = {}
        for i in range(number):
            self.task[str(i)]= [[], []]
        self.task_limit = int(task_limit)
        self.died_task:list[Thread] = []
        self.status = True
    def run(self) -> bool:
        try:
            while self.status:
                for id in self.task:
                    self.died_task.extend([t for t in self.task[id][1] if not t.is_alive()])
                    self.task[id][1] = [t for t in self.task[id][1] if t.is_alive()]
                    for t in self.task[id][0]:
                        if not isinstance(t, Thread):
                            self.task[id][0].remove(t)
                            continue
                        elif self.task_limit:
                            if len(self.task[id][1]) >= self.task_limit:
                                continue
                        self.task[id][1].append(t)
                        t.start()
                        self.task[id][0].remove(t)
        except BaseException as e:
            error = ts.TaskManagerExit("任务管理器异常退出, 原因：{}".format(e))
            raise error
        return True
    def AddTask(self, Task:Thread, id:int) -> bool:
        if isinstance(Task, Thread) and str(id) in self.task:
            self.task[str(id)][0].append(Task)
            return True
        else:
            return False    
    def __delattr__(self, name:str) -> None:
        error = ts.ActionNotAllowed("不允许删除任何内部数据, 包括 {}".format(name))
        raise error
    def stop(self):
        self.status = False

def jsonauto(Json: dict, Action: str, PATH: Path):
    FileLock = Lock()
    with FileLock:
        if PATH.stem+PATH.suffix == "config.json":
            DefaultJSON = {"Root": None, "Admin": [], "BotQQ": None,"NotAllowUser":[], "BadWords": [], "@Me": None, "AdminGroup": [], "Server":{"AcceptPort": 5120, "PostIP": "127.0.0.1:5700", "AccessKey": None}}
            if not PATH.exists():
                with open(PATH, "w+", encoding="utf-8") as f:
                    f.write(json.dumps(DefaultJSON))
            if Action == "WRITE":
                with open(PATH, "w+", encoding="utf-8") as file:
                    file.write(json.dumps(Json))
                return True
            elif Action == "READ":
                with open(PATH, "rt", encoding="utf-8") as file:
                    Res: dict = json.load(file)
                if set(Res.keys()) != set(DefaultJSON.keys()):
                    Res.update({key: DefaultJSON[key] for key in DefaultJSON.keys() if key not in Res})
                return Res
            elif Action == "TEXT":
                with open(PATH, "rt", encoding="utf-8") as file:
                    Res: dict = json.load(file)
                return Res
            else:
                return False
        elif PATH.stem+PATH.suffix == "API.json":
            if not PATH.exists():
                urls = ("https://cdn.jsdelivr.net/gh/CoolPlayLin/CoolPlayLin-Bot@main/database/API.json", "https://fastly.jsdelivr.net/gh/CoolPlayLin/CoolPlayLin-Bot@main/database/API.json", "https://gitee.com/coolplaylin/CoolPlayLin-Bot/raw/main/database/API.json")
                for each in urls:
                    try:
                        with open(PATH, "w+", encoding="utf-8") as f:
                            f.write(requests.get(url=each, verify=False).text)
                            break
                    except:
                        continue
            with open(PATH, "rt", encoding="utf-8") as file:
                Res = json.loads(file.read())
            return Res
        elif PATH.stem+PATH.suffix == "db.dat":
            if not PATH.exists():
                urls = ("https://cdn.jsdelivr.net/gh/CoolPlayLin/CoolPlayLin-Bot@main/database/db.json", "https://fastly.jsdelivr.net/gh/CoolPlayLin/CoolPlayLin-Bot@main/database/db.json", "https://gitee.com/coolplaylin/CoolPlayLin-Bot/raw/main/database/db.json")
                source = Path(__file__).parent.parent / "database" / "db.json"
                if source.exists():
                    with open(source, "rt", encoding="utf-8") as f:
                        res = json.loads(f.read())
                        with open(PATH, "wb+") as f:
                            f.write(pickle.dumps(res))
                else:
                    for each in urls:
                        try:
                            with open(PATH, "wb+") as f:
                                res = requests.get(url=each, verify=False).json()
                                f.write(pickle.dumps(res))
                                break
                        except:
                            continue
            with open(PATH, "rb") as f:
                return pickle.loads(f.read())
        else:
            error = ts.ActionNotAllowed("不支持此文件的读写")
            raise error

def badwords(Message:str, BadWordList:list) -> bool:
    if len([each for each in BadWordList if each in Message]) > 0:
        return True
    else:
        return False

class Logger:
    __slots__ = ("PATH", "FileLock")
    def __init__(self, PATH:Path) -> None:
        if not isinstance(PATH, Path):
            raise TypeError
        elif not PATH.is_file:
            raise TypeError
        elif not PATH.exists():
            with open(PATH, "w+", encoding="utf-8") as f:
                f.close()
        else:
            with open(PATH, "a", encoding="utf-8") as f:
                f.write("\n=====分界线=====\n\n")
        self.PATH = PATH
        self.FileLock = Lock()
    def error(self, msg:str) -> bool:
        with self.FileLock:
            with open(self.PATH, "a", encoding="utf-8") as f:
                f.write("{} Error: {}\n".format(time.strftime(r"%Y-%m-%d %H:%M:%S"), msg))
                return True
    def event(self, msg:str) -> bool:
        with self.FileLock:
            with open(self.PATH, "a", encoding="utf-8") as f:
                f.write("{} Event: {}\n".format(time.strftime(r"%Y-%m-%d %H:%M:%S"), msg))
                return True
    def warn(self, msg:str) -> bool:
        with self.FileLock:
            with open(self.PATH, "a", encoding="utf-8") as f:
                f.write("{} Warning: {}\n".format(time.strftime(r"%Y-%m-%d %H:%M:%S"), msg))
                return True
    def read(self) -> str:
        with self.FileLock:
            with open(self.PATH, "rt", encoding="utf-8") as f:
                return f.read()
    def html(self) -> str:
        with self.FileLock:
            with open(self.PATH, "rt", encoding="utf-8") as f:
                res = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="icon" href="/static/favicon.ico" type="image/x-icon"><link rel="stylesheet" href="/static/mdui.min.css"><script src="/static/mdui.min.js"></script><title>Logs</title></head><body>{}</body></html>""".format(f.read().replace("\n", "<br>"))
                return res

def clean_up(chore:str ,clean:list) -> str:
    for each in clean:
        chore = chore.replace(each, "")
    return chore

def cut_str(chore:str, part:int) -> list:
    return [chore[i:i+part] for i in range(0,len(chore),part)]

class Cache:
    def __init__(self, PATH:Path) -> None:
        self.PATH = PATH

    def write_res(self, objects:requests.Response, prefix:str) -> Path:
        _path = self.PATH / "{}{}.jpg".format(prefix ,random.randint(1, 100000000))
        while _path.exists():
            _path = self.PATH / "{}{}.jpg".format(prefix ,random.randint(1, 100000000))
        with open(_path, "wb") as f:
            f.write(objects.content)
        return _path
    def write_url(self, url:str, prefix:str, verify:bool=False) -> Path:
        _path = self.PATH / "{}{}.jpg".format(prefix ,random.randint(1, 100000000))
        while _path.exists():
            _path = self.PATH / "{}{}.jpg".format(prefix ,random.randint(1, 100000000))
        res = requests.get(url, verify=verify)
        with open(_path, "wb") as f:
            f.write(res.content)
        return _path
    def save_text(self, text:str, suffix:str, prefix:str="") -> Path:
        _path = self.PATH / "{}{}.{}".format(prefix ,random.randint(1, 100000000), suffix)
        while _path.exists():
            _path = self.PATH / "{}{}.{}".format(prefix ,random.randint(1, 100000000), suffix)
        with open(_path, "wt+", encoding="utf-8") as f:
            f.write(text)
        return _path
    def get_file_name(self, suffix:str, prefix:str="") -> Path:
        _path = self.PATH / "{}{}.{}".format(prefix ,random.randint(1, 100000000), suffix)
        while _path.exists():
            _path = self.PATH / "{}{}.{}".format(prefix ,random.randint(1, 100000000), suffix)
        return _path