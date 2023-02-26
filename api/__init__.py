"""
CoolPlayLin-Bot的API基础
"""

# 导入依赖API
from . import cqbotapi as NormalAPI
from . import util as ToolAPI
from . import typings
import pathlib, random
from requests import get

# 加载必要数据
API_PATH = pathlib.Path(__file__).parent.parent / "database" / "API.json"
API = ToolAPI.JsonAuto(None, "READ", API_PATH)

# 群聊消息处理
def Group_Msg(Server:NormalAPI.APIs, Group_id:int, User_id:int, Message:str, Message_Id:int, Dates:dict) -> bool:
    if not isinstance(Server, NormalAPI.APIs):
        return False
    try:
        Msg = {}
        Admin:bool = (Group_id in Dates["AdminGroup"])
        amap:bool = (API["keys"]["amap"] != None)

        if User_id in Dates['NotAllowUser']:
            Msg['管理员不允许你使用'] = Group_id
        elif ToolAPI.BadWord(Message, Dates['BadWords']):
                Server.Delete_Msg(message_id=Message_Id)
                Msg["检测到敏感内容, 已尝试撤回"] = Group_id
        else:
            if Dates["@Me"]+'冷静' in Message:
                if not Admin:
                    Msg["你没有Admin权限"] = Group_id
                else:
                    User = int(Message.replace(Dates["@Me"]+"冷静", ""))
                    Server.Set_Group_Ban(Group_id, User, 60)
                    Msg["已尝试冷静此人"] = Group_id
            elif Dates["@Me"]+'禁言大转盘' in Message:
                if not Admin:
                    Msg["你没有Admin权限"] = Group_id
                else:
                    User = int(Message.replace(Dates["@Me"]+"禁言大转盘", ""))
                    Min = random.randint(1, 60)
                    Server.Set_Group_Ban(Group_id, User, 60*Min)
                    Msg["恭喜获得{}分钟".format(Min)] = Group_id
            elif Dates["@Me"]+'关灯' in Message and Admin:
                Server.Set_Group_Whole_Ban(Group_id, True)
                Msg['全体禁言已启动'] = Group_id
            elif Dates["@Me"]+'开灯' in Message and Admin:
                Server.Set_Group_Whole_Ban(Group_id, False)
                Msg['全体禁言已停止'] = Group_id

            elif Message in [Dates["@Me"]+each for each in ["menu", "Menu", "MENU", "菜单","功能", "功能列表", "help", "帮助", "你好", "Hello", "hello"]]:
                Msg[API["Introduce"]] = Group_id
            elif Message in [Dates["@Me"]+each for each in ["命令列表", "Command", "CommandList", "Command List", "All Command", "command", "命令"]]:
                Msg[API["CommandList"]] = Group_id
            elif Dates["@Me"]+"Show AdminGroup" in Message and Admin:
                Msg['当前所管理的群\n{}'.format(Dates['AdminGroup'])] = Group_id
            elif Dates["@Me"]+"Add AdminGroup" in Message and Admin:
                if User_id in Dates['Admin']:
                    Group = int(Message.replace(Dates["@Me"]+"Add AdminGroup ", ""))
                    Dates['AdminGroup'].append(Group)
                    Msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                else:
                    Msg["你没有Admin权限"] = Group_id
            elif Dates["@Me"]+"Add This AdminGroup" in Message and Admin:
                if User_id in Dates['Admin']:
                    Dates['AdminGroup'].append(Group_id)
                    Msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                else:
                    Msg["你没有Admin权限"] = Group_id
            elif Dates["@Me"]+"Del AdminGroup" in Message and Admin:
                if User_id in Dates['Admin']:
                    Group = int(Message.replace(Dates["@Me"]+"Del AdminGroup ", ""))
                    if Group in Dates['AdminGroup']:
                        Dates['AdminGroup'].remove(Group)
                        Msg['保存成功\n{}'.format(Dates['AdminGroup'])] = Group_id
                    else:
                        Msg['不包含此项'] = Group_id
                else:
                    Msg["你没有Admin权限"] = Group_id
            elif Dates["@Me"]+"Refuse" in Message:
                if not Admin:
                    Msg["你没有Admin权限"] = Group_id
                else:
                    User = int(Message.replace(Dates["@Me"]+"Refuse ", ""))
                    if User != Dates['Root']:
                        Dates['NotAllowUser'].append(User)
                        Msg['已将此用户添加到拒绝列表\n{}'.format(Dates['NotAllowUser'])] = Group_id
                    else:
                        Msg['不允许将Root用户添加到拒绝列表'] = Group_id
            elif Dates["@Me"]+"Accept" in Message:
                if not Admin:
                    Msg["你没有管理权限"] = Group_id
                else:
                    User = int(Message.replace(Dates["@Me"]+"Accept ", ""))
                    if User in Dates['NotAllowUser']:
                        Dates['NotAllowUser'].remove(User)
                        Msg['已将此用户从拒绝列表移除\n{}'.format(Dates['NotAllowUser'])] = Group_id
                    else:
                        Msg['此用户不在拒绝列表中'] = Group_id
            elif Dates["@Me"]+"RefuseList" in Message:
                Msg['拒绝用户列表\n{}'.format(Dates['NotAllowUser'])] = Group_id
            elif Dates["@Me"]+"Set Root" in Message:
                if Dates['Root'] == None:
                    Dates['Root'] = User_id
                    Dates['Admin'].append(User_id)
                    Msg['Root成功设置为{}'.format(str(User_id))] = Group_id
                else:
                    Msg['Root用户已设置，请勿重复设置'] = Group_id
            elif Dates["@Me"]+"Show Admin" in Message:
                if User_id != Dates['Root']:
                    Msg["你没有Root权限"] = Group_id
                else:
                    Msg["当前管理员列表\n{}".format(str(Dates['Admin']))] = Group_id
            elif Dates["@Me"]+'Add Admin' in Message:
                if User_id != Dates['Root']:
                    Msg["你没有Root权限"] = Group_id
                else:
                    Dates['Admin'].append(int(Message.replace(Dates["@Me"]+"Add Admin ", "")))
                    Msg["保存成功\n{}".format(str(Dates['Admin']))] = Group_id
            elif Dates["@Me"]+'Del Admin' in Message:
                if User_id != Dates['Root']:
                    Msg["你没有Root权限"] = Group_id
                else:
                    _ = int(Message.replace(Dates["@Me"]+"Del Admin ", ""))
                    if _ in Dates['Admin']:
                        Dates['Admin'].remove(_)
                        Msg["保存成功\n{}".format(str(Dates['Admin']))] = Group_id
                    else:
                        Msg["此用户不在Admin中"] = Group_id
            elif Dates["@Me"]+'Status' in Message:
                Msg["功能未实现"] = Group_id
            elif Message in [Dates["@Me"]+each for each in ['获取一言', '一言', '文案']]:
                Msg[(get("https://v1.hitokoto.cn/").json()['hitokoto'])] = Group_id
            elif Dates["@Me"]+"城市编码" in Message:
                Message = Message.replace(Dates["@Me"]+"城市编码 ", "")
                _ = [each for each in API["CityCode"] if Message in each[0]]
                if len(_) > 0:
                    _Msg = "我找到了如下城市："
                    for each in _:
                        _Msg += "\n{}: {}".format(each[0], each[1])
                    Msg[_Msg] = Group_id
                else:
                    Msg["似乎没有这个城市哦~"] = Group_id
            elif Dates["@Me"]+"实时天气预报" in Message:
                if amap:
                    city = int(Message.replace(Dates["@Me"]+"实时天气预报", "").replace("查询", "").replace(" ", ""))
                    Res = get("https://restapi.amap.com/v3/weather/weatherInfo?key={}&city={}&extensions=base".format(API["keys"]["amap"], city)).json()
                    if int(Res["status"]) == 1:
                        Res = Res["lives"][0]
                        _ = "{}{} {} 天气预报如下:\n天气{}, {}风 风力{}, 温度{}℃ 湿度{}%".format(Res["province"], Res["city"], Res["reporttime"], Res["weather"], Res["winddirection"], Res["windpower"], Res["temperature"], Res["humidity"]) if len(Res) > 0 else "未查询到有关 {} 的任何天气情况".format(city)
                        Msg[_] = Group_id
                    else:
                        Msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = Group_id
                else:
                    Msg["你没有填入Key, 无法请求"] = Group_id
            elif Dates["@Me"]+"未来天气预报" in Message:
                if amap:
                    city = int(Message.replace(Dates["@Me"]+"未来天气预报", "").replace("查询", "").replace(" ", ""))
                    Res = get("https://restapi.amap.com/v3/weather/weatherInfo?key={}&city={}&extensions=all".format(API["keys"]["amap"], city)).json()
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
            elif Dates["@Me"]+"IP定位" in Message:
                if amap:
                    ip = Message.replace(Dates["@Me"]+"IP定位", "").replace(" ", "")
                    Res = get("https://restapi.amap.com/v3/ip?key={}&ip={}".format(API["keys"]["amap"], ip)).json()
                    if int(Res['status']) == 1:
                        _ = "{} 位于{}{}\n坐标为{}\n该城市的编码为 {}".format(ip, Res["province"], Res["city"], Res["rectangle"], Res["adcode"]) if len(Res["rectangle"]) > 0 else "没有查询到 {} 的信息".format(ip)
                        Msg[_] = Group_id
                    else:
                        Msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = Group_id
                else:
                    Msg["你没有填入Key, 无法请求"] = Group_id
            elif Dates["@Me"] in Message:
                Msg["干啥子"] = Group_id
        # 集中发送消息
        Msgs = Msg.keys()
        for each in Msgs:
            Server.Send_Group_Msg(Msg[each], Msgs)
        return True
    except BaseException as e:
        Server.Send_Group_Msg(Group_id, "错误：\n{}".format(e))
        raise

# 数据保存
def retention(Server:NormalAPI.APIs, Dates:dict, PATH:pathlib.Path) -> None:
    if Dates["BotQQ"] is None:
        Dates.update({"BotQQ": Server.Get_Login_Info().json()['data']['user_id'], "@Me": "[CQ:at,qq={}] ".format(Server.Get_Login_Info().json()['data']['user_id'])})
    if Dates != ToolAPI.JsonAuto(None, "TEXT", PATH):
        ToolAPI.JsonAuto(Dates, "WRITE", PATH)