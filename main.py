from api import *
from flask import Flask, render_template, request
from time import sleep
from threading import Thread

# 加载必要数据
app = Flask(__name__)
PATH = pathlib.Path(__file__).parent / "database" / "config.json"
Always_Task:list[Thread] = []
Task = ToolAPI.TaskManager(0)
Dates = ToolAPI.JsonAuto(None, "READ", PATH)
Server = NormalAPI.APIs(Dates['PostIP'])

# POST数据路由
@app.route("/commit", methods=['POST'])
def Main():
    if request.json["post_type"] == "message":
        if request.json['message_type'] == 'group':
            Task.AddTask(Thread(target=logger.event, kwargs=dict(msg="收到{}群{}发送的请求 {}".format(request.json['group_id'], request.json['user_id'], request.json['raw_message']))))
            Task.AddTask(Thread(target=Group_Msg, args=(Server, request.json['group_id'], request.json['user_id'], request.json['raw_message'], request.json['message_id'], Dates)))
        elif request.json['message_type'] == 'private':
            Task.AddTask(Thread(target=Server.Send_Private_Msg, args=(request.json['user_id'], "我暂时无法为你服务~")))
    
    # 更新数据
    Task.AddTask(Thread(target=retention, args=(Server, Dates, PATH)))
    return 'ok'

# Web页面路由
@app.route("/", methods=['GET', "POST"])
def Web():
    if "log" in dict(request.args):
        return logger.html()
    else:
        return render_template("index.html")

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