import flask
import pytest
import rafi


@pytest.fixture
def app():
    demo = rafi.App("demo_app")

    @demo.route("/")
    def index():
        return "index"

    @demo.route("/", methods=["POST"])
    def post():
        return "POST"

    @demo.route("/hello/<param>")
    def param(param):
        return "hello {}".format(param)

    @demo.route("/code/<code>")
    def code(code=200):
        return "code: {}".format(code), code

    @demo.route("/query")
    def query():
        return demo.request.args.get("query")

    return demo


@pytest.fixture
def req():
    return flask.Flask(__name__)


def test_index_get(app, req):
    with req.test_request_context(method="GET"):
        res = app(flask.request)
        assert res[0] == "index"
        assert res[1] == 200


def test_index_post(app, req):
    with req.test_request_context(method="POST"):
        res = app(flask.request)
        assert res[0] == "POST"
        assert res[1] == 200


def test_hello_world(app, req):
    with req.test_request_context(path="/hello/world", method="GET"):
        res = app(flask.request)
        assert res[0] == "hello world"
        assert res[1] == 200


def test_status_code(app, req):
    with req.test_request_context(path="/code/400", method="GET"):
        res = app(flask.request)
        assert res[0] == "code: 400"
        assert res[1] == "400"


def test_not_found(app, req):
    with req.test_request_context(path="/foo"):
        res = app(flask.request)
        assert res[0] == ""
        assert res[1] == 404


def test_wrong_method(app, req):
    with req.test_request_context(method="DELETE"):
        res = app(flask.request)
        assert res[0] == ""
        assert res[1] == 405


def test_empty_path(app, req):
    with req.test_request_context(method="GET"):
        flask.request.path = ""
        res = app(flask.request)
        assert res[0] == "index"
        assert res[1] == 200


def test_request_object(app, req):
    with req.test_request_context(path="/query?query=1234"):
        res = app(flask.request)
        assert res[0] == "1234"
        assert res[1] == 200
