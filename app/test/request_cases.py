import requests
from .common import log

cookies = 'session=eyJfZnJlc2giOmZhbHNlLCJsb2dnZWRfaW4iOnRydWV9.DklzlQ.7szQbkhxbnYwcC6Clv3aDq3HHDY'
logger = log.log()
def get_cases(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base):
    url = 'http://' + server + way
    print('用例:%s开始执行  url=%s  请求方式%s'%(case_name,url,request_method))
    result, text, code = assert_result(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base)
    return result, text, code

def case_request(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base):
    headers = {
        'Accept': 'application/json,text/plain,*/*',
        'Content-Type': 'application/json;charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'Cookie': cookies,
    }
    url = 'http://' + server + way
    if request_method == 'GET':
        try:
            response = requests.get(url,headers=headers)
        except:
            response = ''
            logger.info('%d--%s参数错误，请检查url,data,header是否正确'%(id_num,case_name))
    elif request_method == 'POST':
        if data_type == 'DATA':
            try:
                response = requests.post(url,data=data_i,headers=headers)
            except:
                response = ''
                logger.info('%d--%s参数错误，请检查url,data,header是否正确' % (id_num, case_name))
        elif data_type == 'FILE':
            files = {'file':open(data_i,'rb')}
            try:
                response = requests.post(url, files=files, headers=headers)
            except:
                response = ''
                logger.info('%d--%s参数错误，请检查url,data,header是否正确' % (id_num, case_name))
        else:
            response = ''
    elif request_method == 'PUT':
        try:
            response = requests.put(url,data=data_i,headers=headers)
        except:
            response = ''
            logger.info('%d--%s参数错误，请检查url,data,header是否正确' % (id_num, case_name))
    elif request_method == 'DELETE':
        try:
            response = requests.delete(url,data=data_i,headers=headers)
        except:
            response = ''
            logger.info('%d--%s参数错误，请检查url,data,header是否正确' % (id_num, case_name))
    return response

def assert_result(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base):
    try:
        response = case_request(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base)
        code = response.status_code
        text = response.text
    except:
        code = 404
        text = '参数错误，请检查url,data,header是否正确'
        result = 'error'
    logger.info('  ---预期结果%s' % check)
    # logger.info('  ---实际结果%s' % text)
    try:
        assert check in text
        logger.info('  --%s--正确' % case_name)
        result = 'success'
    except:
        result = 'fail'
    return result, text, code