import os
import sys
#incantation to fix python imports
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

import flask
import random
import compose

#app = flask.Flask(__name__, static_folder="/Users/slaplante/projects/pokemon/site/static")
app = flask.Flask(__name__, static_folder="/var/www/pokemon/site/static")


names = [line.strip() for line in open("../pokemon_names.txt", "r")]
types = [line.strip() for line in open("../types.txt", "r")]

length_units = ["m", "ft", "yards", "cm", "smts", "rod"]
weight_units = ["lbs", "kg", "drams", "stone", "mg"]


def randomize_name():
    return random.choice(names)

def random_types():
    return random.sample(types, 2)

def height():
  return str(round(random.uniform(.01, 100), 1)) + random.choice(length_units)

def weight():
  return str(round(random.uniform(.01, 100), 1)) + random.choice(weight_units)


@app.route('/')
def index():
    make_image()
    type_choice = random_types()
    return flask.render_template("index.html",
             pokename=randomize_name(),
             type1=type_choice[0],
             type2=type_choice[1],
             height=height(),
             weight=weight(),
             description="lololol")


def make_image():
    compose.generate_image()


if __name__ == '__main__':
    host = "127.0.0.1"
    port = 8081
    app.debug = True
    app.run(host, port)
