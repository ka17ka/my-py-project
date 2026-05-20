import configparser
import yaml
import requests
import logging
import util

logger = logging.getLogger(__name__)

def get_config(env):
    config = configparser.ConfigParser()
    config.read('config.ini')
    base_url = config.get(env, 'base_url')
    authorization = config.get(env, 'authorization')
    sign = config.get(env, 'sign')
    gxsaas_auth = config.get(env, 'gxsaas-auth')
    atimestamp = config.get(env, 'atimestamp')

    return base_url, authorization, sign, gxsaas_auth, atimestamp

def get_test_data():
    with open('test_data.yaml', 'r', encoding='utf-8') as f:
        test_data = yaml.load(f, Loader=yaml.FullLoader)
        return test_data

def req_api(case_data,**kwargs):
    base_url, authorization, sign, gxsaas_auth, atimestamp = get_config(env="fat")
    gxsaas_auth = f"bearer {util.get_cached_token()}"
    logger.info(f"gxsaas_auth: {gxsaas_auth}")
    # test_data = get_test_data()
    test_req = case_data["request"]

    full_url = base_url +test_req["url"]
    logger.debug(f"请求URL: {full_url}")  # 调试信息用DEBUG级别
    headers = {"Authorization": authorization,"gxsaas-auth": gxsaas_auth,"sign": sign,"atimestamp": atimestamp}
    method =test_req["method"]
    response = None
    if method == "GET":
        param = test_req.get("param")
        if "param" in kwargs:
            param.update(kwargs["param"])
        response = requests.request(method, full_url, headers=headers, params=param)
        logger.info(f"请求方法: {method}, 请求参数: {param}")
    elif method == "POST":
        if test_req.get("data") and not test_req.get("param"):
            body = test_req["data"]
            if "body" in kwargs:
                body.update(kwargs["body"])
            response = requests.request(method, full_url, headers=headers, json=body)
            logger.info(f"请求方法: {method}, 请求体: {body}")
        elif test_req.get("param") and not test_req.get("data"):
            param = test_req["param"]
            if "param" in kwargs:
                param.update(kwargs["param"])
            response = requests.request(method, full_url, headers=headers, params=param)
            logger.info(f"请求方法: {method}, 请求参数: {param}")
        elif test_req.get("param") and test_req.get("data"):
            body = test_req["data"]
            param = test_req["param"]
            if "param" in kwargs:
                param.update(kwargs["param"])
            if "body" in kwargs:
                body.update(kwargs["body"])
            response = requests.request(method, full_url, headers=headers, json=body,params=param)
            logger.info(f"请求方法: {method}, 请求参数: {param}，请求体: {body}")

    return response

def assert_case_result(case_data,res):
    # 获取预期值
    expected_code = case_data["expect"]["code"]

    logger.info(f"开始测试断言验证，等待…")
    try:
        if res["code"] != expected_code:
            logger.warning(f"业务错误: {res.get('msg', '无错误信息')}")
        assert res["code"] == expected_code, f"测试断言验证失败,实际code: {res.get('code')}"
        logger.info("测试断言验证通过")
    finally:
        logger.info(f"测试用例:{case_data['name']}执行完毕")




















