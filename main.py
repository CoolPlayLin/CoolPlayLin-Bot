from api import *
from flask import Flask
from threading import Thread
from flask import request
import time
import random, pathlib, json
from requests import get

if not (pathlib.Path(__file__).parent / "Admin.json").exists():
    with open((pathlib.Path(__file__).parent / "Admin.json"), "w+", encoding="utf-8") as f:
        f.write(json.dumps({"Root": None,"Admin": [],"NotAllowUser":[], "BadWords": [], "AcceptPort": 5120, "PostIP": "127.0.0.1:5700"}))

Always_Task = []
Task = ToolAPI.TaskManager()
app = Flask(__name__)
Dates = ToolAPI.JsonAuto(None, "READ")

Server = NormalAPI.APIs(Dates['PostIP'])

def Group_Msg(Group_id:int, User_id:int, Message:str, Message_Id:int) -> None:
        if User_id in Dates['NotAllowUser']:
            Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, '管理员不允许你使用')))
            return
        elif ToolAPI.BadWord(request.json['raw_message'], Dates['BadWords']):
                Task.AddTask(Thread(target=Server.Delete_Msg, kwargs=dict(message_id=Message_Id)))
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "检测到敏感内容, 已尝试撤回")))
                return
        if Message in ["[CQ:at,qq=391760560] "+each for each in ["menu", "Menu", "MENU", "菜单","功能", "功能列表"]]:
            Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "Hello，我是由CoolPlayLin开发并维护的开源QQ机器人，采用GPLv3许可证，项目直达 -> https://github.com/CoolPlayLin/CoolPlayLin-Bot\n我目前的功能\n1. 一言：获取一言文案")))
        elif "[CQ:at,qq=391760560] Refuse " in Message:
            if not User_id in Dates['Admin']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有Admin权限，无法查看管理列表")))
            else:
                try:
                    User = int(Message.replace("[CQ:at,qq=391760560] Refuse ", ""))
                    if User != Dates['Root']:
                        Dates['NotAllowUser'].append(User)
                        Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, '已将此用户添加到拒绝列表\n{}'.format(Dates['NotAllowUser']))))
                    else:
                        Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, '不允许将Root用户添加到拒绝列表')))
                except BaseException as e:
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "错误：\n{}".format(e))))
        elif "[CQ:at,qq=391760560] Accept " in Message:
            if not User_id in Dates['Admin']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有管理权限，无法查看管理列表")))
            else:
                try:
                    User = int(Message.replace("[CQ:at,qq=391760560] Accept ", ""))
                    if User in Dates['NotAllowUser']:
                        Dates['NotAllowUser'].remove(User)
                        Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, '已将此用户从拒绝列表移除\n{}'.format(Dates['NotAllowUser']))))
                    else:
                        Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, '此用户不在拒绝列表中')))
                except BaseException as e:
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "错误：\n{}".format(e))))
        elif "[CQ:at,qq=391760560] RefuseList" in Message:
            Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, '拒绝用户列表\n{}'.format(Dates['NotAllowUser']))))
        elif "[CQ:at,qq=391760560] Set Root" in Message:
            if Dates['Root'] == None:
                Dates['Root'] = User_id
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, 'Root成功设置为{}'.format(str(User_id)))))
            else:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, 'Root用户已设置，请勿重复设置')))
        elif Message == "[CQ:at,qq=391760560] Admin":
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
            Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, f"状态信息\n正在排队的任务数 {len(Task.Perform_QueuingTask)}\n正在运行的任务数 {len(Task.Perform_RunningTask)}")))
        elif Message in ['[CQ:at,qq=391760560] 获取一言', '[CQ:at,qq=391760560] 一言', '[CQ:at,qq=391760560] 文案']:
            Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, (get("https://v1.hitokoto.cn/").json()['hitokoto']))))
        elif '[CQ:at,qq=391760560] 冷静' in Message:
            if not User_id in Dates['Admin']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有Admin权限，无法查看管理列表")))
            else:
                try:
                    User = int(Message.replace("[CQ:at,qq=391760560] 冷静", ""))
                    Task.AddTask(Thread(target=Server.Set_Group_Ban, args=(Group_id, User, 60)))
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "已尝试冷静此人")))
                except BaseException as e:
                    Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "错误：\n{}".format(e))))
        elif '[CQ:at,qq=391760560] 禁言大转盘' in Message:
            if not User_id in Dates['Admin']:
                Task.AddTask(Thread(target=Server.Send_Group_Msg, args=(Group_id, "你没有Admin权限，无法查看管理列表")))
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
            Group_Msg(request.json['group_id'], request.json['user_id'], request.json['raw_message'], request.json['message_id'])
    return 'ok'
def DateAutoSave():
    global Dates

    while True:
        if Dates != ToolAPI.JsonAuto(None, "READ"):
            Task.AddTask(Thread(target=ToolAPI.JsonAuto, args=(Dates, "WRITE")))


Always_Task.append(Thread(target=app.run, kwargs=dict(host='0.0.0.0' ,port=Dates['AcceptPort'])))
Always_Task.append(Thread(target=Task))
Always_Task.append(Thread(target=DateAutoSave))

if __name__ == '__main__':
    for each in Always_Task:
        each.start()
    for each in Always_Task:
        each.join()