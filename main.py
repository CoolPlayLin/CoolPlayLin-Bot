"""
CoolPlayLin-Bot启动器
"""
from api import *
from time import sleep

# 建立常驻线程列表
Always_Task:list[Thread] = []
Always_Task.append(Thread(target=Task.run, name="TaskManager"))
Always_Task.append(Thread(target=app.run, kwargs=dict(host='0.0.0.0' ,port=Dates['AcceptPort']), name="FlaskServer"))

if __name__ == '__main__':
    # 启动所有任务
    for each in Always_Task:
        Task.AddTask(Thread(target=logger.event, kwargs=dict(msg="正在请求启动{}".format(each.name))))
        each.start()
        Task.AddTask(Thread(target=logger.event, kwargs=dict(msg="{}已成功发送启动请求".format(each.name))))

    # 看门狗
    while True:
        TaskList:tuple[Thread] = (Thread(target=Task.run, name="TaskManager"), Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=Dates['AcceptPort']), name="FlaskServer"))
        for each in Always_Task:
            if not each.is_alive():
                Task.AddTask(Thread(target=logger.warn, kwargs=dict(msg="{}意外退出，正在尝试重新启动".format(each.name))))
                Index = Always_Task.index(each)
                Always_Task[Index] = TaskList[Index]
                Always_Task[Index].start()
        sleep(5)