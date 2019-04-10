import requests


def request_app1(APP1_HOST):
    r = requests.get(APP1_HOST + '/app1/api/')
    if r.status_code == 200:
        return 'app1 right'
    else:
        return 'app1 wrong'


def request_app2(APP2_HOST):
    requests.get(APP2_HOST + '/app2/api/')
    return 'app2'


def request_two_apps(APP1_HOST, APP2_HOST):
    a = request_app1(APP1_HOST)
    b = request_app2(APP2_HOST)
    return a + b
