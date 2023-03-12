"""
CoolPlayLin-Bot启动器
"""

print("正在初始化内核组件，请稍等")
from api import task, app, logger, Dates
from threading import Thread
from time import sleep
print("内核主机初始化成功完成")

# 建立常驻线程列表
always_task:list[Thread] = []
always_task.append(Thread(target=task.run, name="TaskManager"))
always_task.append(Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=Dates["Server"]['AcceptPort']), name="FlaskServer"))

if __name__ == '__main__':
    # 启动所有任务
    for each in always_task:
        task.AddTask(Thread(target=logger.event, kwargs=dict(msg="正在请求启动{}".format(each.name))), 0)
        each.start()
        task.AddTask(Thread(target=logger.event, kwargs=dict(msg="{}已成功发送启动请求".format(each.name))), 0)

    # 看门狗
    while True:
        for each in always_task:
            if not each.is_alive():
                tasks = (Thread(target=task.run, name="TaskManager"), Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=Dates["Server"]['AcceptPort']), name="FlaskServer"))
                task.AddTask(Thread(target=logger.warn, kwargs=dict(msg="{}意外退出，正在尝试重新启动".format(each.name))))
                Index = always_task.index(each)
                always_task[Index] = tasks[Index]
                always_task[Index].start()
        sleep(5)
