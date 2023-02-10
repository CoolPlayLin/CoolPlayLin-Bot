import requests

__all__ = ['APIs']

class APIs:
    __slots__ = ('Server', 'Verify', 'AccessKey')
    def __init__(self, Server:str, head:str="http://", Verify:bool=False, AccessKey:str=False, Online:bool=True) -> None:
        self.Server = head+Server
        self.Verify = Verify
        self.AccessKey = AccessKey
        if Online:
            try:
                Status = requests.get(self.Server).status_code
            except:
                Status = False
            if Status in (403, 401):
                print("主机拒绝了连接, AccessKey似乎不正确哦~")
            if Status == 404:
                print("主机的返回代码很玄学, 请检查IP是否正确哦~")
            elif not Status:
                print("主机拒绝了这次连接, 请确认防火墙和IP是否正确哦~")
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