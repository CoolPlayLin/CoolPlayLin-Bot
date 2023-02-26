# CoolPlayLin-Bot
Go-cqhttp基于Flask的Python功能实现

## 启动项目

克隆本项目
```
clone https://github.com/CoolPlayLin/CoolPlayLin-Bot/
cd CoolPlayLin-Bot
```

安装依赖
```
python -m install -r requirements.txt
```

启动本项目
```
python3 main.py
```

## 使用须知

1. 本项目部分功能基于[高德API](https://lbs.amap.com/)，请在`API.json`的`keys`中把`amap`的值换成你的key
2. 本项目默认接受来自`5120`端口的POST，默认发送数据到`127.0.0.1:5700`
3. 可在config.json文件中修改`PostIP`和`AcceptPort`的值进行更改
4. 如果你在使用中遇到了问题，欢迎提交Issues为本项目做出贡献

## 相关项目

- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [flask](https://github.com/pallets/flask)
- [mdui](https://github.com/zdhxiong/mdui)