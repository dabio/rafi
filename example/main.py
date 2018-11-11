import rafi

app = rafi.App(__name__)


@app.route("/hello/<name>")
def hello(name):
    return "hello {}".format(name)
