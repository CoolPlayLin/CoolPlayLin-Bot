FROM python:3.11.2-slim-buster
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]