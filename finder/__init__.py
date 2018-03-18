from flask import Flask
import time
import hashlib
import logging
import json
import os.path


logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('finder-access.log', mode='w')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(sh)


app = Flask('finder')
app.config['SECRET_KEY'] = str(hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest())

app.timetable = {}

if os.path.isfile("timetable.json"):
    with open("timetable.json", encoding="utf-8") as f:
        app.timetable = json.load(f)


import finder.models
import finder.controller
