"""
CoolPlayLin-Bot 运行测试
"""
print("{}正在初始化程序{}".format("="*5, "="*5))
from api import task, app, logger, Dates
from api import typing
from threading import Thread
from time import sleep
print("{}程序初始化完成{}".format("="*5, "="*5))

always_task:list[Thread] = []
always_task.append(Thread(target=task.run, name="TaskManager"))
always_task.append(Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=Dates["Server"]['AcceptPort']), name="FlaskServer"))

if __name__ == "__main__":
    print("{}开始测试{}".format("="*5, "="*5))
    for t in always_task:
        t.daemon = True
        t.start()
    sleep(60)
    for t in always_task:
        if not t.is_alive():
            error = typing.CIError("有进程意外退出")
            raise error
    print("{}测试完成，程序无错误{}".format("="*5, "="*5))
    quit(0)