# CoolPlayLin-Bot
Go-cqhttp基于Flask的Python功能实现

## 食用方法

**开箱即用**

- 克隆本项目
```
git clone https://github.com/CoolPlayLin/CoolPlayLin-Bot/
cd CoolPlayLin-Bot
```

- 安装依赖
```
python -m install -r requirements.txt
```

- 启动本项目
```
python3 main.py
```

**使用Docker部署**

- DockerHub
```
docker push coolplaylin/coolplaylin-bot:main
```
- Github
```
docker pull ghcr.io/coolplaylin/coolplaylin-bot:main
```

## 使用须知

1. 本项目部分功能基于[高德地图API](https://lbs.amap.com/)，请把`API.json`->`keys`->`amap`的值换成你的key
2. 本项目集成[ChatGPT](https://chat.openai.com/chat)问答功能，请把`API.json`->`keys`->`chatgpt`的值换成你的token
3. 本项目默认接受来自`5120`端口`/commit`路径的POST，默认发送数据到`127.0.0.1:5700`
4. 机器人GUI管理页面与接受POST的端口一致，路径为`/`
5. 可在`config.json`文件中修改`PostIP`和`AcceptPort`的值进行更改
6. 如果你在使用中遇到了问题，欢迎提交`issues`为本项目做出贡献

## 相关项目

- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [flask](https://github.com/pallets/flask)
- [mdui](https://github.com/zdhxiong/mdui)
- [revChatGPT](https://github.com/acheong08/ChatGPT)