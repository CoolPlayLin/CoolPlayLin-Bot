# 贡献者指南

欢迎你对 CoolPlayLin-Bot 做出贡献！你可以成为 CoolPlayLin-Bot 的 Contributor

## 开发环境准备

- CoolPlayLin-Bot 使用 Python 语言开发，以 Flask 框架作为基础，所有你至少需要一个 Python3.8 以上的 Python 环境，最好使用 3.11 作为基础的开发环境
- 你可以使用 Python 自带的虚拟环境进行开发，可自行在网上查找，这里不做赘述

### 安装与运行

- 使用以下代码一键安装所需的依赖
```
python -m pip install -r requirements.txt
```
- 运行代码
```
python3 main.py
```

## Pull Request

首先，提交PR请将你的代码提交到主分支

**拉取规范**

1. 应当使用模板或者详细说明你更改了什么，优化了什么，添加了什么功能
2. 在检查没通过时，应及时查看代码是否有错误
3. 如果只是修改了文档文件而为修改代码，应在前面备注`[轻量级PR]`

**查找issue**

1. 如果你要开发issue中的功能，请评论表示你正在开发功能
2. 如果发现你开发的功能与issue中请求的功能一致，也应当表示你正在开发此功能

## **组织结构**
下面是 CoolPlayLin-Bot 代码结构

api
- `main.py` - CoolPlayLin-Bot的启动器
- `__init__.py` - 核心功能实现
- `api.py` - 存放需要调用到的API
- `typing.py` - 存放一些自定义数据类型
- `util.py` - 存放一些工具类
- `static` - 存放静态文件
- `template` - 存放GUI的网页文件

database
- `API.json` - 存放一些可自定义的数据
- `db.json` - 存放运行必须的数据