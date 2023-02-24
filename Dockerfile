FROM python:3.11.2-buster
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

RUN mkdir server \
    && curl -sSL -o go-cqhttp.tar.gz https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc4/go-cqhttp_linux_amd64.tar.gz \
    && tar -zxvf go-cqhttp.tar.gz \
    && mv go-cqhttp config.yml ./server/ \
    && rm go-cqhttp.tar.gz LICENSE README.md

# 设置config.yml文件
ENV GO_CQHTTP_CONFIG_PATH=/app/server/config.yml

# 暴露端口
EXPOSE 5120

CMD ["/app/server/go-cqhttp", "-c", "/app/server/config.yml", "&", "python3", "main.py"]