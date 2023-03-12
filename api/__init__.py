"""
CoolPlayLin-Bot的API基础与功能实现

核心代码，不支持直接启动
"""

# 导入依赖API
if __name__ != "__main__":
    from flask import Flask, render_template, request
    from threading import Thread
    from . import api, util, typing
    import pathlib, random, time, os, requests
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
task = util.TaskManager(0, 3)
logger = util.Logger(LOG_PATH)

# 创建缓存文件夹
if not (pathlib.Path(__file__).parent / "cache").exists():
    os.mkdir(pathlib.Path(__file__).parent / "cache")

# 实例化所需API
server = api.APIs(Dates["Server"]['PostIP'], AccessKey=Dates["Server"]["AccessKey"])
amap = api.Amap(API["keys"]["amap"])
others = api.OtherAPI(API["keys"]["chatgpt"])


# 群聊消息处理
def group_msg(group_id:int,
              user_id:int,
              message:str,
              message_id:int,
              Dates:dict,
              API:dict,
              DB:dict,
              safe_sleep:float=0.5) -> bool:
    try:
        if Dates["@Me"] in message:
            msg = {}
            message = util.clean_up(message, [Dates["@Me"]]).lstrip()
            admin:bool = (user_id in Dates["Admin"])
            admingroup:bool = (group_id in Dates["AdminGroup"])
            admingroup_admin:bool = (admin and admingroup)

            if user_id in Dates['NotAllowUser']:
                msg['管理员不允许你使用'] = group_id
            elif util.badwords(message, Dates['BadWords']) and admingroup:
                    server.delete_msg(message_id)
                    msg["检测到敏感内容, 已尝试撤回"] = group_id
            else:
                if '冷静' in message and admingroup_admin:
                    User = int(util.clean_up(message, ["冷静", " "]))
                    server.set_group_ban(group_id, User, 60)
                    msg["已尝试冷静此人"] = group_id
                elif '禁言大转盘' in message and admingroup_admin:
                    User = int(util.clean_up(message, ["禁言大转盘", " "]))
                    Min = random.randint(1, 60)
                    server.set_group_ban(group_id, User, 60*Min)
                    msg["恭喜获得{}分钟".format(Min)] = group_id
                elif '关灯' in message and admingroup_admin:
                    server.set_group_whole_ban(group_id, True)
                    msg['全体禁言已启动'] = group_id
                elif '开灯' in message and admingroup_admin:
                    server.set_group_whole_ban(group_id, False)
                    msg['全体禁言已停止'] = group_id

                elif util.clean_up(message, [" "]) in ["menu", "Menu", "MENU", "菜单", "功能", "功能列表", "help", "帮助", "你好", "Hello", "hello"]:
                    msg[API["Introduce"]] = group_id
                elif util.clean_up(message, [" "]) in ["命令列表", "Command", "CommandList", "Command List", "All Command", "command", "命令"]:
                    msg[API["Command"]] = group_id
                elif "命令查找" in message:
                    _ = [each for each in API["CommandList"].keys() if util.clean_up(message, ["命令查找", " "]) in each]
                    if len(_) > 0:
                        _msg = "我找到了如下命令："
                        for each in _:
                            _msg += "\n{}\n{}".format(each, API["CommandList"][each])
                        msg[_msg] = group_id
                    else:
                        msg["我没有找到有关 {} 的命令".format(util.clean_up(message, ["命令查找", " "]))] = group_id
                elif "AdminGroup.show" in message and admin:
                    msg['当前所管理的群\n{}'.format(Dates['AdminGroup'])] = group_id
                elif "AdminGroup.append!" in message and admin:
                    if user_id in Dates['Admin']:
                        Dates['AdminGroup'].append(group_id)
                        msg['保存成功\n{}'.format(Dates['AdminGroup'])] = group_id
                    else:
                        msg["你没有Admin权限"] = group_id
                elif "AdminGroup.append" in message and admin:
                    if user_id in Dates['Admin']:
                        Group = int(util.clean_up(message ,["AdminGroup.append"]))
                        Dates['AdminGroup'].append(Group)
                        msg['保存成功\n{}'.format(Dates['AdminGroup'])] = group_id
                    else:
                        msg["你没有Admin权限"] = group_id
                elif "AdminGroup.del" in message and admin:
                    if user_id in Dates['Admin']:
                        Group = int(util.clean_up(message, ["AdminGroup.del", " "]))
                        if Group in Dates['AdminGroup']:
                            Dates['AdminGroup'].remove(Group)
                            msg['保存成功\n{}'.format(Dates['AdminGroup'])] = group_id
                        else:
                            msg['不包含此项'] = group_id
                    else:
                        msg["你没有Admin权限"] = group_id
                elif "Refuse" in message and admin:
                    User = int(util.clean_up(message, ["Refuse", " "]))
                    if User != Dates['Root']:
                        Dates['NotAllowUser'].append(User)
                        msg['已将此用户添加到拒绝列表\n{}'.format(Dates['NotAllowUser'])] = group_id
                    else:
                        msg['不允许将Root用户添加到拒绝列表'] = group_id
                elif "Accept" in message and admin:
                    User = int(util.clean_up(message, ["Accept", " "]))
                    if User in Dates['NotAllowUser']:
                        Dates['NotAllowUser'].remove(User)
                        msg['已将此用户从拒绝列表移除\n{}'.format(Dates['NotAllowUser'])] = group_id
                    else:
                        msg['此用户不在拒绝列表中'] = group_id
                elif "Refuse.show" in message:
                    msg['拒绝用户列表\n{}'.format(Dates['NotAllowUser'])] = group_id
                elif "Root.set" in message:
                    if Dates['Root'] == None:
                        Dates['Root'] = user_id
                        Dates['Admin'].append(user_id)
                        msg['Root成功设置为{}'.format(str(user_id))] = group_id
                    else:
                        msg['Root用户已设置，请勿重复设置'] = group_id
                elif "Admin.show" in message:
                    if user_id != Dates['Root']:
                        msg["你没有Root权限"] = group_id
                    else:
                        msg["当前管理员列表\n{}".format(str(Dates['Admin']))] = group_id
                elif 'Admin.append' in message:
                    if user_id != Dates['Root']:
                        msg["你没有Root权限"] = group_id
                    else:
                        Dates['Admin'].append(int(util.clean_up(message, ["Admin.append", " "])))
                        msg["保存成功\n{}".format(str(Dates['Admin']))] = group_id
                elif 'Admin.del' in message:
                    if user_id != Dates['Root']:
                        msg["你没有Root权限"] = group_id
                    else:
                        _ = int(util.clean_up(message, ["Admin.del", " "]))
                        if _ in Dates['Admin']:
                            Dates['Admin'].remove(_)
                            msg["保存成功\n{}".format(str(Dates['Admin']))] = group_id
                        else:
                            msg["此用户不在Admin中"] = group_id
                elif 'Status' in message:
                    msg["以下是全部任务视图:\n{}".format(task._task)] = group_id
                elif util.clean_up(message, [" "]) in ['获取一言', '一言', '文案']:
                    msg[(others.copy().json()['hitokoto'])] = group_id
                elif "城市编码" in message:
                    _city = util.clean_up(message, ["城市编码", " "])
                    if len(_city) > 0:
                        _ = [each for each in DB["CityCode"] if _city in each[0]]
                        if len(_) > 0:
                            _Msg = "我找到了如下城市："
                            for each in _:
                                _Msg += "\n{}: {}".format(each[0], each[1])
                            msg[_Msg] = group_id
                        else:
                            msg["似乎没有这个城市哦~"] = group_id
                    else:
                        msg["输入的内容为空"] = group_id
                elif "实时天气预报" in message:
                    if amap.key:
                        city = int(util.clean_up(message, ["实时天气预报", "查询", " "]))
                        Res = amap.forecasters(city, "base").json()
                        if int(Res["status"]) == 1:
                            Res = Res["lives"][0]
                            _ = "{}{} 天气预报如下:\n{}\n天气{} {}风{}级 气温{}℃ 湿度{}%".format(Res["province"], Res["city"], Res["reporttime"], Res["weather"], Res["winddirection"], Res["windpower"], Res["temperature"], Res["humidity"]) if len(Res) > 0 else "未查询到有关 {} 的任何天气情况".format(city)
                            msg[_] = group_id
                        else:
                            msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = group_id
                    else:
                        msg["你没有填入Key, 无法请求"] = group_id
                elif "未来天气预报" in message:
                    if amap.key:
                        city = int(util.clean_up(message, ["未来天气预报", "查询", " "]))
                        Res = amap.forecasters(city, "all").json()
                        if int(Res["status"]) == 1:
                            Res = Res["forecasts"][0]
                            if len(Res["casts"]) > 0:
                                _ = "{}{} 未来天气情况如下：".format(Res["province"], Res["city"])
                                for each in Res["casts"]:
                                    _ += "\n{}\n白天{} {}风{}级 气温{}℃\n晚上{} {}风{}级 气温{}℃".format(each["date"], each["dayweather"], each["daywind"], each["daypower"], each["daytemp"], each["nightweather"], each["nightwind"], each["nightpower"], each["nighttemp"])
                            else:
                                _ = "未查询到有关 {} 的任何天气情况".format(city)
                            msg[_] = group_id
                        else:
                            msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = group_id
                    else:
                        msg["你没有填入Key, 无法请求"] = group_id
                elif "IP定位" in message:
                    if amap.key:
                        ip = util.clean_up(message, ["城市", "编码", "查询", " "])
                        if len(ip) > 0:
                            Res = amap.ip_positioning(ip).json()
                            if int(Res['status']) == 1:
                                _ = "{} 位于{}{}\n坐标为{}\n该城市的编码为 {}".format(ip, Res["province"], Res["city"], Res["rectangle"], Res["adcode"]) if len(Res["rectangle"]) > 0 else "没有查询到 {} 的信息".format(ip)
                                msg[_] = group_id
                            else:
                                msg["请求失败, 状态代码为{}, 错误原因为{}".format(Res['status'], Res['info'])] = group_id
                        else:
                            msg["输入的内容为空"] = group_id
                    else:
                        msg["你没有填入Key, 无法请求"] = group_id
                        
                elif "ChatGPT" in message:
                    if others.chatgpt_token:
                        _msg = util.clean_up(message, ["ChatGPT", " "])
                        if len(_msg) > 0:
                            try:
                                _ = others.chatgpt(_msg, API["gptproxy"]) if API["gptproxy"] else others.chatgpt(_msg)
                                if len(_) <= 512:
                                    msg["以下是ChatGPT的回答:\n{}".format(_)] = group_id
                                else:
                                    msg["以下是ChatGPT的回答:"] = group_id
                                    msg.update({each:group_id for each in util.cut_str(_, 512)})
                            except:
                                msg["请求失败，可能是由于网络原因"] = group_id
                        else:
                            msg["输入的内容为空"] = group_id
                    else:
                        msg["你没有填入Key, 无法请求"] = group_id
                elif "搜索Github_repo" in message:
                    _data = others.search_github_repo(util.clean_up(message, [" ", ":", "搜索Github_repo"])).json()
                    if "message" in _data:
                        msg["请求失败，原因: {}".format(_data["message"])] = group_id
                    else:
                        _msg = "搜索到{}个结果，只展示前30位".format(_data["total_count"]) if _data["total_count"] > 30 else "搜索到{}个结果".format(_data["total_count"])
                        for each in _data["items"]:
                            _msg += "\n=====\n仓库名称:{}\n作者:{}\n描述:{}\n项目地址:{}".format(each["name"], each["owner"]["login"], each["description"], each["html_url"])
                        if len(_msg) <= 512:
                            msg[_msg] = group_id
                        else:
                            msg.update({each:group_id for each in util.cut_str(_msg, 512)})
                elif "搜索Github_user" in message:
                    _data = others.search_github_user(util.clean_up(message, [" ", ":", "搜索Github_user"])).json()
                    if "message" in _data:
                        msg["请求失败，原因: {}".format(_data["message"])] = group_id
                    else:
                        _msg = "搜索到{}个结果，只展示前30位".format(_data["total_count"]) if _data["total_count"] > 30 else "搜索到{}个结果".format(_data["total_count"])
                        for each in _data["items"]:
                            _msg += "\n=====\n用户名:{}\n主页:{}".format(each["login"], each["html_url"])
                        if len(_msg) <= 512:
                            msg[_msg] = group_id
                        else:
                            msg.update({each:group_id for each in util.cut_str(_msg, 512)})
                elif "查看个人Github" in message:
                    _data = others.lookup_github_user(util.clean_up(message, [" ", ":", "查看个人Github"])).json()
                    if "message" in _data:
                        msg["请求失败，原因: {}".format(_data["message"])] = group_id
                    else:
                        if len(_data) > 0:
                            _msg = "找到了关于{}的{}个仓库信息".format(util.clean_up(message, [" ", ":", "查看个人Github"]), len(_data))
                            for each in _data:
                                _msg += "\n=====\n仓库名称:{}\n描述:{}\n项目地址:{}".format(each["name"], each["description"], each["html_url"])
                            if len(_msg) <= 512:
                                msg[_msg] = group_id
                            else:
                                msg.update({each:group_id for each in util.cut_str(_msg, 512)})
                        else:
                            _msg["{}没有创建任何仓库".format(util.clean_up(message, [" ", ":", "查看个人Github"]))]
                elif "拼音查询" in message:
                    _all = [each[0] for each in DB["PiYin2"]] if "拼音查询!" in message else [each[0] for each in DB["PiYin1"]]
                    _word = util.clean_up(message, [" ", "拼音查询!", "拼音查询"])
                    if len(_word) == 0:
                        res = "请输入内容"
                    elif len(_word) >= 512:
                        res = "汉字数量超过限制"
                    else:
                        res = """"{}"的拼音为""".format(_word)
                        for word in _word:
                            _exist = word in _all
                            for each in (DB["PiYin2"] if "拼音查询!" in message else DB["PiYin1"]):
                                if _exist:
                                    if each[0] == word:
                                        res += " {}".format(each[1])
                                        break
                                else:
                                    res += " {}".format(word)  
                                    break
                    msg[res] = group_id
                elif "图片生成" in message:
                    if others.chatgpt_token:
                        _msg = util.clean_up(message, [" ", "图片生成"])
                        if len(_msg) > 0:
                            _url = others.image_generation(_msg)['data'][0]['url']
                            _img_path = pathlib.Path(__file__).parent / "cache" / "{}.jpg".format(random.randint(1, 100000000))
                            while _img_path.exists():
                                _img_path = pathlib.Path(__file__).parent / "cache" / "{}.jpg".format(random.randint(1, 100000000))
                            with open(_img_path, "wb") as f:
                                res = requests.get(_url)
                                f.write(res.content)
                            server.upload_group_file(group_id , _img_path, _img_path.stem+_img_path.suffix)
                            msg["生成成功完成"] = group_id
                        else:
                            msg["输入的内容为空"] = group_id
                    else:
                        msg["密钥为空，无法请求"] = group_id
                elif "随机图片" in message:
                    _img_path = pathlib.Path(__file__).parent / "cache" / "random{}.jpg".format(random.randint(1, 100000000))
                    while _img_path.exists():
                        _img_path = pathlib.Path(__file__).parent / "cache" / "random{}.jpg".format(random.randint(1, 100000000))
                    with open(_img_path, "wb+") as f:
                        res = others.random_image()
                        f.write(res.content)
                    server.upload_group_file(group_id, _img_path, _img_path.stem+_img_path.suffix)
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
                    msg[_] = group_id
            # 集中发送消息
            for each in msg.keys():
                server.send_group_msg(msg[each], each)
                time.sleep(safe_sleep)
            return True
    except BaseException as e:
        server.send_group_msg(group_id, "错误：\n{}".format(e))
        logger.error(e)
        raise

# 私聊消息处理
def private_msg(user_id:int,
                message:str,
                message_id:int,
                Dates:dict,
                API:dict,
                DB:dict,
                safe_sleep:float=0.5
                ) -> bool:
    try:
        msg = {}
        if user_id in Dates['NotAllowUser']:
                msg['管理员不允许你使用'] = user_id
        elif util.badwords(message, Dates['BadWords']):
                server.delete_msg(message_id)
                msg["检测到敏感词汇，不予处理"] = user_id
        else:
            if "图片生成" in message:
                if others.chatgpt_token:
                    _msg = util.clean_up(message, [" ", "图片生成"])
                    if len(_msg) > 0:
                        _url = others.image_generation(_msg)['data'][0]['url']
                        _img_path = pathlib.Path(__file__).parent / "cache" / "{}.jpg".format(random.randint(1, 100000000))
                        while _img_path.exists():
                            _img_path = pathlib.Path(__file__).parent / "cache" / "{}.jpg".format(random.randint(1, 100000000))
                        with open(_img_path, "wb") as f:
                            res = requests.get(_url)
                            f.write(res.content)
                        msg["[CQ:image,file=file://{},type=show,id=40004]".format(_img_path.as_posix().replace("/", "//"))] = user_id
                    else:
                        msg["输入的内容为空"] = user_id
                else:
                    msg["密钥为空，无法请求"] = user_id
            # elif "图片修改" in message:
            #     if others.chatgpt_token:
            #         _msg = util.clean_up(message, [" ", "图片修改"])
            #         if len(_msg) > 0:
            #             _old_url = _msg[_msg.find("url=")+4:_msg.find(";")]
            #             _old_path = pathlib.Path(__file__).parent / "cache" / "user{}.png".format(random.randint(1, 100000000))
            #             while _old_path.exists():
            #                 _old_path = pathlib.Path(__file__).parent / "cache" / "user{}.png".format(random.randint(1, 100000000))
            #             with open(_old_path, "wb") as f:
            #                 res = requests.get(_old_url)
            #                 f.write(res.content)
            #             _new_url = others.image_variation(_old_path)['data'][0]['url']
            #             _new_path = pathlib.Path(__file__).parent / "cache" / "{}.jpg".format(random.randint(1, 100000000))
            #             while _new_path.exists():
            #                 _new_path = pathlib.Path(__file__).parent / "cache" / "{}.jpg".format(random.randint(1, 100000000))
            #             with open(_new_path, "wb") as f:
            #                 res = requests.get(_new_url)
            #                 f.write(res.content)
            #             msg["[CQ:image,file=file://{},type=show,id=40004]".format(_new_path.as_posix().replace("/", "//"))] = user_id
            #         else:
            #             msg["输入的内容为空"] = user_id
            #     else:
            #         msg["密钥为空，无法请求"] = user_id
            elif "随机图片" in message:
                _img_path = pathlib.Path(__file__).parent / "cache" / "random{}.jpg".format(random.randint(1, 100000000))
                while _img_path.exists():
                    _img_path = pathlib.Path(__file__).parent / "cache" / "random{}.jpg".format(random.randint(1, 100000000))
                with open(_img_path, "wb+") as f:
                    res = others.random_image()
                    f.write(res.content)
                msg["[CQ:image,file=file://{},type=show,id=40004]".format(_img_path.as_posix().replace("/", "//"))] = user_id
            elif 'Status' in message:
                    msg["以下是全部任务视图:\n{}".format(task._task)] = user_id
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
                msg[_] = user_id

        for each in msg.keys():
            server.send_private_msg(msg[each], msg)
            time.sleep(safe_sleep)
        return True
    except BaseException as e:
        server.send_private_msg(user_id, "错误：\n{}".format(e))
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
            task.AddTask(Thread(target=logger.event, kwargs=dict(msg="收到{}群{}发送的请求 {}".format(request.json['group_id'], request.json['user_id'], request.json['raw_message']))), 1)
            task.AddTask(Thread(target=group_msg, args=(request.json['group_id'], request.json['user_id'], request.json['raw_message'], request.json['message_id'], Dates, API, DB)), 1)
        elif request.json['message_type'] == 'private':
            task.AddTask(Thread(target=private_msg, args=(request.json['user_id'], request.json['raw_message'], request.json['message_id'], Dates, API, DB)), 2)
    elif request.json["post_type"] == "meta_event":
        if request.json["meta_event_type"] == "heartbeat":
            task.AddTask(Thread(target=logger.event, kwargs=dict(msg="接收到心跳包，机器人在线")), 0)
    
    # 更新数据
    task.AddTask(Thread(target=retention, args=(server, Dates, PATH)), 0)
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