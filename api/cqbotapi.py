"""
Go-cqhttp的API库
"""

import requests
from revChatGPT.V3 import Chatbot

__all__ = ('APIs', "Amap")

# Go-cqhttp的API
class APIs:
    __slots__ = ('Server', 'Verify', 'AccessKey')
    def __init__(self, Server:str, head:str="http://", Verify:bool=False, AccessKey:str=False) -> None:
        self.Server = head+Server
        self.Verify = Verify
        # self.AccessKey = AccessKey
    def Send_Private_Msg(self, user_id:int, message:str, group_id:int=False, auto_escape:bool=False) -> requests.Response:
        Date = {
            'user_id': user_id,
            'message': message,
            'auto_escape': auto_escape
        }
        if group_id:
            Date['group_id'] = group_id
        Response = requests.post('{}/send_private_msg'.format(self.Server), data=Date)
        return Response
    def Send_Group_Msg(self, group_id:int, message:str, auto_escape:bool=False) -> requests.Response:
        Date = {
            'group_id': group_id,
            'message': message,
            'auto_escape': auto_escape
        }
        Response = requests.post('{}/send_group_msg'.format(self.Server), data=Date)
        return Response
    def Send_Group_Forward_Msg(self, group_id:int, message:str) -> requests.Response:
        Date = {
            'group_id': group_id,
            'message': message
        }
        Response = requests.post('{}/send_group_forward_msg'.format(self.Server), data=Date)
        return Response
    def Send_Msg(self, message:str, user_id:int, group_id:int, message_type:str=None, auto_escape:bool=False) -> requests.Response:
        Date = {
            'message': message,
            'auto_escape': auto_escape
        }
        if user_id:
            Date['user_id'] = user_id
        if group_id:
            Date['group_id'] = group_id
        if message_type:
            Date['message_type'] = message_type
        Response = requests.post('{}/send_msg'.format(self.Server), data=Date)
        return Response
    def Get_Msg(self, message_id:int) -> requests.Response:
        Date = {
            'message_id': message_id
        }
        Response = requests.post('{}/get_msg'.format(self.Server), data=Date)
        return Response
    def Get_Forward_Msg(self, message_id:int) -> requests.Response:
        Date = {
            'message_id': message_id
        }
        Response = requests.post('{}/get_forward_msg'.format(self.Server), data=Date)
        return Response
    def Get_image(self, file:str) -> requests.Response:
        Date = {
            'file': file
        }
        Response = requests.post('{}/get_image'.format(self.Server), data=Date)
        return Response
    def Mark_Msg_As_Read(self, message_id:int) -> requests.Response:
        Date = {
            'message_id': message_id
        }
        Response = requests.post('{}/mark_msg_as_read'.format(self.Server), data=Date)
        return Response
    def Set_Group_Kick(self, group_id:int, user_id:int, reject_add_request:bool=False) -> requests.Response:
        Date = {
            'group_id': group_id,
            'user_id': user_id,
            'reject_add_request': reject_add_request
        }
        Response = requests.post('{}/set_group_kick'.format(self.Server), data=Date)
        return Response
    def Set_Group_Ban(self, group_id:int, user_id:int, duration:int) -> requests.Response:
        Date = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }
        Response = requests.post("{}/set_group_ban".format(self.Server), data=Date)
        return Response
    def Set_Group_Anonymous_Ban(self, group_id:int, duration:int, anonymous_flag:str=False,anonymous:object=False) -> requests.Response:
        Date = {
            "group_id": group_id,
            "duration": duration,
        }
        if anonymous:
            Date["anonymous"] = anonymous
        if anonymous_flag:
            Date["anonymous_flag"] = anonymous_flag
        Response = requests.post("{}/set_group_anonymous_ban".format(self.Server), data=Date)
        return Response
    def Set_Group_Whole_Ban(self, group_id:int, enable:bool=True) -> requests.Response:
        Date = {
            "group_id": group_id,
            "enable": enable
        }
        Response = requests.post("{}/set_group_whole_ban".format(self.Server), data=Date)
        return Response
    def Set_Group_Admin(self, group_id:int, user_id:int, enable:bool=True) -> requests.Response:
        Date = {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        }
        Response = requests.post("{}/set_group_admin".format(self.Server), data=Date)
        return Response
    def Set_Group_Card(self, group_id:int, user_id:int, card:str) -> requests.Response:
        Date = {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        }
        Response = requests.post("{}/set_group_card".format(self.Server), data=Date)
        return Response
    def Set_Group_Name(self, group_id:int, group_name:str) -> requests.Response:
        Date = {
            "group_id": group_id,
            "group_name": group_name
        }
        Response = requests.post("{}/set_group_name".format(self.Server), data=Date)
        return Response
    def Set_Group_Leave(self, group_id:int, is_dismiss:bool=False) -> requests.Response:
        Date = {
            "group_id": group_id,
            "is_dismiss": is_dismiss
        }
        Response = requests.post("{}/set_group_leave".format(self.Server), data=Date)
        return Response
    def Set_Group_Special_Title(self, group_id:int, user_id:int, special_title:str) -> requests.Response:
        Date = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title
        }
        Response = requests.post("{}/set_group_special_title".format(self.Server), data=Date)
        return Response
    def Send_Group_Sign(self, group_id:int) -> requests.Response:
        Date = {
            "group_id": group_id
        }
        Response = requests.post("{}/send_group_sign".format(self.Server), data=Date)
        return Response
    def Set_Friend_Add_Request(self, flag:str, approve:bool, remark:str=False) -> requests.Response:
        Date = {
            "flag": flag,
            "approve": approve
        }
        if remark:
            Date["remark"] = remark
        Response = requests.post("{}/set_friend_add_request".format(self.Server), data=Date)
        return Response
    def Set_Group_Add_Request(self, flag:str, sub_type:str, approve:bool, reason:str=False) -> requests.Response:
        Date = {
            "flag": flag,
            "sub_type": sub_type,
            "approve": approve
        }
        if reason:
            Date["reason"] = reason
        Response = requests.post("{}/set_group_add_request".format(self.Server), data=Date)
        return Response
    def Get_Login_Info(self) -> requests.Response:
        Response = requests.post("{}/get_login_info".format(self.Server))
        return Response
    def Didian_Get_Account_Info(self) -> requests.Response:
        Response = requests.post("{}/qidian_get_account_info".format(self.Server))
        return Response
    def Get_Friend_List(self) -> requests.Response:
        Response = requests.post("{}/get_friend_list".format(self.Server))
        return Response
    def Get_Unidirectional_Friend_List(self) -> requests.Response:
        Response = requests.post("{}/get_unidirectional_friend_list".format(self.Server))
        return Response
    def Set_QQ_Profile(self, nickname:str, company:str, email:str, college:str, personal_note:str) -> requests.Response:
        Date = {
            "nickname": nickname,
            "company": company,
            "email": email,
            "college": college,
            "personal_note": personal_note
        }
        Response = requests.post("{}/set_qq_profile".format(self.Server), data=Date)
        return Response
    def Get_Stranger_Info(self, user_id:int, no_cache:bool=False) -> requests.Response:
        Date = {
            "user_id": user_id,
            "no_cache": no_cache
        }
        Response = requests.post("{}/get_stranger_info".format(self.Server), data=Date)
        return Response
    def Delete_Friend(self, user_id:int) -> requests.Response:
        Date = {
            "user_id": user_id
        }
        Response = requests.post("{}/delete_friend".format(self.Server), data=Date)
        return Response
    def Delete_Msg(self, message_id:int) -> requests.Response:
        Date = {
            "message_id": message_id
        }
        Response = requests.post("{}/delete_msg".format(self.Server), data=Date)
        return Response

# 高德地图API
class Amap:
    __slots__ = ("key")
    def __init__(self, key:str) -> None:
        self.key = key
    def ip_positioning(self, ip:str) -> requests.Response:
        Response = requests.get("https://restapi.amap.com/v3/ip?key={}&ip={}".format(self.key, ip))
        return Response
    def forecasters(self, city, extensions) -> requests.Response:
        Response = requests.get("https://restapi.amap.com/v3/weather/weatherInfo?key={}&city={}&extensions={}".format(self.key, city, extensions))
        return Response

# 其他杂七杂八的API
class OtherAPI:
    __slots__ = ("chatgpt_token")
    def __init__(self, chatgpt_token:str) -> None:
        self.chatgpt_token = chatgpt_token
    def copy(self) -> requests.Response:
        Response = requests.get("https://v1.hitokoto.cn/")
        return Response
    def chatgpt(self, msg:str, proxy:str=None) -> str:
        if proxy:
            chatbot = Chatbot(self.chatgpt_token, proxy=proxy)
        else:
            chatbot = Chatbot(self.chatgpt_token)
        Response = chatbot.ask(msg)
        return Response