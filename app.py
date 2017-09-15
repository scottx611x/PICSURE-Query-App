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


@app.route('/afl-table', methods=['GET'])
def afl_table():
    afl_query = request.args.get('query', '')
    return render_template(
        'display-table-from-afl-query.html',
        afl_query=afl_query,
        title=APP_TITLE
    )


@app.route('/afl-table-no-limit', methods=['GET'])
def afl_table_no_limit():
    afl_query = request.args.get('query', '')
    return render_template(
        'display-table-from-afl-query-no-limit.html',
        afl_query=afl_query,
        title=APP_TITLE
    )


@app.route('/json-table', methods=['GET'])
def json_table():
    json_query = request.args.get('query', '')
    return render_template(
        'display-table-from-json-query.html',
        json_query=json_query,
        title=APP_TITLE
    )


@app.route('/scidb-afl-no-limit', methods=['POST'])
def scidb_afl_no_limit():
    afl_query = request.form["query"].replace("&#39;", "'")
    afl_query = afl_query.replace("&gt;", ">")
    afl_query = afl_query.replace("&lt;", "<")

    query_result = u.get_scidb_query(
        session,
        QUERY_SERVICE_URL,
        RESULT_STATUS_URL,
        RESULT_URL,
        afl_query=afl_query
    )
    if query_result.get("error"):
        return jsonify(query_result)

    return jsonify(
        {
            "table": u.generate_plotly_div(query_result)
        }
    )

@app.route('/scidb-afl', methods=['POST'])
def scidb_afl():
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


@app.route('/scidb-json', methods=['POST'])
def scidb_json():
    json_query = request.form["query"].replace("&#39;", "'")

    query_result = u.get_scidb_query(
        session,
        QUERY_SERVICE_URL,
        RESULT_STATUS_URL,
        RESULT_URL,
        json_query=json_query
    )
    if query_result.get("error"):
        return jsonify(query_result)

    return jsonify(
        {
            "table": u.generate_plotly_div(query_result)
        }
    )


@app.route('/gene-data', methods=['POST'])
def gene_data():
    afl_query = request.form["query"].replace("&#39;", "'")

    query_result = u.get_scidb_query(
        session,
        QUERY_SERVICE_URL,
        RESULT_STATUS_URL,
        RESULT_URL,
        afl_query=afl_query
    )
    if query_result.get("error"):
        return jsonify(query_result)

    ref_gene_id = query_result["columns"][1]["name"]
    gene_names = []

    for row in query_result["data"]:
        for item in row:
            if item.get(ref_gene_id):
                gene_names.append(item[ref_gene_id])

    return jsonify(
        {
            "gene_names": gene_names
        }
    )

if __name__ == "__main__":
    app.run("0.0.0.0")
