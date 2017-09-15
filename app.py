import urllib

import requests
from flask import Flask, request
from flask import render_template
from flask import jsonify

import plotly.figure_factory as figure_factory
import plotly.offline as plotly_offline

from utils import get_scidb_query, get_secure_session

BD2K_PICSURE_API_KEY = "p9328a0ukd626q5lb4s0iim3j7"
SSC_REST_URL = "https://ssc-dev.hms.harvard.edu/rest/v1"

TEAM_HOST = "team-07.aws.dbmi.hms.harvard.edu"
TEAM_REST_URL = "https://{}/SSC/rest".format(TEAM_HOST)

URL = SSC_REST_URL

PROCESS_SERVICE_URL = "{}/{}".format(URL, "processService")
QUERY_SERVICE_URL = "{}/{}".format(URL, "queryService/runQuery")
RESOURCE_SERVICE_URL = "{}/{}".format(URL, "resourceService/resources")
RESULT_SERVICE_URL = "{}/{}".format(URL, "resultService/")
RESULT_STATUS_URL = RESULT_SERVICE_URL + "resultStatus"
RESULT_URL = RESULT_SERVICE_URL + "result"

SECURITY_SERVICE_URL = "{}/{}".format(
    URL,
    "securityService/startSession?key={}".format(BD2K_PICSURE_API_KEY)
)
SYSTEM_SERVICE_URL = "{}/{}".format(URL, "systemService")

if URL == TEAM_REST_URL:
    session = requests.session()
else:
    session = get_secure_session(SECURITY_SERVICE_URL)

APP_TITLE = "AFL Query App"

AFL_RESULT_LIMIT = 10
PLOTLY_TABLE_FONT_SIZE = 10

app = Flask(__name__)
app.debug = True


@app.template_filter()
def decode_uri(uri):
    uri = urllib.unquote(uri).decode('utf8')
    return uri


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html', title=APP_TITLE)


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

    query_result = get_scidb_query(
        session,
        QUERY_SERVICE_URL,
        RESULT_STATUS_URL,
        RESULT_URL,
        afl_query=limited_afl_query
    )
    if query_result.get("error"):
        return jsonify(query_result)

    column_names = [column["name"] for column in query_result["columns"]]
    data_matrix = [column_names]

    for row in query_result["data"]:
        row_info = []
        for index, item in enumerate(row):
            column_name = column_names[index]
            row_info.append(item[column_name])
        data_matrix.append(row_info)
    table = figure_factory.create_table(data_matrix)
    for i in range(len(table.layout.annotations)):
        table.layout.annotations[i].font.size = PLOTLY_TABLE_FONT_SIZE
    plot_div = plotly_offline.plot(
        table,
        include_plotlyjs=False,
        output_type='div'
    )
    return jsonify({"table": plot_div})


if __name__ == "__main__":
    app.run()
