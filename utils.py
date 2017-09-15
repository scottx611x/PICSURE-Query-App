import ast

import requests
import json
import time

from plotly import figure_factory
import plotly.offline as plotly_offline


from constants import (RUNNING_STATE, AVAILABLE_STATE, ERROR_STATE,
                       PLOTLY_TABLE_FONT_SIZE)


def _get(url, session=None):
    response = session.get(url, verify=False)
    assert response.status_code == 200
    return response


def get_secure_session(url):
    session = requests.session()
    _get(url, session=session)
    return session


def _post(session, url, afl_query=None, json_query=None):
    # TODO: Can we specify NHANES below here somewhere as well??

    if afl_query:
        query_string = {
            'where': [
                {
                    'field': {
                        'pui': '/SciDBAFL'
                    },
                    'predicate': 'AFL',
                    'fields': {'IQUERY': '{}'.format(afl_query)}
                }
            ]
        }
        print query_string
        post_data = query_string

    if json_query:
        post_data = json_query
        post_data = post_data.replace("&#34;", "\"")
        post_data = json.dumps(ast.literal_eval(post_data))
        post_data = json.loads(post_data)

    response = session.post(
        url,
        data=json.dumps(post_data),
        verify=False,
        headers={'Content-Type': 'application/json'}
    )
    return response


def _get_result_json(session, result_id, result_url):
    print "Fetching result JSON for resultId: {}".format(result_id)
    result_url = "{}/{}/JSON".format(result_url, result_id)
    return _get(result_url, session=session).json()


def get_scidb_query(session, url, result_service_url, result_url,
                    afl_query=None, json_query=None):
    if afl_query:
        query_response = _post(
            session,
            url,
            afl_query=afl_query
        ).json()

    if json_query:
        query_response = _post(
            session,
            url,
            json_query=json_query
        ).json()

    result_id = query_response["resultId"]
    result_id_url = "{}/{}".format(result_service_url, result_id)

    query_status = RUNNING_STATE
    while query_status != AVAILABLE_STATE:
        query = _get(result_id_url, session=session)
        query_status = query.json()["status"]
        if query_status == ERROR_STATE:
            return {"error": json.loads(query.content)["message"]}
        time.sleep(1)
        print "Still loading query from resultId: {}".format(result_id)

    print "Query from resultId: {} is available".format(result_id)
    return _get_result_json(session, result_id, result_url)


def generate_plotly_div(query_result):
    column_names = [column["name"] for column in query_result["columns"]]
    data_matrix = [column_names]

    for row in query_result["data"]:
        row_info = []
        for index, item in enumerate(row):
            column_name = column_names[index]
            if item.get(column_name):
                row_info.append(item[column_name])
            else:
                row_info.append("N/A")
        data_matrix.append(row_info)

    table = figure_factory.create_table(data_matrix)
    for i in range(len(table.layout.annotations)):
        table.layout.annotations[i].font.size = PLOTLY_TABLE_FONT_SIZE
    plot_div = plotly_offline.plot(
        table,
        include_plotlyjs=False,
        output_type='div'
    )
    return plot_div
