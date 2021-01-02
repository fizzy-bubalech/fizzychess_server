from flask import Flask, url_for , Response

from server import app

@app.route("/")
def test():
    return('worked')

