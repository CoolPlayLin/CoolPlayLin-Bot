"""
Go-cqhttp的API库
"""
from revChatGPT.V3 import Chatbot
import openai, pathlib, random, requests, warnings

warnings.filterwarnings('ignore')

__all__ = ('APIs', "Amap")

# Go-cqhttp的API
class APIs:
    __slots__ = ('Server', 'Verify', 'headers')
    def __init__(self, Server:str, head:str="http://", Verify:bool=False, AccessKey:str=None) -> None:
        self.Server = head+Server
        self.Verify = Verify
        self.headers = {
            "Authorization": "Bearer {}".format(AccessKey)
        }
    def send_private_msg(self, user_id:int, message:str, group_id:int=False, auto_escape:bool=False) -> requests.Response:
        Date = {
            'user_id': user_id,
            'message': message,
            'auto_escape': auto_escape
        }
        if group_id:
            Date['group_id'] = group_id
        Response = requests.post('{}/send_private_msg'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def send_group_msg(self, group_id:int, message:str, auto_escape:bool=False) -> requests.Response:
        Date = {
            'group_id': group_id,
            'message': message,
            'auto_escape': auto_escape
        }
        Response = requests.post('{}/send_group_msg'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def send_group_forward_msg(self, group_id:int, message:str) -> requests.Response:
        Date = {
            'group_id': group_id,
            'message': message
        }
        Response = requests.post('{}/send_group_forward_msg'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def send_msg(self, message:str, user_id:int, group_id:int, message_type:str=None, auto_escape:bool=False) -> requests.Response:
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
        Response = requests.post('{}/send_msg'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def get_msg(self, message_id:int) -> requests.Response:
        Date = {
            'message_id': message_id
        }
        Response = requests.post('{}/get_msg'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def get_forward_msg(self, message_id:int) -> requests.Response:
        Date = {
            'message_id': message_id
        }
        Response = requests.post('{}/get_forward_msg'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def get_image(self, file:str) -> requests.Response:
        Date = {
            'file': file
        }
        Response = requests.post('{}/get_image'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def mark_msg_as_read(self, message_id:int) -> requests.Response:
        Date = {
            'message_id': message_id
        }
        Response = requests.post('{}/mark_msg_as_read'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_group_kick(self, group_id:int, user_id:int, reject_add_request:bool=False) -> requests.Response:
        Date = {
            'group_id': group_id,
            'user_id': user_id,
            'reject_add_request': reject_add_request
        }
        Response = requests.post('{}/set_group_kick'.format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_group_ban(self, group_id:int, user_id:int, duration:int) -> requests.Response:
        Date = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }
        Response = requests.post("{}/set_group_ban".format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_group_anonymous_ban(self, group_id:int, duration:int, anonymous_flag:str=False,anonymous:object=False) -> requests.Response:
        Date = {
            "group_id": group_id,
            "duration": duration,
        }
        if anonymous:
            Date["anonymous"] = anonymous
        if anonymous_flag:
            Date["anonymous_flag"] = anonymous_flag
        Response = requests.post("{}/set_group_anonymous_ban".format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_group_whole_ban(self, group_id:int, enable:bool=True) -> requests.Response:
        Date = {
            "group_id": group_id,
            "enable": enable
        }
        Response = requests.post("{}/set_group_whole_ban".format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_group_admin(self, group_id:int, user_id:int, enable:bool=True) -> requests.Response:
        Date = {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        }
        Response = requests.post("{}/set_group_admin".format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_group_card(self, group_id:int, user_id:int, card:str) -> requests.Response:
        Date = {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        }
        Response = requests.post("{}/set_group_card".format(self.Server), data=Date, headers=self.headers)
        return Response
    def Set_Group_Name(self, group_id:int, group_name:str) -> requests.Response:
        Date = {
            "group_id": group_id,
            "group_name": group_name
        }
        Response = requests.post("{}/set_group_name".format(self.Server), data=Date)
        return Response
    def set_group_leave(self, group_id:int, is_dismiss:bool=False) -> requests.Response:
        Date = {
            "group_id": group_id,
            "is_dismiss": is_dismiss
        }
        Response = requests.post("{}/set_group_leave".format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_group_special_title(self, group_id:int, user_id:int, special_title:str) -> requests.Response:
        Date = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title
        }
        Response = requests.post("{}/set_group_special_title".format(self.Server), data=Date, headers=self.headers)
        return Response
    def send_group_sign(self, group_id:int) -> requests.Response:
        Date = {
            "group_id": group_id
        }
        Response = requests.post("{}/send_group_sign".format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_friend_add_request(self, flag:str, approve:bool, remark:str=False) -> requests.Response:
        Date = {
            "flag": flag,
            "approve": approve
        }
        if remark:
            Date["remark"] = remark
        Response = requests.post("{}/set_friend_add_request".format(self.Server), data=Date, headers=self.headers)
        return Response
    def set_group_add_request(self, flag:str, sub_type:str, approve:bool, reason:str=False) -> requests.Response:
        Date = {
            "flag": flag,
            "sub_type": sub_type,
            "approve": approve
        }
        if reason:
            Date["reason"] = reason
        Response = requests.post("{}/set_group_add_request".format(self.Server), data=Date, headers=self.headers)
        return Response
    def get_login_info(self) -> requests.Response:
        Response = requests.post("{}/get_login_info".format(self.Server), headers=self.headers)
        return Response
    def didian_get_account_info(self) -> requests.Response:
        Response = requests.post("{}/qidian_get_account_info".format(self.Server), headers=self.headers)
        return Response
    def get_friend_list(self) -> requests.Response:
        Response = requests.post("{}/get_friend_list".format(self.Server), headers=self.headers)
        return Response
    def get_unidirectional_friend_list(self) -> requests.Response:
        Response = requests.post("{}/get_unidirectional_friend_list".format(self.Server), headers=self.headers)
        return Response
    def set_qq_profile(self, nickname:str, company:str, email:str, college:str, personal_note:str) -> requests.Response:
        Date = {
            "nickname": nickname,
            "company": company,
            "email": email,
            "college": college,
            "personal_note": personal_note
        }
        Response = requests.post("{}/set_qq_profile".format(self.Server), data=Date, headers=self.headers)
        return Response
    def get_stranger_info(self, user_id:int, no_cache:bool=False) -> requests.Response:
        Date = {
            "user_id": user_id,
            "no_cache": no_cache
        }
        Response = requests.post("{}/get_stranger_info".format(self.Server), data=Date, headers=self.headers)
        return Response
    def delete_friend(self, user_id:int) -> requests.Response:
        Date = {
            "user_id": user_id
        }
        Response = requests.post("{}/delete_friend".format(self.Server), data=Date, headers=self.headers)
        return Response
    def delete_msg(self, message_id:int) -> requests.Response:
        Date = {
            "message_id": message_id
        }
        Response = requests.post("{}/delete_msg".format(self.Server), data=Date, headers=self.headers)
        return Response
    def upload_group_file(self, group_id:int, file:str, name:str, folder:str=None) -> requests.Response:
        Date = {
            "group_id": group_id,
            "file": file,
            "name": name
        }
        if folder:
            Date["folder"] = folder
        Response = requests.post("{}/upload_group_file".format(self.Server), data=Date, headers=self.headers)

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
    __slots__ = ("chatgpt_token", "verify")
    def __init__(self, chatgpt_token:str, verify:bool=False) -> None:
        self.chatgpt_token = chatgpt_token
        self.verify = verify
    def copy(self) -> requests.Response:
        Response = requests.get("https://v1.hitokoto.cn/", verify=self.verify)
        return Response
    def chatgpt(self, msg:str, proxy:str=None) -> str:
        chatbot = Chatbot(self.chatgpt_token, proxy=proxy) if proxy else Chatbot(self.chatgpt_token)
        Response = chatbot.ask(msg)
        return Response
    def image_generation(self, description:str) -> dict:
        Response = openai.Image.create(self.chatgpt_token, prompt=description, n=1, size="1024x1024")
        return Response
    def image_variation(self, img_path:pathlib.Path) -> dict:
        Response = openai.Image.create_variation(open(img_path, "rb"), self.chatgpt_token, n=1, size="1024x1024")
        return Response
    def search_github_repo(self, args:str) -> requests.Response:
        Response = requests.get(url="https://api.github.com/search/repositories?q={}".format(args), verify=self.verify)
        return Response
    def search_github_user(self, args:str) -> requests.Response:
        Response = requests.get(url="https://api.github.com/search/users?q={}".format(args), verify=self.verify)
        return Response
    def lookup_github_user(self, user:str) -> requests.Response:
        Response = requests.get("https://api.github.com/users/{}/repos".format(user), verify=self.verify)
        return Response
    def random_image(self) -> requests.Response:
        url = ("https://api.ixiaowai.cn/api/api.php", "https://api.ixiaowai.cn/gqapi/gqapi.php", "https://api.ixiaowai.cn/mcapi/mcapi.php")
        Response = requests.get(url[random.randint(0, len(url)-1)], verify=self.verify)
        return Response