"""
CoolPlayLin-Bot的API基础
"""

# 导入本地API
from . import cqbotapi as NormalAPI
from . import util as ToolAPI
from . import typings

# 导入依赖库
import pathlib, random
from requests import get

# 群聊消息处理
def Group_Msg(Server:NormalAPI.APIs, Group_id:int, User_id:int, Message:str, Message_Id:int, Dates:dict) -> bool:

    if not isinstance(Server, NormalAPI.APIs):
        return False
    try:
        Msg = {}
        Admin:bool = (Group_id in Dates["AdminGroup"])

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

            elif Message in [Dates["@Me"]+each for each in ["menu", "Menu", "MENU", "菜单","功能", "功能列表", "help", "帮助"]]:
                Msg["Hello，我是由CoolPlayLin开发并维护的开源QQ机器人，采用GPLv3许可证，项目直达 -> https://github.com/CoolPlayLin/CoolPlayLin-Bot\n我目前的功能\n1. 一言：获取一言文案"] = Group_id
            elif Message in [Dates["@Me"]+each for each in ["命令列表", "Command", "CommandList", "Command List", "All Command", "command", "命令"]]:
                Msg["以下是所有管理员命令的列表\n1. Set Root 设置发送者为Root用户\n2. 开灯|关灯 关闭|启动全体禁言\n3. Show|Add|Del AdminGroup 展示|增加|删除管理的群聊\n4. Add This AdminGroup 将添加此群聊为所管理群聊\n5. Refuse|Accept 拒绝|同意请求\n6. Show|Add|Del Admin 展示|增加|删除管理员\n7. 禁言大转盘 随机分钟禁言\n8. 冷静 禁言1分钟"] = Group_id
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
            elif Message in [Dates["@Me"]+'获取一言', Dates["@Me"]+'一言', Dates["@Me"]+'文案']:
                Msg[(get("https://v1.hitokoto.cn/").json()['hitokoto'])] = Group_id
            elif Dates["@Me"].replace(" ", "") in Message:
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
        print(0000)
        ToolAPI.JsonAuto(Dates, "WRITE", PATH)