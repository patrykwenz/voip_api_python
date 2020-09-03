import requests

URL = "http://0.0.0.0:5000"
ENDPOINT_NEW_USER = "/add-user-to-sip-exten-conf/"
ENDPOINT_SIP_FILE = "/sip-file-lookup"
ENDPOINT_USER_STATUS_RDY = "/update-status-rdy/"
ENDPOINT_USER_STATUS_BUSY = "/update-status-busy/"
ENDPOINT_PEER = "/get-peer/"


def get_delete_info(req, info):
    print(f"{info}")
    print(f"request.url: {req.url}")
    print(f"request.status_code: {req.status_code}")
    print(f"request.headers: {req.headers}")
    print(f"request.text: {req.text}")
    print(f"request.request.headers: {req.request.headers}")


def post_info(req):
    print(f"POST")
    print(f"request.url: {req.url}")
    print(f"request.status_code: {req.status_code}")
    print(f"request.headers: {req.headers}")
    print(f"request.text: {req.text}")
    print(f"request.body: {req.request.body}")
    print(f"request.request.headers: {req.request.headers}")


def post_new_user(user_name):
    final_endpoint = URL + ENDPOINT_NEW_USER + str(user_name)
    req = requests.post(final_endpoint)
    post_info(req)


def get_sip_file():
    final_endpoint = URL + ENDPOINT_SIP_FILE
    req = requests.get(final_endpoint)
    get_delete_info(req, "GET")


def update_user_status_rdy(user_name):
    final_endpoint = URL + ENDPOINT_USER_STATUS_RDY + str(user_name)
    req = requests.put(final_endpoint)
    get_delete_info(req, "GET")


def update_user_status_busy(user_name):
    final_endpoint = URL + ENDPOINT_USER_STATUS_BUSY + str(user_name)
    req = requests.put(final_endpoint)
    get_delete_info(req, "GET")


def get_peer(user_name):
    final_endpoint = URL + ENDPOINT_PEER + str(user_name)
    req = requests.get(final_endpoint)
    get_delete_info(req, "GET")


def status():
    final_endpoint = URL + "/user-status"
    req = requests.get(final_endpoint)
    get_delete_info(req, "GET")


def status2():
    final_endpoint = URL + "/pair-status"
    req = requests.get(final_endpoint)
    get_delete_info(req, "GET")


def de(user_name):
    final_endpoint = URL + "/delete-user/" + str(user_name)
    req = requests.delete(final_endpoint)
    get_delete_info(req, "GET")


if __name__ == '__main__':
    u_name = "aa"
    u2_name = "bb"
    u3_name = "cc"

    status()
    status2()

    # get_sip_file()
    post_new_user(u_name)
    post_new_user(u3_name)
    post_new_user(u2_name)
    # update_user_status_rdy(u_name)
    # update_user_status_busy(u_name)
    #
    # status()
    # status2()
    # update_user_status_rdy(u3_name)
    # update_user_status_rdy(u2_name)
    # status()
    status()
    status2()
    #
    get_peer(u_name)
    get_peer(u2_name)
    get_peer(u3_name)
    de(u_name)
    de(u2_name)
    de(u3_name)
    status()
    status2()