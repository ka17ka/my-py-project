import configparser
import yaml
import time
import requests
import logging


logger = logging.getLogger(__name__)

def get_config(env="fat"):
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
# print(get_test_data()["add_distribution_cases"]["request"]["url"])

def req_api(case_data,env="fat",**kwargs):
    base_url, authorization, sign, gxsaas_auth, atimestamp = get_config(env)
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
        elif test_req.get("param") and test_req.get("param"):
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
    time.sleep(2)


# print(get_test_data()["add_distribution_cases"]["request"]["url"])
def wait_for_hardware_ready(hardware_id,timeout=20,interval=2):
    start_time = time.time()
    expect_dostate = get_test_data()["wait_for_hardware_ready_cases"]["expect"]["data"]["open_doState"]
    expect_distate = get_test_data()["wait_for_hardware_ready_cases"]["expect"]["data"]["open_diState"]
    expect_outstate = get_test_data()["wait_for_hardware_ready_cases"]["expect"]["data"]["open_outState"]
    base_url, authorization, sign, gxsaas_auth, atimestamp = get_config()
    full_url = base_url + get_test_data()["wait_for_hardware_ready_cases"]["request"]["url"]
    headers = {"Authorization": authorization, "gxsaas-auth": gxsaas_auth, "sign": sign, "atimestamp": atimestamp}
    # body = common.get_test_data()["wait_for_hardware_ready_cases"]["request"]["data"]
    param = {"id": hardware_id}
    method = get_test_data()["wait_for_hardware_ready_cases"]["request"]["method"]

    while time.time() - start_time < timeout:
        try:
            response = requests.request(method, full_url, headers=headers,params=param)
            res = response.json()
            for r in res["data"]["loopRunDataList"]:
                if r["doState"] == expect_dostate and r["diState"] == expect_distate and r["outState"] == expect_outstate:
                    return True
        except Exception as e:
            print(f"设备状态未就绪: {e}")

        time.sleep(interval)
        print(f"等待设备启动中，已等待{int(time.time()-start_time)}秒")
    end_time = time.time()
    print(f"{int(start_time) * 1000}-{int(end_time) * 1000}")

    return False

def wait_for_hardware_close(hardware_id,timeout=20,interval=2):
    start_time = time.time()
    expect_dostate = get_test_data()["wait_for_hardware_ready_cases"]["expect"]["data"]["close_doState"]
    expect_distate = get_test_data()["wait_for_hardware_ready_cases"]["expect"]["data"]["close_diState"]
    expect_outstate = get_test_data()["wait_for_hardware_ready_cases"]["expect"]["data"]["close_outState"]
    base_url, authorization, sign, gxsaas_auth, atimestamp = get_config()
    full_url = base_url + get_test_data()["wait_for_hardware_ready_cases"]["request"]["url"]
    headers = {"Authorization": authorization, "gxsaas-auth": gxsaas_auth, "sign": sign, "atimestamp": atimestamp}
    # body = common.get_test_data()["wait_for_hardware_ready_cases"]["request"]["data"]
    param = {"id": hardware_id}
    method = get_test_data()["wait_for_hardware_ready_cases"]["request"]["method"]

    while time.time() - start_time < timeout:
        try:
            response = requests.request(method, full_url, headers=headers, params=param)
            res = response.json()
            for r in res["data"]["loopRunDataList"]:
                if r["doState"] == expect_dostate and r["diState"] == expect_distate and r["outState"] == expect_outstate:
                    return True
        except Exception as e:
            print(f"设备状态未关闭: {e}")

        time.sleep(interval)
        print(f"等待设备关闭中，已等待{int(time.time()-start_time)}秒")

    return False

def check_lampbase_switchstatus(test_special_lamppost,start_time,current_end_time,timeout=10,interval=2):
    expect_open_switchstatus = get_test_data()["check_lampbase_switchstatus_cases"]["expect"]["data"]["open_switchstatus"]
    expect_close_switchstatus = get_test_data()["check_lampbase_switchstatus_cases"]["expect"]["data"]["close_switchstatus"]

    base_url, authorization, sign, gxsaas_auth, atimestamp = get_config()
    full_url = base_url + get_test_data()["check_lampbase_switchstatus_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    # body = get_test_data()["check_lampbase_switchstatus_cases"]["request"]["data"]
    method = get_test_data()["check_lampbase_switchstatus_cases"]["request"]["method"]
    while time.time() - start_time < timeout:
        # current_end_time = time.time()
        try:
            param = {"current": 1, "size": 15, "lampPostId": test_special_lamppost, "beginTime": int(start_time)*1000, "endTime": int(current_end_time)*1000}
            print(f"{int(start_time)*1000}-{int(current_end_time)*1000}")
            response = requests.request(method, full_url, headers=headers,params=param)
            res = response.json()
            if res["data"]["records"]:
                pos1_switchstatus = None
                pos2_switchstatus = None
                for r in res["data"]["records"]:
                    if r["position"] == 1:
                        pos1_switchstatus = r["switchStatus"]
                    elif r["position"] == 2:
                        pos2_switchstatus = r["switchStatus"]
                if pos1_switchstatus == expect_open_switchstatus and pos2_switchstatus == expect_open_switchstatus:
                    return True
                elif pos1_switchstatus == expect_close_switchstatus and pos2_switchstatus == expect_close_switchstatus:
                    return True
        except Exception as e:
            print(f"运行数据暂未上报,{e}")

        time.sleep(interval)
        current_end_time += interval
        print(current_end_time)

        print(f"等待运行数据上报中，已等待{int(time.time() - start_time)}秒")
    return False

def check_lampbase_dimming(test_special_lamppost,start_time,current_end_time,timeout=10,interval=2):
    expect_main_dimminglevel = get_test_data()["check_lampbase_dimmingLevel_cases"]["expect"]["data"]["main_dimmingLevel"]
    expect_side_dimminglevel = get_test_data()["check_lampbase_dimmingLevel_cases"]["expect"]["data"]["side_dimmingLevel"]

    base_url, authorization, sign, gxsaas_auth, atimestamp = get_config()
    full_url = base_url + get_test_data()["check_lampbase_dimmingLevel_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    # body = get_test_data()["check_lampbase_dimmingLevel_cases"]["request"]["data"]
    method = get_test_data()["check_lampbase_dimmingLevel_cases"]["request"]["method"]
    while time.time() - start_time < timeout:
        # current_end_time = time.time()
        try:
            param = {"current": 1, "size": 15, "lampPostId": test_special_lamppost, "beginTime": int(start_time)*1000, "endTime": int(current_end_time)*1000}
            print(f"{int(start_time)*1000}-{int(current_end_time)*1000}")
            response = requests.request(method, full_url, headers=headers,params=param)
            res = response.json()
            if res["data"]["records"]:
                pos1_dimminglevel = None
                pos2_dimminglevel = None
                for r in res["data"]["records"]:
                    if r["position"] == 1:
                        pos1_dimminglevel = r["dimmingLevel"]
                    elif r["position"] == 2:
                        pos2_dimminglevel = r["dimmingLevel"]
                if pos1_dimminglevel == expect_main_dimminglevel and pos2_dimminglevel == expect_side_dimminglevel:
                    return True
        except Exception as e:
            print(f"运行数据暂未上报,{e}")

        time.sleep(interval)
        current_end_time += interval
        print(current_end_time)

        print(f"等待运行数据上报中，已等待{int(time.time() - start_time)}秒")
    return False





















