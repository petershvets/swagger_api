from collections import OrderedDict
import requests
import json
import argparse

# Logging
#Log levels
_MESSAGE = 0
_INFO = 1
_DEBUG = 2
_EXTRA = 3
_WARNING = -2
_ERROR = -1
_DEBUG_LEVEL = 2

# _DEBUG_CONF_LEVEL = {
#     "DEBUG": _DEBUG,
#     "EXTRA": _EXTRA,
#     "NORMAL": _INFO
# }

# we cane setup logging into a file later, for now output to console
_LOGGER = None

_MESSAGE_TEXT = {
    _MESSAGE: "",
    _INFO: "INFO: ",
    _ERROR: "ERROR: ",
    _EXTRA: "DEBUG: ",
    _DEBUG: "DEBUG: ",
    _WARNING: "WARNING: "
}

_REQUEST_TIMEOUT = 600

def debug (msg, level = _MESSAGE, json_flag = False):

    global _LOGGER

    if level <= _DEBUG_LEVEL :
        if json_flag:
            log_msg = json.dumps(msg, indent=4, separators=(',', ': '))
            print(log_msg)
            if _LOGGER:
                _LOGGER.info(log_msg)
        else:
            print(_MESSAGE_TEXT[level]+str(msg))
            if _LOGGER:
                _LOGGER.info(_MESSAGE_TEXT[level]+str(msg))
    return None

# Define API
SWAGGER_TODO_API={
    "GET_ALL_LISTS":("lists", requests.get),
    "CREATE_NEW_LIST":("lists", requests.post),
    "GET_LIST":("list/{}", requests.get),
    "ADD_NEW_TASK":("list/{}/tasks", requests.post),
    "UPDATE_TASK_STATUS":("list/{}/task/{}/complete", requests.post)
}

_get_all_lists =        "https://virtserver.swaggerhub.com/aweiker/ToDo/1.0.0/lists"
_get_all_lists_search = "https://virtserver.swaggerhub.com/aweiker/ToDo/1.0.0/lists?searchString=<search string>"
search =                "https://virtserver.swaggerhub.com/aweiker/ToDo/1.0.0/lists?searchString=MyList"

# Function processes properties json file
def get_json_prop(in_json_file):
    """ param:  in_json_file - fileobject returned by argparse
        Returns: Ordered dictionary of properties as defined in passed properties file
       Raises:
            json.decoder.JSONDecodeError: if config file is not valid JSON document
    """
    try:
        out_json_properties = json.load(in_json_file, encoding='utf-8', object_pairs_hook=OrderedDict)
        return out_json_properties
    except json.decoder.JSONDecodeError as json_err:
        debug("Provided config file {} is not valid JSON document".format(in_json_file), _ERROR)
        debug(json_err, _ERROR)
        #raise json_err.with_traceback(sys.exc_info()[2])
        exit(1)

# Function constructs and returns Looker REST API URL
def get_api_url(run_properties, api_uri, *params):
    """
    :param run_properties:
    :param api_uri: API request, like lists, etc.
    :return:
    """
    api_request = run_properties["api_host"] + "/" + run_properties["api_base_path"] + "/" + SWAGGER_TODO_API[api_uri][0]

    if params:
        api_request = api_request.format(*params)

    debug("Constructed API URL: {}".format(api_request))
    return api_request

def run_api(run_properties, api_call_name, *api_params, in_payload=False):
    """
    :param run_properties:
    :param api_call_name:
    :param api_params: optional
    :param in_payload:
    :return: raw response
    """

    # header_content = {"Authorization": "token " + in_access_token}

    api_url = get_api_url(run_properties, api_call_name, *api_params)
    if not in_payload:
        r = SWAGGER_TODO_API[api_call_name][1](api_url, verify=False, timeout=_REQUEST_TIMEOUT)
    else:
        r = SWAGGER_TODO_API[api_call_name][1](api_url, json=in_payload, verify=False,  timeout=_REQUEST_TIMEOUT)

    return r

# Function processes Looker REST API request response codes
def get_response_code(in_raw_response):
    """
    :param in_raw_response:
    :return: dictionary in a form {'Response': '<code value>'}
    """
    status_response_code = str(in_raw_response)
    for iter_char in ['<', '>', '[', ']']:
        if iter_char in status_response_code:
            status_response_code = status_response_code.replace(iter_char, '')

    status_response_code_l = status_response_code.split()
    status_response_code_d = dict([(k, v) for k, v in zip(status_response_code_l[::2], status_response_code_l[1::2])])
    status_response_code = int(status_response_code_d["Response"])
    return status_response_code

def get_all_lists(run_properties):
    # _get_all_lists = "https://virtserver.swaggerhub.com/aweiker/ToDo/1.0.0/lists"
    r = run_api(run_properties, "GET_ALL_LISTS")
    resp_code = get_response_code(r)

    # uncomment for debugging
    # debug("Header content:\n{}".format(r.headers))
    # debug("Status: {}".format(r.headers.get("status")))
    # debug("Status: {}".format(resp_code))
    if resp_code == 200:
        body = r.json()
        # debug("TODO lists:\n{}".format(body), _INFO, json_flag=True)
        return body
    elif resp_code == 400:
        debug("Bad Input Parameter", _WARNING)
        return False
    else:
        debug("Unknown code", _WARNING)

def get_list(run_properties, list_id):

    r = run_api(run_properties, "GET_LIST", list_id)
    resp_code = get_response_code(r)
    if resp_code == 200:
        body = r.json()
        debug("Looking up TODO list with ID: {}".format(list_id), _INFO)
        debug("Found TODO list:\n{}".format(body), _INFO)
        return body
    elif resp_code == 400:
        debug("Invalid ID supplied", _WARNING)
    elif resp_code == 404:
        debug("List with ID {} not found", _WARNING)
    else:
        debug("Unknown code", _WARNING)

def create_new_list(run_properties):
    """
    :param run_properties:
    :return: response header or False
    """
    # _create_new_list = "https://virtserver.swaggerhub.com/aweiker/ToDo/1.0.0/lists"
    payload = {
        "id": "d290f1ee-6c54-4b01-90e6-d701748f0852",
        "name": "Employment",
        "description": "The list of tasks that need to be done to start new employment",
        "tasks": [
                    {
                        "id": "0e2ac84f-f723-4f24-878b-44e63e7ae581",
                        "name": "learn Spark",
                        "completed": False
                    },
                    {"id": "0e2ac84f-f723-4f24-878b-44e63e7ae582",
                     "name": "learn Python",
                     "completed": False
                     }
                ]
    }

    r = run_api(run_properties, "CREATE_NEW_LIST", in_payload=payload)
    resp_code = get_response_code(r)
    if resp_code == 201:
        # body = r.json()
        res_header = r.headers
        debug("New list: {}".format(res_header))
        return res_header
    elif resp_code == 400:
        debug("Invalid input", _WARNING)
    elif resp_code == 409:
        debug("Item already exists", _WARNING)
    else:
        debug("Unknown code {}".format(resp_code), _WARNING)


def add_new_task(run_properties, list_id):
    """
    :param run_properties:
    :param list_id:
    :return: response header
    """
    uri = "https://virtserver.swaggerhub.com/aweiker/ToDo/1.0.0/list/d290f1ee-6c54-4b01-90e6-d701748f0851/tasks"
    # Payload can be passed into the function:
    # through properties file or in main flow from some other function.
    #

    payload = {
                "id": "0e2ac84f-f723-4f24-878b-44e63e7ae583",
                "name": "trim trees",
                "completed": True
              }

    r = run_api(run_properties, "ADD_NEW_TASK", list_id, in_payload=payload)
    resp_code = get_response_code(r)
    if resp_code == 201:
        res_header = r.headers
        debug("New task: {}".format(res_header))
        return res_header
    elif resp_code == 400:
        debug("Invalid input", _WARNING)
    elif resp_code == 409:
        debug("Item already exists", _WARNING)
    else:
        debug("Unknown code {}".format(resp_code), _WARNING)


def update_task_status(run_properties, list_id, task_id):
    """
    :param run_properties:
    :param list_id:
    :param task_id:
    :return: response header
    """
    payload = {
                "completed": True
              }

    r = run_api(run_properties, "UPDATE_TASK_STATUS", list_id, task_id, in_payload=payload)
    resp_code = get_response_code(r)
    if resp_code == 201:
        res_header = r.headers
        debug("Updated task: {}".format(res_header))
        return res_header
    elif resp_code == 400:
        debug("Invalid input, object invalid", _WARNING)
    else:
        debug("Unknown code {}".format(resp_code), _WARNING)

def main():
    # need to disable security warning
    # InsecureRequestWarning: Unverified HTTPS request is being made.Adding certificate verification is strongly advised.
    requests.packages.urllib3.disable_warnings()

    # Setup parsing command line arguments and app usage help
    parseArgs = argparse.ArgumentParser(description='Provide the following app arguments:')
    parseArgs.add_argument('-run_properties_file', type=argparse.FileType('r', encoding='UTF-8'),
                           help='Please provide json formatted properties file name', required=True,
                           default='run_properties.json')

    args = parseArgs.parse_args()
    debug("Reading run properties", _INFO)
    run_properties = get_json_prop(args.run_properties_file)

    # # do some setup if needed create app directories structure, enable logging into file
    # log_file_short_name = "looker_installer{}.log".format(get_date_timestamp())
    # log_file_name = os.path.join(APP_DEPLOYMENT_DIR_LOG, log_file_short_name)
    #
    # logging.basicConfig(filename=log_file_name, level=logging.INFO)
    # global _LOGGER
    # _LOGGER = logging.getLogger()

    debug("Get All TODO Lists", _INFO)
    current_lists = get_all_lists(run_properties)
    if current_lists:
        for li in current_lists:
            debug("TODO List Name: {}".format(li.get("name")), _INFO)
            debug(" List tasks", _INFO)
            task_list = li.get("tasks")
            for listtask in task_list:
                debug("     Task name: {}".format(listtask.get("name")), _INFO)
                debug("     Task completed: {}".format('Yes' if listtask.get("completed") else 'No'), _INFO)

    # Get list by ID
    debug("Obtain TODO list by ID", _INFO)
    get_list(run_properties, "3")
    # List lookup by ID does not work properly - no matter what ID is passed, API returns Home list

    # Create new list
    debug("Creating new TODO List", _INFO)
    create_new_list(run_properties)

    debug("Add New task to the list", _INFO)
    add_new_task(run_properties, 'd290f1ee-6c54-4b01-90e6-d701748f0851')

    debug("Update Task", _INFO)
    update_task_status(run_properties, "d290f1ee-6c54-4b01-90e6-d701748f0851", "0e2ac84f-f723-4f24-878b-44e63e7ae580")
# Main execution.
if __name__ == '__main__':
    main()
