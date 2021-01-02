from flask import Flask, url_for , Response

import os
app = Flask(__name__)



app.config['SECRET_KEY'] = os.urandom(24) 


@app.route("/")
def test():
    with open("static/test.txt", "r") as f:
        content = f.read()
    return('worked')


if __name__ == "__main__":
    app.run(debug = True)