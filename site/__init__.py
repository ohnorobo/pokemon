import os
import sys
#incantation to fix python imports
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

import flask
import random
import compose

app = flask.Flask(__name__, static_folder="/var/www/pokemon/site/static")


names = [line.strip() for line in open("../pokemon_names.txt", "r")]
types = [line.strip() for line in open("../types.txt", "r")]


def randomize_name():
    return random.choice(names)


def random_types():
    return random.sample(types, 2)


@app.route('/')
def index():
    make_image()
    return flask.render_template("index.html", pokename=randomize_name(), type1=random_types()[0], type2=random_types()[1])


def make_image():
    compose.generate_image()


if __name__ == '__main__':
    host = "127.0.0.1"
    port = 8081
    app.debug = True
    app.run(host, port)