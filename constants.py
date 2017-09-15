# API States
AVAILABLE_STATE = "AVAILABLE"
RUNNING_STATE = "RUNNING"
ERROR_STATE = "ERROR"

# API key
BD2K_PICSURE_API_KEY = "p9328a0ukd626q5lb4s0iim3j7"

# Hosts
SSC_REST_URL = "https://ssc-dev.hms.harvard.edu/rest/v1"
TEAM_HOST = "team-03.aws.dbmi.hms.harvard.edu"
TEAM_REST_URL = "https://{}/SSC/rest".format(TEAM_HOST)

API_URL = SSC_REST_URL

# Endpoints
PROCESS_SERVICE_URL = "{}/{}".format(API_URL, "processService")
QUERY_SERVICE_URL = "{}/{}".format(API_URL, "queryService/runQuery")
RESOURCE_SERVICE_URL = "{}/{}".format(API_URL, "resourceService/resources")
RESULT_SERVICE_URL = "{}/{}".format(API_URL, "resultService/")
RESULT_STATUS_URL = RESULT_SERVICE_URL + "resultStatus"
RESULT_URL = RESULT_SERVICE_URL + "result"

SECURITY_SERVICE_URL = "{}/{}".format(
    API_URL,
    "securityService/startSession?key={}".format(BD2K_PICSURE_API_KEY)
)
SYSTEM_SERVICE_URL = "{}/{}".format(API_URL, "systemService")

AFL_RESULT_LIMIT = 10
APP_TITLE = "AFL Query App"
GITHUB_URL = "https://github.com/scottx611x/afl-querier"
PLOTLY_TABLE_FONT_SIZE = 10
