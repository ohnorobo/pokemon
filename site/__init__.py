import flask
import random

app = flask.Flask(__name__, static_folder="/var/www/pokemon/html/static")


names = [line.strip() for line in open("../pokemon_names.txt", "r")]


def randomize_name():
    return random.choice(names)


def random_pokemon():
    numberstring = "{:0>3d}.png".format(random.choice(range(0, 151)))
    return numberstring

@app.route('/')
def index():
    return flask.render_template("index.html", pokename=randomize_name(), pokemon=random_pokemon())

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 8081
    app.debug = True
    app.run(host, port)