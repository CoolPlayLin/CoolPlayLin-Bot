# CoolPlayLin-Bot
Go-cqhttp基于Flask的Python功能实现

## 食用方法

**开箱即用**

- 克隆本项目
```
clone https://github.com/CoolPlayLin/CoolPlayLin-Bot/
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

1. 本项目部分功能基于[高德API](https://lbs.amap.com/)，请在`API.json`的`keys`中把`amap`的值换成你的key
2. 本项目集成ChatGPT问答功能，请在`API.json`的`keys`中的`chatgpt`的值换成你的token
3. 由于中国大陆的网络环境，你可以更改`API.json`中的`gptproxy`的值启用代理，通过代理服务器访问API
4. 本项目默认接受来自`5120`端口`/commit`路径的POST，默认发送数据到`127.0.0.1:5700`
5. 可在config.json文件中修改`PostIP`和`AcceptPort`的值进行更改
6. 如果你在使用中遇到了问题，欢迎提交Issues为本项目做出贡献

## 相关项目

- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [flask](https://github.com/pallets/flask)
- [mdui](https://github.com/zdhxiong/mdui)
- [revChatGPT](https://github.com/acheong08/ChatGPT)