import flask
app = flask.Flask(__name__)

@app.route('/')
def index():
	return flask.render_template("index.html", pokename="charizard")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8081, debug=True)