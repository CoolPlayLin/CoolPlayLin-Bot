import api
from flask import Flask
from flask import request
import time
import json

Post_Type_List = ['']

app = Flask(__name__)

def Logger(Message):
    with open("Run.log", "a", encoding='utf-8') as f:
        f.write("{} Message".format(time.strftime("%H:%M:%S")))


@app.route("/commit", methods=['POST'])
def Main():
    with open("Run.json", "a", encoding='utf-8') as f:
        f.write(json.dumps(request.json))
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5120)