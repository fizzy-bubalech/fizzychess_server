
from flask import Flask, url_for , Response

import os
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24) 


from server import routes