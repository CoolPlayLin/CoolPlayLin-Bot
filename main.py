from api import *
from flask import Flask, render_template
from threading import Thread
from flask import request
from time import sleep
import pathlib
PATH = pathlib.Path(__file__).parent / "Config.json"
from requests import get

# 加载必要数据
Always_Task:list[Thread] = []
Task = ToolAPI.TaskManager(0)
app = Flask(__name__)
Dates = ToolAPI.JsonAuto(None, "READ", PATH)
Server = NormalAPI.APIs(Dates['PostIP'])

# POST数据路由
@app.route("/commit", methods=['POST'])
def Main():
    if request.json["post_type"] == "message":
        if request.json['message_type'] == 'group':
            Task.AddTask(Thread(target=Group_Msg, args=(Server, request.json['group_id'], request.json['user_id'], request.json['raw_message'], request.json['message_id'], Dates)))
            Task.AddTask(Thread(target=AutoSave, args=(Task, Server, Dates, PATH)))
    return 'ok'

# Web页面路由
@app.route("/", methods=['GET'])
def Web():
    return render_template("index.html")

Always_Task.append(Thread(target=Task.run, name="TaskManager"))
Always_Task.append(Thread(target=app.run, kwargs=dict(host='0.0.0.0' ,port=Dates['AcceptPort']), name="FlaskServer"))

if __name__ == '__main__':
    # 启动所有任务
    for each in Always_Task:
        each.start()

    # 看门狗
    while True:
        TaskList:tuple[Thread] = (Thread(target=Task.run, name="TaskManager"), Thread(target=app.run, kwargs=dict(host='0.0.0.0' ,port=Dates['AcceptPort']), name="FlaskServer"))
        for each in Always_Task:
            if not each.is_alive():
                print("看门狗: 部分进程意外退出，正在尝试重新启动")
                Index = Always_Task.index(each)
                Always_Task[Index] = TaskList[Index]
                Always_Task[Index].start()
        sleep(5)