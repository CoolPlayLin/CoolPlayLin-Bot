"""
CoolPlayLin-Bot Docker 启动器
"""

print("正在初始化内核组件，请稍等")
from api import task, app, logger, Dates
from threading import Thread
from time import sleep
import pathlib, os, yaml, json, random
print("内核主机初始化成功完成")

# 寻找服务器
cqhttpPath = pathlib.Path(__file__).parents[0] / "server"
if cqhttpPath.exists():
    _ = [each for each in [cqhttpPath / pathlib.Path(e) for e in os.listdir(cqhttpPath)] if each.suffix in [".exe", ""] and each.is_file()]
    if len(_) == 1:
        cqhttpPath = _[0]
    else:
        error = Exception("没有找到 Server 目录中找到可执行文件")
        raise error
else:
    error = FileNotFoundError("没有找到 Server 目录")
    raise error

# 寻找配置文件
cqhttpPath_cfg = pathlib.Path(__file__).parents[0] / "server"
if cqhttpPath_cfg.exists():
    _ = [each for each in [cqhttpPath_cfg / pathlib.Path(e) for e in os.listdir(cqhttpPath_cfg)] if each.suffix in [".yml"] and each.is_file()]
    print(_)
    if len(_) == 1:
        cqhttpPath_cfg = _[0]
        with open(cqhttpPath_cfg, "rt", encoding="utf-8") as f:
            yml = [each for each in yaml.load_all(f.read(), yaml.Loader)][0]
        if yml["account"]["password"] == "":
            if os.getenv("ACCOUNT") == None or os.getenv("PASSWORD") == None:
                error = RuntimeError("环境变量中没有 ACCOUNT 与 PASSWORD 的值")
                raise error
            else:
                yml["account"]["uid"] = int(os.getenv("ACCOUNT"))
                yml["account"]["password"] = os.getenv("PASSWORD")
            with open(cqhttpPath_cfg, "w+", encoding="utf-8") as f:
                f.write(yaml.dump(yml))
    else:
        error = Exception("没有找到 Server 目录中找到可执行文件")
        raise error
else:
    error = FileNotFoundError("没有找到 Server 目录")
    raise error

# 建立常驻线程列表
always_task:list[Thread] = []
always_task.append(Thread(target=task.run, name="TaskManager"))
always_task.append(Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=Dates["Server"]['AcceptPort']), name="FlaskServer"))
always_task.append(Thread(target=os.system, kwargs=dict(command=f"cd {cqhttpPath.parents[0]} && {cqhttpPath}")))

if __name__ == '__main__':
    # 启动所有任务
    for t in always_task:
        logger.event(msg="正在启用守护线程{}".format(t.name))
        t.daemon = True
        logger.event(msg="正在请求启动{}".format(t.name))
        t.start()
        logger.event(msg="{}已成功发送启动请求".format(t.name))

    # 看门狗
    Times = 0
    while True:
        for each in always_task:
            if not each.is_alive():
                tasks = (Thread(target=task.run, name="TaskManager"), Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=Dates["Server"]['AcceptPort']), name="FlaskServer"), Thread(target=os.system, kwargs=dict(command=f"cd {cqhttpPath.parents[0]} && {cqhttpPath}"), name="Server"))
                if each == task[-1]:
                    DevicesPath = pathlib.Path(__file__).parents[0] / "server/device.json"
                    if DevicesPath.exists():
                        with open(DevicesPath, "rt", encoding="utf-8") as f:
                            cfg = json.loads(f.read())
                        cfg["protocol"] = random.randint(1, 9)
                        with open(DevicesPath, "w+", encoding="utf-8") as f:
                            cfg = json.dumps(cfg)
                    else:
                        error = Exception("服务端无法正常运行")
                logger.warn(msg="{}意外退出，正在尝试重新启动".format(each.name))
                Index = always_task.index(each)
                always_task[Index] = tasks[Index]
                always_task[Index].start()
                Times += 1
        sleep(5)
        if Times >= 10:
            logger.event(msg="{}线程重启次数过多".format(t.name))
            quit()