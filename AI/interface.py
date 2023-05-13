import traceback
from flask import Flask, Response, request
import webbrowser

app = Flask(__name__)
@app.route("/")
def main():
    return 'Hello world'

