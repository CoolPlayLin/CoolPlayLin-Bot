from api import *
from flask import Flask
from threading import Thread
from flask import request
import time
import psutil, os, random, pathlib, json
from requests import get

if not (pathlib.Path(__file__).parent / "Admin.json").exists():
    with open((pathlib.Path(__file__).parent / "Admin.json"), "w+", encoding="utf-8") as f:
        f.write(json.dumps({"Root": None, "Admin": []}))

Always_Task = []
Task = ToolAPI.TaskManager()
app = Flask(__name__)
Dates = ToolAPI.JsonAuto(None, "READ")

Server = NormalAPI.APIs("127.0.0.1:5700")

def Group_Msg(Group_id, User_id, Message:str):
        if Message == "[CQ:at,qq=391760560] Admin":
            if User_id != Dates['Root']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有Root权限，无法查看管理列表")))
            else:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "当前管理员列表\n{}".format(str(Dates['Admin'])))))
        elif '[CQ:at,qq=391760560] Add Admin ' in Message:
            if User_id != Dates['Root']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有Root权限，无法查看管理列表")))
            else:
                try:
                    Dates['Admin'].append(int(Message.replace("[CQ:at,qq=391760560] Add Admin ", "")))
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "保存成功\n{}".format(str(Dates['Admin'])))))
                except BaseException as e:
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "错误：\n{}".format(e))))
        elif '[CQ:at,qq=391760560] Del Admin ' in Message:
            if User_id != Dates['Root']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有Root权限，无法查看管理列表")))
            else:
                try:
                    _ = int(Message.replace("[CQ:at,qq=391760560] Del Admin ", ""))
                    if _ in Dates['Admin']:
                        Dates['Admin'].remove(_)
                        Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "保存成功\n{}".format(str(Dates['Admin'])))))
                    else:
                        Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "此用户不在Admin中")))
                except BaseException as e:
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "错误：\n{}".format(e))))
        elif '[CQ:at,qq=391760560] Status' in Message:
            Info = psutil.virtual_memory()
            Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, f"状态信息\n正在排队的任务数 {len(Task.Perform_QueuingTask)}\n正在运行的任务数 {len(Task.Perform_RunningTask)}")))
        elif Message in ['[CQ:at,qq=391760560] 获取一言', '[CQ:at,qq=391760560] 一言', '[CQ:at,qq=391760560] 文案']:
            Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, (get("https://v1.hitokoto.cn/").json()['hitokoto']))))
        elif '[CQ:at,qq=391760560] 冷静' in Message:
            if not User_id in Dates['Admin']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有Root权限，无法查看管理列表")))
            else:
                try:
                    User = int(Message.replace("[CQ:at,qq=391760560] 冷静", ""))
                    Task.AddTask(Thread(target=Server.Set_Group_Ban, args=(Group_id, User, 60)))
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "已尝试冷静此人")))
                except BaseException as e:
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "错误：\n{}".format(e))))
        elif '[CQ:at,qq=391760560] 禁言大转盘' in Message:
            if not User_id in Dates['Admin']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有Root权限，无法查看管理列表")))
            else:
                try:
                    User = int(Message.replace("[CQ:at,qq=391760560] 禁言大转盘", ""))
                    Min = random.randint(1, 60)
                    Task.AddTask(Thread(target=Server.Set_Group_Ban, args=(Group_id, User, 60*Min)))
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "恭喜获得{}分钟".format(Min))))
                except BaseException as e:
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "错误：\n{}".format(e))))
        elif '[CQ:at,qq=391760560]' in Message:
            Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "干啥子")))

@app.route("/commit", methods=['POST'])
def Main():
    # if request.get_json("post_type") == "message":
    #     if request.get_json("message_type") == "group":
    if request.json["post_type"] == "message":
        if request.json['message_type'] == 'group':
            Group_Msg(request.json['group_id'], request.json['user_id'], request.json['raw_message'])
    return 'ok'
def DateAutoSave():
    global Dates

    while True:
        time.sleep(1)
        ToolAPI.JsonAuto(Dates, "WRITE")


Always_Task.append(Thread(target=app.run, kwargs=dict(host='0.0.0.0' ,port=5120)))
Always_Task.append(Thread(target=Task))
Always_Task.append(Thread(target=DateAutoSave))

if __name__ == '__main__':
    for each in Always_Task:
        each.start()
    for each in Always_Task:
        each.join()