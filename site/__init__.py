import os
import sys
import time

# STATIC_DIR = "/var/www/pokemon/site/static"

#incantation to fix python imports
thisdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(thisdir)
sys.path.insert(0, parentdir)

import flask
import random
import compose, markov

static_dir = os.path.join(thisdir, 'static')
app = flask.Flask(__name__, static_folder=static_dir)

names = [line.strip() for line in open("pokemon_names.txt", "r")]
types = [line.strip() for line in open("types.txt", "r")]

length_units = ["m", "ft", "yds", "cm", "smts", "rod"]
weight_units = ["lbs", "kg", "drams", "stone", "mg", "tons"]

recent_combos = []

def random_text(name, seed=None):
    text = markov.get_text(seed)
    text = text.replace("<NAME>", name)
    return text

def randomize_name(seed=None):
    random.seed(seed)
    return random.choice(names)

def random_types(seed=None):
    random.seed(seed)
    return random.sample(types, 2)

def height():
  return str(round(random.uniform(.01, 100), 1)) + random.choice(length_units)

def weight():
  return str(round(random.uniform(.01, 100), 1)) + random.choice(weight_units)

def get_image_filename(ids):
    return "-".join(map(str,ids[:3])) + ".png"

def get_url(ids):
    return "-".join(map(str, ids))

def make_image(seed=None):
    return compose.generate_image(seed)

@app.route('/<ids>')
def id_index(ids):
    ids = ids.split('-')
    try:
      seed = ids[3]
    except:
      seed = int(time.time()*1000)

    filename = get_image_filename(ids)
    name=randomize_name(seed)
    type_choice = random_types(seed)
    description = random_text(name, seed)

    if not os.path.isfile("site/static/imgs/generated/"+filename):
      return flask.render_template("index.html",
               pokename=name,
               image="missingno.png",
               type1=type_choice[0],
               type2=type_choice[1],
               height=height(),
               weight=weight(),
               url = "",
               description=description.decode('utf-8'))

    else:
      return flask.render_template("index.html",
               pokename=name,
               image=filename,
               type1=type_choice[0],
               type2=type_choice[1],
               height=height(),
               weight=weight(),
               url = "",
               description=description.decode('utf-8'))


@app.route('/')
def index():
    seed = int(time.time()*1000)

    ids = make_image(seed)
    name=randomize_name(seed)
    type_choice = random_types(seed)
    description = random_text(name, seed)

    return flask.render_template("index.html",
             pokename=name,
             image=get_image_filename(ids),
             type1=type_choice[0],
             type2=type_choice[1],
             height=height(),
             weight=weight(),
             url=get_url(ids),
             description=description.decode('utf-8'))


if __name__ == "__main__":
    app.debug = True

    host="127.0.0.1"
    port=80    #run on 80 by default

    if sys.argv[1]: #run on port given from heroku
        host = sys.argv[1]
    if sys.argv[2]: #run on host given from heroku
        port = sys.argv[2]

    app.run(host=host, port=int(port))
