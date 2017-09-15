import urllib

import requests
from flask import Flask, jsonify, request, redirect, render_template

from constants import (APP_TITLE, API_URL, GITHUB_URL,
                       TEAM_REST_URL, SECURITY_SERVICE_URL,
                       QUERY_SERVICE_URL, RESULT_STATUS_URL, RESULT_URL,
                       AFL_RESULT_LIMIT)
import utils as u

# No auth needed if hitting our sandboxed instance
if API_URL == TEAM_REST_URL:
    session = requests.session()
else:
    session = u.get_secure_session(SECURITY_SERVICE_URL)

app = Flask(__name__)
app.debug = True


@app.template_filter()
def decode_uri(uri):
    uri = urllib.unquote(uri).decode('utf8')
    return uri


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html', title=APP_TITLE)


@app.route('/github', methods=['GET'])
def github():
    return redirect(GITHUB_URL, code=302)


@app.route('/table', methods=['GET'])
def table():
    afl_query = request.args.get('query', '')
    return render_template(
        'display-table.html',
        afl_query=afl_query,
        title=APP_TITLE
    )


@app.route('/scidb', methods=['POST'])
def scidb():
    afl_query = request.form["query"].replace("&#39;", "'")
    limited_afl_query = "limit({}, {})".format(afl_query, AFL_RESULT_LIMIT)

    query_result = u.get_scidb_query(
        session,
        QUERY_SERVICE_URL,
        RESULT_STATUS_URL,
        RESULT_URL,
        afl_query=limited_afl_query
    )
    if query_result.get("error"):
        return jsonify(query_result)

    return jsonify(
        {
            "table": u.generate_plotly_div(query_result)
        }
    )


if __name__ == "__main__":
    app.run("0.0.0.0")
