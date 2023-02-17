FROM python:3.11.2-slim-buster
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
EXPOSE 5120
CMD ["python3", "main.py"]