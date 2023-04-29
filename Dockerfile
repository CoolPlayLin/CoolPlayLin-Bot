FROM python:3.11.3-bullseye

WORKDIR /app
COPY . .

RUN mkdir server \
    && curl -sSL -o go-cqhttp.tar.gz https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0/go-cqhttp_linux_amd64.tar.gz \
    && tar -zxvf go-cqhttp.tar.gz \
    && mv go-cqhttp config.yml ./server/ \
    && rm go-cqhttp.tar.gz LICENSE README.md

# 设置config.yml文件
ENV GO_CQHTTP_CONFIG_PATH=/app/server/config.yml

# 安装全部依赖
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt --upgrade
RUN python -m pip install pyyaml --upgrade

# 暴露端口
EXPOSE 5120

CMD ["python3", "app.py"]