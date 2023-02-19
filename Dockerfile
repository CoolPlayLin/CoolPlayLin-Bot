FROM python:3.11.2-buster
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN curl -sSL -o go-cqhttp.tar.gz https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc4/go-cqhttp_linux_amd64.tar.gz \
    && tar -zxvf go-cqhttp.tar.gz \
    && rm go-cqhttp.tar.gz

# 设置config.yml文件
COPY config.yml ./go-cqhttp/
ENV GO_CQHTTP_CONFIG_PATH=/app/go-cqhttp/config.yml

# 暴露端口
EXPOSE 5120

CMD ["/app/go-cqhttp/go-cqhttp", "-c", "/app/go-cqhttp/config.yml", "&&", "python3", "app.py"]