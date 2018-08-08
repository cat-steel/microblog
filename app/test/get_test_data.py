import json
import requests
def get_test_data(case_name, IP, way, request_method, data_i, data, check, is_base):
    test_data = {
        'case_name': case_name,
        'IP': IP,
        'way': way,
        'request_method': request_method,
        'data_i': data_i,
        'data': data,
        'check': check,
        'is_base': is_base,
    }
    url = 'http://' + test_data.get('IP') + test_data.get('way')
    datas = test_data.get('data')
    print(url, datas)
    try:
        request_cose = request_case(url, datas)
    except:
        request_cose = 404
    return request_cose

def request_case(url,data):
    response = requests.post(url,data=data)
    cose = response.status_code
    return cose