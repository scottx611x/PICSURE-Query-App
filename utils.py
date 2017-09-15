import requests
import json
import time

from plotly import figure_factory
import plotly.offline as plotly_offline


from constants import RUNNING_STATE, AVAILABLE_STATE, ERROR_STATE, \
    PLOTLY_TABLE_FONT_SIZE


def get(url, session=None):
    response = session.get(url, verify=False)
    assert response.status_code == 200
    return response


def get_secure_session(url):
    session = requests.session()
    get(url, session=session)
    return session


def post(session, url, afl_query=None):
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
    post_data = json.dumps(query_string)
    response = session.post(url, data=post_data, verify=False)
    return response


def get_resources(session, url):
    resource_response = get(url, session=session)
    return [resource["name"] for resource in resource_response.json() if resource.get("name")]


def get_result_json(session, result_id, result_url):
    print "Fetching result JSON for resultId: {}".format(result_id)
    result_url = "{}/{}/JSON".format(result_url, result_id)
    response = get(result_url, session=session)
    return response.json()


def get_scidb_query(session, url, result_service_url, result_url, afl_query=None):
    query_response = post(
        session,
        url,
        afl_query=afl_query
    ).json()

    result_id = query_response["resultId"]
    result_id_url = "{}/{}".format(result_service_url, result_id)

    query_status = RUNNING_STATE
    while query_status != AVAILABLE_STATE:
        query = get(result_id_url, session=session)
        query_status = query.json()["status"]
        if query_status == ERROR_STATE:
            return {"error": json.loads(query.content)["message"]}
        time.sleep(1)
        print "Still loading query from resultId: {}".format(result_id)

    print "Query from resultId: {} is available".format(result_id)
    return get_result_json(session, result_id, result_url)


def generate_plotly_div(query_result):
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
    return plot_div
