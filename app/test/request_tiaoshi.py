import requests

def get_cases(id_num, name, server, ways, request_method, data_i, data, check, is_base, org_name, module_name):
    code = case_request(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base)
    return code

def case_request(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base):
    url = 'http://' + server + way
    print('用例：%s 请求方式:%s  url:%s  data:%s' % (case_name,request_method,url,data_i))
    if request_method == 'GET':
        try:
            responese = requests.get(url)
            code = responese.status_code
        except:
            code = 404
    elif request_method == 'POST':
        try:
            responese = requests.post(url,data=data_i)
            code = responese.status_code
        except:
            code = 404
    elif request_method == 'PUT':
        try:
            responese = requests.put(url,data=data_i)
            code = responese.status_code
        except:
            code = 404
    elif request_method == 'DELETE':
        try:
            responese = requests.delete(url,data=data_i)
            code = responese.status_code
        except:
            code = 404
    return code