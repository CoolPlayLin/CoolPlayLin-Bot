"""
CoolPlayLin-Bot的API基础与功能实现

核心代码，不支持直接启动
"""

# 导入依赖API
from . import typing


if __name__ != "__main__":
    from flask import Flask, render_template, request
    from threading import Thread
    from . import api, util
    import pathlib, random, time
else:
    print("本程序需要启动器进行启动，不允许直接运行")
    quit(0)

# 加载必要数据
PATH = pathlib.Path(__file__).parent.parent / "database" / "config.json"
API_PATH = pathlib.Path(__file__).parent.parent / "database" / "API.json"
LOG_PATH = pathlib.Path(__file__).parent.parent / "database" / "running.log"
DB_PATH = pathlib.Path(__file__).parent.parent / "database" / "db.dat"
Dates = util.jsonauto(None, "READ", PATH)
API = util.jsonauto(None, "READ", API_PATH)
DB = util.jsonauto(None, "READ", DB_PATH)
Task = util.TaskManager(0)
logger = util.Logger(LOG_PATH)

# 实例化所需API
server = api.APIs(Dates['PostIP'])
amap = api.Amap(API["keys"]["amap"])
others = api.OtherAPI(API["keys"]["chatgpt"])

# 群聊消息处理
def group_msg(Group_id:int,
              User_id:int,
              Message:str,
              Message_Id:int,
              Dates:dict,
              API:dict,
              DB:dict,
              safe_sleep:float=0.5) -> bool:
    try:
        if Dates["@Me"] in Message:
            msg = {}
            Message = util.clean_up(Message, [Dates["@Me"]]).lstrip()
            admin:bool = (User_id in Dates["Admin"])
            admingroup:bool = (Group_id in Dates["AdminGroup"])
            admingroup_admin:bool = (admin and admingroup)

            if User_id in Dates['NotAllowUser']:
                msg['管理员不允许你使用'] = Group_id
            elif util.badwords(Message, Dates['BadWords']) and admingroup:
                    server.delete_msg(message_id=Message_Id)
                    msg["检测到敏感内容, 已尝试撤回"] = Group_id
            else:
                if '冷静' in Message and admingroup_admin:
                    User = int(util.clean_up(Message, ["冷静", " "]))
                    server.set_group_ban(Group_id, User, 60)
                    msg["已尝试冷静此人"] = Group_id
                elif '禁言大转盘' in Message and admingroup_admin:
                    User = int(util.clean_up(Message, ["禁言大转盘", " "]))
                    Min = random.randint(1, 60)
                    server.set_group_ban(Group_id, User, 60*Min)
                    msg["恭喜获得{}分钟".format(Min)] = Group_id
                elif '关灯' in Message and admingroup_admin:
                    server.set_group_whole_ban(Group_id, True)
                    msg['全体禁言已启动'] = Group_id
                elif '开灯' in Message and admingroup_admin:
                    server.set_group_whole_ban(Group_id, False)
                    msg['全体禁言已停止'] = Group_id

                elif util.clean_up(Message, [" "]) in ["menu", "Menu", "MENU", "菜单", "功能", "功能列表", "help", "帮助", "你好", "Hello", "hello"]:
                    msg[API["Introduce"]] = Group_id
                elif util.clean_up(Message, [" "]) in ["命令列表", "Command", "CommandList", "Command List", "All Command", "command", "命令"]:
                    msg[API["Command"]] = Group_id
                elif "命令查找" in Message:
                    _ = [each for each in API["CommandList"].keys() if util.clean_up(Message, ["命令查找", " "]) in each]
                    if len(_) > 0:
                        _msg = "我找到了如下命令："
                        for each in _:
                            _msg += "\n{}\n{}".format(each, API["CommandList"][each])
                        msg[_msg] = Group_id
                    else:
                        msg["我没有找到有关 {} 的命令".format(util.clean_up(Message, ["命令查找", " "]))] = Group_id
                elif "AdminGroup.show" in Message and admin:
                    msg['当前所管理的群\n{}'.format(Dates['AdminGroup'])] = Group_id
                elif "AdminGroup.append!" in Message and admin:
                    if User_id in Dates['Admin']:
                        Dates['AdminGroup'].append(Group_id)
                        msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                    else:
                        msg["你没有Admin权限"] = Group_id
                elif "AdminGroup.append" in Message and admin:
                    if User_id in Dates['Admin']:
                        Group = int(util.clean_up(Message ,["AdminGroup.append"]))
                        Dates['AdminGroup'].append(Group)
                        msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                    else:
                        msg["你没有Admin权限"] = Group_id
                elif "AdminGroup.del" in Message and admin:
                    if User_id in Dates['Admin']:
                        Group = int(util.clean_up(Message, ["AdminGroup.del", " "]))
                        if Group in Dates['AdminGroup']:
                            Dates['AdminGroup'].remove(Group)
                            msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                        else:
                            msg['不包含此项'] = Group_id
                    else:
                        msg["你没有Admin权限"] = Group_id
                elif "Refuse" in Message and admin:
                    User = int(util.clean_up(Message, ["Refuse", " "]))
                    if User != Dates['Root']:
                        Dates['NotAllowUser'].append(User)
                        msg['已将此用户添加到拒绝列表\n{}'.format(Dates['NotAllowUser'])] = Group_id
                    else:
                        msg['不允许将Root用户添加到拒绝列表'] = Group_id
                elif "Accept" in Message and admin:
                    User = int(util.clean_up(Message, ["Accept", " "]))
                    if User in Dates['NotAllowUser']:
                        Dates['NotAllowUser'].remove(User)
                        msg['已将此用户从拒绝列表移除\n{}'.format(Dates['NotAllowUser'])] = Group_id
                    else:
                        msg['此用户不在拒绝列表中'] = Group_id
                elif "Refuse.show" in Message:
                    msg['拒绝用户列表\n{}'.format(Dates['NotAllowUser'])] = Group_id
                elif "Root.set" in Message:
                    if Dates['Root'] == None:
                        Dates['Root'] = User_id
                        Dates['Admin'].append(User_id)
                        msg['Root成功设置为{}'.format(str(User_id))] = Group_id
                    else:
                        msg['Root用户已设置，请勿重复设置'] = Group_id
                elif "Admin.show" in Message:
                    if User_id != Dates['Root']:
                        msg["你没有Root权限"] = Group_id
                    else:
                        msg["当前管理员列表\n{}".format(str(Dates['Admin']))] = Group_id
                elif 'Admin.append' in Message:
                    if User_id != Dates['Root']:
                        msg["你没有Root权限"] = Group_id
                    else:
                        Dates['Admin'].append(int(util.clean_up(Message, ["Admin.append", " "])))
                        msg["保存成功\n{}".format(str(Dates['Admin']))] = Group_id
                elif 'Admin.del' in Message:
                    if User_id != Dates['Root']:
                        msg["你没有Root权限"] = Group_id
                    else:
                        _ = int(util.clean_up(Message, ["Admin.del", " "]))
                        if _ in Dates['Admin']:
                            Dates['Admin'].remove(_)
                            msg["保存成功\n{}".format(str(Dates['Admin']))] = Group_id
                        else:
                            msg["此用户不在Admin中"] = Group_id
                elif 'Status' in Message:
                    msg["状态如下:\n{}个任务正在排队\n{}个任务正在运行".format(len(Task.Perform_QueuingTask), len(Task.Perform_RunningTask))] = Group_id
                elif util.clean_up(Message, [" "]) in ['获取一言', '一言', '文案']:
                    msg[(others.copy().json()['hitokoto'])] = Group_id
                elif "城市编码" in Message:
                    _city = util.clean_up(Message, ["城市编码", " "])
                    if len(_city) > 0:
                        _ = [each for each in DB["CityCode"] if _city in each[0]]
                        if len(_) > 0:
                            _Msg = "我找到了如下城市："
                            for each in _:
                                _Msg += "\n{}: {}".format(each[0], each[1])
                            msg[_Msg] = Group_id
                        else:
                            msg["似乎没有这个城市哦~"] = Group_id
                    else:
                        msg["输入的内容为空"] = Group_id
                elif "实时天气预报" in Message:
                    if amap.key:
                        city = int(util.util.clean_up(Message, ["实时天气预报", "查询", " "]))
                        Res = amap.forecasters(city, "base").json()
                        if int(Res["status"]) == 1:
                            Res = Res["lives"][0]
                            _ = "{}{} 天气预报如下:\n{}\n天气{} {}风{}级 气温{}℃ 湿度{}%".format(Res["province"], Res["city"], Res["reporttime"], Res["weather"], Res["winddirection"], Res["windpower"], Res["temperature"], Res["humidity"]) if len(Res) > 0 else "未查询到有关 {} 的任何天气情况".format(city)
                            msg[_] = Group_id
                        else:
                            msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = Group_id
                    else:
                        msg["你没有填入Key, 无法请求"] = Group_id
                elif "未来天气预报" in Message:
                    if amap.key:
                        city = int(util.clean_up(Message, ["未来天气预报", "查询", " "]))
                        Res = amap.forecasters(city, "all").json()
                        if int(Res["status"]) == 1:
                            Res = Res["forecasts"][0]
                            if len(Res["casts"]) > 0:
                                _ = "{}{} 未来天气情况如下：".format(Res["province"], Res["city"])
                                for each in Res["casts"]:
                                    _ += "\n{}\n白天{} {}风{}级 气温{}℃\n晚上{} {}风{}级 气温{}℃".format(each["date"], each["dayweather"], each["daywind"], each["daypower"], each["daytemp"], each["nightweather"], each["nightwind"], each["nightpower"], each["nighttemp"])
                            else:
                                _ = "未查询到有关 {} 的任何天气情况".format(city)
                            msg[_] = Group_id
                        else:
                            msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = Group_id
                    else:
                        msg["你没有填入Key, 无法请求"] = Group_id
                elif "IP定位" in Message:
                    if amap.key:
                        ip = util.clean_up(Message, ["城市", "编码", "查询", " "])
                        if len(ip) > 0:
                            Res = amap.ip_positioning(ip).json()
                            if int(Res['status']) == 1:
                                _ = "{} 位于{}{}\n坐标为{}\n该城市的编码为 {}".format(ip, Res["province"], Res["city"], Res["rectangle"], Res["adcode"]) if len(Res["rectangle"]) > 0 else "没有查询到 {} 的信息".format(ip)
                                msg[_] = Group_id
                            else:
                                msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = Group_id
                        else:
                            msg["输入的内容为空"] = Group_id
                    else:
                        msg["你没有填入Key, 无法请求"] = Group_id
                        
                elif "ChatGPT" in Message:
                    if others.chatgpt_token:
                        _msg = util.clean_up(Message, ["ChatGPT", " "])
                        if len(_msg) > 0:
                            try:
                                _ = others.chatgpt(_msg, API["gptproxy"]) if API["gptproxy"] else others.chatgpt(_msg)
                                if len(_) <= 512:
                                    msg["以下是ChatGPT的回答:\n{}".format(_)] = Group_id
                                else:
                                    msg["以下是ChatGPT的回答:"] = Group_id
                                    msg.update({each:Group_id for each in util.cut_str(_, 512)})
                            except:
                                msg["请求失败，可能是由于网络原因"] = Group_id
                        else:
                            msg["输入的内容为空"] = Group_id
                    else:
                        msg["你没有填入Key, 无法请求"] = Group_id
                elif "搜索Github" in Message:
                    _data = others.search_github(util.clean_up(Message, [" ", ":", "搜索Github"])).json()
                    _msg = "搜索到{}个结果，只展示前30".format(_data["total_count"]) if _data["total_count"] > 30 else "搜索到{}个结果".format(_data["total_count"])
                    for each in _data["items"]:
                        _msg += "\n仓库名称:{}\n作者:{}\n描述:{}\n项目地址:{}\n=====".format(each["name"], each["owner"]["login"], each["description"], each["html_url"])
                    if len(_msg) <= 512:
                        msg[_msg] = Group_id
                    else:
                        msg.update({each:Group_id for each in util.cut_str(_msg, 512)})
                elif "拼音查询" in Message:
                    _all = [each[0] for each in DB["PiYin2"]] if "拼音查询!" in Message else [each[0] for each in DB["PiYin1"]]
                    _word = util.clean_up(Message, [" ", "拼音查询!", "拼音查询"])
                    if len(_word) == 0:
                        res = "请输入内容"
                    elif len(_word) >= 512:
                        res = "汉字数量超过限制"
                    else:
                        res = """"{}"的拼音为""".format(_word)
                        for word in _word:
                            _exist = word in _all
                            for each in (DB["PiYin2"] if "拼音查询!" in Message else DB["PiYin1"]):
                                if _exist:
                                    if each[0] == word:
                                        res += " {}".format(each[1])
                                        break
                                else:
                                    res += " {}".format(word)  
                                    break
                    msg[res] = Group_id
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
                    msg[_] = Group_id
            # 集中发送消息
            Msgs = msg.keys()
            for each in Msgs:
                server.send_group_msg(msg[each], each)
                time.sleep(safe_sleep)
            return True
    except BaseException as e:
        server.send_group_msg(Group_id, "错误：\n{}".format(e))
        logger.error(e)
        raise

# 数据保存
def retention(server:api.APIs, Dates:dict, PATH:pathlib.Path) -> bool:
    if Dates["BotQQ"] is None:
        logger.event("正在将当前登录QQ的数据写入config.json")
        Dates.update({"BotQQ": server.get_login_info().json()['data']['user_id'], "@Me": "[CQ:at,qq={}]".format(server.get_login_info().json()['data']['user_id'])})
        logger.event("数据写入成功完成")
    if Dates != util.jsonauto(None, "TEXT", PATH):
        logger.event("运行数据发生更改，正在保存到本地")
        util.jsonauto(Dates, "WRITE", PATH)
        logger.event("数据写入成功完成")
    return True

# Flask数据接收
app = Flask(__name__)

@app.route("/commit", methods=['POST']) # POST数据路由
def accept():
    if request.json["post_type"] == "message":
        if request.json['message_type'] == 'group':
            Task.AddTask(Thread(target=logger.event, kwargs=dict(msg="收到{}群{}发送的请求 {}".format(request.json['group_id'], request.json['user_id'], request.json['raw_message']))))
            Task.AddTask(Thread(target=group_msg, args=(request.json['group_id'], request.json['user_id'], request.json['raw_message'], request.json['message_id'], Dates, API, DB)))
        elif request.json['message_type'] == 'private':
            Task.AddTask(Thread(target=server.send_private_msg, args=(request.json['user_id'], "我暂时无法为你服务~")))
    elif request.json["post_type"] == "meta_event":
        if request.json["meta_event_type"] == "heartbeat":
            Task.AddTask(Thread(target=logger.event, kwargs=dict(msg="接收到心跳包，机器人在线")))
    
    # 更新数据
    Task.AddTask(Thread(target=retention, args=(server, Dates, PATH)))
    return 'ok'

@app.route("/", methods=['GET', "POST"]) # Web页面路由
def web():
    Res = dict(request.args)
    if "page" in Res:
        if Res["page"] == '1':
            return render_template("index.html")
        elif Res["page"] == '2':
            return logger.html()
        else:
            return "404"
    else:
        return render_template("index.html")