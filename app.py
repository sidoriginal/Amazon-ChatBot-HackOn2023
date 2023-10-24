from flask import Flask, render_template, request, jsonify
from _main import handle_response, get_wit_response
import torch

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)

@app.route("/get_result", methods=["GET"])
def get_result():
    from _main import result
    if result:
        # Assuming result is a list of dictionaries, each containing product info
        return result
    else:
        return "Still processing. Please wait."

def get_Chat_response(text):
    wit_response = get_wit_response(text)
    bot_reply = handle_response(wit_response)
    open('test.csv', 'w').close()
    return bot_reply

if __name__ == '__main__':
    app.run()
