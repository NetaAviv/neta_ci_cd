# app.py
from flask import Flask
import time
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"

while True:
    time.sleep(1)
