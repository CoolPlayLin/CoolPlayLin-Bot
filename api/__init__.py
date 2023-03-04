"""
CoolPlayLin-Bot的API基础与功能实现

核心代码，不支持直接启动
"""

# 导入依赖API
if __name__ != "__main__":
    from flask import Flask, render_template, request
    from threading import Thread
    from . import cqbotapi as NormalAPI
    from . import util as ToolAPI
    from . import typings
    import pathlib, random
    import requests
else:
    print("本程序需要启动器进行启动，不允许直接运行")
    quit(0)

# 加载必要数据
app = Flask(__name__)
PATH = pathlib.Path(__file__).parent.parent / "database" / "config.json"
Dates = ToolAPI.JsonAuto(None, "READ", PATH)
Task = ToolAPI.TaskManager(0)
API_PATH = pathlib.Path(__file__).parent.parent / "database" / "API.json"
LOG_PATH = pathlib.Path(__file__).parent.parent / "database" / "running.log"
API = ToolAPI.JsonAuto(None, "READ", API_PATH)
logger = ToolAPI.Logger(LOG_PATH)

# 数据纠错
if not API:
    urls = ("https://cdn.jsdelivr.net/gh/CoolPlayLin/CoolPlayLin-Bot@main/database/API.json", "https://fastly.jsdelivr.net/gh/CoolPlayLin/CoolPlayLin-Bot@main/database/API.json", "https://gitee.com/coolplaylin/CoolPlayLin-Bot/raw/main/database/API.json")
    for each in urls:
        try:
            with open(API_PATH, "w+", encoding="utf-8") as f:
                f.write(requests.get(url=each, verify=False).text)
                break
        except:
            continue
    quit()

# 实例化所需API
Server = NormalAPI.APIs(Dates['PostIP'])
Server_amap = NormalAPI.Amap(API["keys"]["amap"])
Server_others = NormalAPI.OtherAPI(API["keys"]["chatgpt"])

# 群聊消息处理
def Group_Msg(Server:NormalAPI.APIs, Group_id:int, User_id:int, Message:str, Message_Id:int, Dates:dict, clean_up:ToolAPI.clean_up, amap:NormalAPI.Amap, others:NormalAPI.OtherAPI) -> bool:
    if not isinstance(Server, NormalAPI.APIs):
        return False
    try:
        if Dates["@Me"] in Message:
            Message = clean_up(Message, [Dates["@Me"]])
            Msg = {}
            Admin:bool = (User_id in Dates["Admin"])
            AdminGroup:bool = (Group_id in Dates["AdminGroup"])
            AdminGroup_Admin:bool = (Admin and AdminGroup)

            if User_id in Dates['NotAllowUser']:
                Msg['管理员不允许你使用'] = Group_id
            elif ToolAPI.BadWord(Message, Dates['BadWords']) and AdminGroup:
                    Server.Delete_Msg(message_id=Message_Id)
                    Msg["检测到敏感内容, 已尝试撤回"] = Group_id
            else:
                if '冷静' in Message and AdminGroup_Admin:
                    User = int(clean_up(Message, ["冷静", " "]))
                    Server.Set_Group_Ban(Group_id, User, 60)
                    Msg["已尝试冷静此人"] = Group_id
                elif '禁言大转盘' in Message and AdminGroup_Admin:
                    User = int(clean_up(Message, ["禁言大转盘", " "]))
                    Min = random.randint(1, 60)
                    Server.Set_Group_Ban(Group_id, User, 60*Min)
                    Msg["恭喜获得{}分钟".format(Min)] = Group_id
                elif '关灯' in Message and AdminGroup_Admin:
                    Server.Set_Group_Whole_Ban(Group_id, True)
                    Msg['全体禁言已启动'] = Group_id
                elif '开灯' in Message and AdminGroup_Admin:
                    Server.Set_Group_Whole_Ban(Group_id, False)
                    Msg['全体禁言已停止'] = Group_id

                elif clean_up(Message, [" "]) in ["menu", "Menu", "MENU", "菜单", "功能", "功能列表", "help", "帮助", "你好", "Hello", "hello"]:
                    Msg[API["Introduce"]] = Group_id
                elif clean_up(Message, [" "]) in ["命令列表", "Command", "CommandList", "Command List", "All Command", "command", "命令"]:
                    Msg[API["Command"]] = Group_id
                elif "命令查找" in Message:
                    _ = [each for each in API["CommandList"].keys() if clean_up(Message, ["命令查找", " "]) in each]
                    if len(_) > 0:
                        _msg = "我找到了如下命令："
                        for each in _:
                            _msg += "\n{}\n{}".format(each, API["CommandList"][each])
                        Msg[_msg] = Group_id
                    else:
                        Msg["我没有找到有关 {} 的命令".format(clean_up(Message, ["命令查找", " "]))] = Group_id
                elif "AdminGroup.show" in Message and Admin:
                    Msg['当前所管理的群\n{}'.format(Dates['AdminGroup'])] = Group_id
                elif "AdminGroup.append!" in Message and Admin:
                    if User_id in Dates['Admin']:
                        Dates['AdminGroup'].append(Group_id)
                        Msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                    else:
                        Msg["你没有Admin权限"] = Group_id
                elif "AdminGroup.append" in Message and Admin:
                    if User_id in Dates['Admin']:
                        Group = int(clean_up(Message ,["AdminGroup.append"]))
                        Dates['AdminGroup'].append(Group)
                        Msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                    else:
                        Msg["你没有Admin权限"] = Group_id
                elif "AdminGroup.del" in Message and Admin:
                    if User_id in Dates['Admin']:
                        Group = int(clean_up(Message, ["AdminGroup.del", " "]))
                        if Group in Dates['AdminGroup']:
                            Dates['AdminGroup'].remove(Group)
                            Msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                        else:
                            Msg['不包含此项'] = Group_id
                    else:
                        Msg["你没有Admin权限"] = Group_id
                elif "Refuse" in Message:
                    if not Admin:
                        Msg["你没有Admin权限"] = Group_id
                    else:
                        User = int(clean_up(Message, ["Refuse", " "]))
                        if User != Dates['Root']:
                            Dates['NotAllowUser'].append(User)
                            Msg['已将此用户添加到拒绝列表\n{}'.format(Dates['NotAllowUser'])] = Group_id
                        else:
                            Msg['不允许将Root用户添加到拒绝列表'] = Group_id
                elif "Accept" in Message:
                    if not Admin:
                        Msg["你没有管理权限"] = Group_id
                    else:
                        User = int(clean_up(Message, ["Accept", " "]))
                        if User in Dates['NotAllowUser']:
                            Dates['NotAllowUser'].remove(User)
                            Msg['已将此用户从拒绝列表移除\n{}'.format(Dates['NotAllowUser'])] = Group_id
                        else:
                            Msg['此用户不在拒绝列表中'] = Group_id
                elif "Refuse.show" in Message:
                    Msg['拒绝用户列表\n{}'.format(Dates['NotAllowUser'])] = Group_id
                elif "Root.set" in Message:
                    if Dates['Root'] == None:
                        Dates['Root'] = User_id
                        Dates['Admin'].append(User_id)
                        Msg['Root成功设置为{}'.format(str(User_id))] = Group_id
                    else:
                        Msg['Root用户已设置，请勿重复设置'] = Group_id
                elif "Admin.show" in Message:
                    if User_id != Dates['Root']:
                        Msg["你没有Root权限"] = Group_id
                    else:
                        Msg["当前管理员列表\n{}".format(str(Dates['Admin']))] = Group_id
                elif 'Admin.append' in Message:
                    if User_id != Dates['Root']:
                        Msg["你没有Root权限"] = Group_id
                    else:
                        Dates['Admin'].append(int(clean_up(Message, ["Admin.append", " "])))
                        Msg["保存成功\n{}".format(str(Dates['Admin']))] = Group_id
                elif 'Admin.del' in Message:
                    if User_id != Dates['Root']:
                        Msg["你没有Root权限"] = Group_id
                    else:
                        _ = int(clean_up(Message, "Admin.del", " "))
                        if _ in Dates['Admin']:
                            Dates['Admin'].remove(_)
                            Msg["保存成功\n{}".format(str(Dates['Admin']))] = Group_id
                        else:
                            Msg["此用户不在Admin中"] = Group_id
                elif 'Status' in Message:
                    Msg["状态如下:\n{}个任务正在排队\n{}个任务正在运行".format(len(Task.Perform_QueuingTask), len(Task.Perform_RunningTask))] = Group_id
                elif Message in [each for each in ['获取一言', '一言', '文案']]:
                    Msg[(others.copy().json()['hitokoto'])] = Group_id
                elif "城市编码" in Message:
                    Message = clean_up(Message, ["城市编码", " "])
                    _ = [each for each in API["CityCode"] if Message in each[0]]
                    if len(_) > 0:
                        _Msg = "我找到了如下城市："
                        for each in _:
                            _Msg += "\n{}: {}".format(each[0], each[1])
                        Msg[_Msg] = Group_id
                    else:
                        Msg["似乎没有这个城市哦~"] = Group_id
                elif "实时天气预报" in Message:
                    if Server_amap.key:
                        city = int(ToolAPI.clean_up(Message, ["实时天气预报", "查询", " "]))
                        Res = amap.forecasters(city, "base").json()
                        if int(Res["status"]) == 1:
                            Res = Res["lives"][0]
                            _ = "{}{} 天气预报如下:\n{}\n天气{} {}风{}级 气温{}℃ 湿度{}%".format(Res["province"], Res["city"], Res["reporttime"], Res["weather"], Res["winddirection"], Res["windpower"], Res["temperature"], Res["humidity"]) if len(Res) > 0 else "未查询到有关 {} 的任何天气情况".format(city)
                            Msg[_] = Group_id
                        else:
                            Msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = Group_id
                    else:
                        Msg["你没有填入Key, 无法请求"] = Group_id
                elif "未来天气预报" in Message:
                    if Server_amap.key:
                        city = int(clean_up(Message, ["未来天气预报", "查询", " "]))
                        Res = amap.forecasters(city, "all").json()
                        if int(Res["status"]) == 1:
                            Res = Res["forecasts"][0]
                            if len(Res["casts"]) > 0:
                                _ = "{}{} 未来天气情况如下：".format(Res["province"], Res["city"])
                                for each in Res["casts"]:
                                    _ += "\n{}\n白天{} {}风{}级 气温{}℃\n晚上{} {}风{}级 气温{}℃".format(each["date"], each["dayweather"], each["daywind"], each["daypower"], each["daytemp"], each["nightweather"], each["nightwind"], each["nightpower"], each["nighttemp"])
                            else:
                                _ = "未查询到有关 {} 的任何天气情况".format(city)
                            Msg[_] = Group_id
                        else:
                            Msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = Group_id
                    else:
                        Msg["你没有填入Key, 无法请求"] = Group_id
                elif "IP定位" in Message:
                    if Server_amap.key:
                        ip = clean_up(Message, ["城市", "编码", "查询", " "])
                        Res = amap.ip_positioning(ip).json()
                        if int(Res['status']) == 1:
                            _ = "{} 位于{}{}\n坐标为{}\n该城市的编码为 {}".format(ip, Res["province"], Res["city"], Res["rectangle"], Res["adcode"]) if len(Res["rectangle"]) > 0 else "没有查询到 {} 的信息".format(ip)
                            Msg[_] = Group_id
                        else:
                            Msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = Group_id
                    else:
                        Msg["你没有填入Key, 无法请求"] = Group_id
                elif "ChatGPT" in Message:
                    if others.chatgpt_token:
                        _msg = clean_up(Message, ["ChatGPT", " "])
                        try:
                            _ = others.chatgpt(_msg, API["gptproxy"]) if API["gptproxy"] else others.chatgpt(_msg)
                            Msg["以下是ChatGPT的回答:\n{}".format(_)] = Group_id
                        except:
                            Msg["请求失败，可能是由于网络原因"] = Group_id
                    else:
                        Msg["你没有填入Key, 无法请求"] = Group_id
                else:
                    # 彩蛋
                    if random.randint(1, 1000000) % random.randint(1, 1000000) == 0:
                        _ = "难熬的日子总会过去，不信你回头看看，你都已经在不知不觉中，熬过了很多苦难，很棒吧"
                    elif random.randint(1, 100000) % random.randint(1, 100000) == 0:
                        _ = "无论顺境还是逆境，都希望你能喜欢和接纳当下的自己，爱这个酸甜苦辣的百味人生"
                    elif random.randint(1, 10000) % random.randint(1, 10000) == 0:
                        _ = "生活总是来来往往，千万别等来日方长"
                    elif random.randint(1, 1000) % random.randint(1, 1000) == 0:
                        _ = "路漫漫其修远兮，吾将上下而求索"
                    elif random.randint(1, 1000) % random.randint(1, 1000) == 0:
                        _ = "不是每一次的努力都会有收获，但是每一次的收获都需要努力"
                    elif random.randint(1, 100) % random.randint(1, 100) == 0:
                        _ = "人类的勇气可以跨越时间，跨越当下，跨越未来"
                    elif random.randint(1, 100) % random.randint(1, 100) == 0:
                        _ = "星光不问赶路人，时光不负有心人"
                    else:
                        _ = "干啥子"
                    Msg[_] = Group_id
            # 集中发送消息
            Msgs = Msg.keys()
            for each in Msgs:
                Server.Send_Group_Msg(Msg[each], each)
            return True
    except BaseException as e:
        Server.Send_Group_Msg(Group_id, "错误：\n{}".format(e))
        logger.error(e)
        raise

# 数据保存
def retention(Server:NormalAPI.APIs, Dates:dict, PATH:pathlib.Path) -> None:
    if Dates["BotQQ"] is None:
        logger.event("正在将当前登录QQ的数据写入config.json")
        Dates.update({"BotQQ": Server.Get_Login_Info().json()['data']['user_id'], "@Me": "[CQ:at,qq={}]".format(Server.Get_Login_Info().json()['data']['user_id'])})
        logger.event("数据写入成功完成")
    if Dates != ToolAPI.JsonAuto(None, "TEXT", PATH):
        logger.event("运行数据发生更改，正在保存到本地")
        ToolAPI.JsonAuto(Dates, "WRITE", PATH)
        logger.event("数据写入成功完成")

# POST数据路由
@app.route("/commit", methods=['POST'])
def Main():
    if request.json["post_type"] == "message":
        if request.json['message_type'] == 'group':
            Task.AddTask(Thread(target=logger.event, kwargs=dict(msg="收到{}群{}发送的请求 {}".format(request.json['group_id'], request.json['user_id'], request.json['raw_message']))))
            Task.AddTask(Thread(target=Group_Msg, args=(Server, request.json['group_id'], request.json['user_id'], request.json['raw_message'], request.json['message_id'], Dates, ToolAPI.clean_up, Server_amap, Server_others)))
        elif request.json['message_type'] == 'private':
            Task.AddTask(Thread(target=Server.Send_Private_Msg, args=(request.json['user_id'], "我暂时无法为你服务~")))
    elif request.json["post_type"] == "meta_event":
        if request.json["meta_event_type"] == "heartbeat":
            Task.AddTask(Thread(target=logger.event, kwargs=dict(msg="接收到发来的心跳包，机器人在线")))
    
    # 更新数据
    Task.AddTask(Thread(target=retention, args=(Server, Dates, PATH)))
    return 'ok'

# Web页面路由
@app.route("/", methods=['GET', "POST"])
def Web():
    Res = dict(request.args)
    if "page" in Res:
        print(Res)
        if Res["page"] == '1':
            return render_template("index.html")
        elif Res["page"] == '2':
            return logger.html()
        else:
            return "404"
    else:
        return render_template("index.html")