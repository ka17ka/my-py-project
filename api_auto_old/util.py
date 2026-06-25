import time
import logging
import common
import json
import os
import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import base64

logger = logging.getLogger(__name__)

# 平台RSA加密公钥
PUBLIC_KEY_PEM = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCroUafvWBEVSH6uR9YaeFDWwqm
0mH0s6d1a+qXjNRe7ZG4p+Q8jYcwydBYR9/NxSCkR9Kw623+YSOp8Bd62XZeB10x
pEmGO1HPneSBCUlxxUPcoA3NNK257AKZcX2lFvCAfUYWcciYZqyzqTU+EVogSbrh
Ab6zGmC0x+FlnYLQQwIDAQAB
-----END PUBLIC KEY-----
"""

# 将公钥解读为可用字段
public_key = serialization.load_pem_public_key(
    PUBLIC_KEY_PEM.encode()
)

def rsa_encrypt(key):
    """
    获取平台固定公钥，RSA加密登录密码等数据
    :param key: 登录密码等
    :return: 返回加密后的值
    """
    plaintext_bytes = key.encode()
    ciphertext = public_key.encrypt(
        plaintext_bytes,
        padding.PKCS1v15()
    )

    return base64.b64encode(ciphertext).decode('utf-8')

def login_api():
    """
    token过期后，重新登录
    :return: 返回重新登录后的token
    """
    base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config(env="fat")
    password = rsa_encrypt("Ttxs6226510")

    login_case_data = common.get_test_data()["get_login_token"]
    login_req = login_case_data["request"]
    login_req["data"]["password"] = password
    full_url = base_url + login_req["url"]
    headers = {"Authorization": authorization, "gxsaas-auth": gxsaas_auth, "sign": sign, "atimestamp": atimestamp}
    method = login_req["method"]
    body = login_req["data"]
    response = requests.request(method, full_url, headers=headers, json=body)
    logger.info(f"请求方法: {method}, 请求体: {body}")
    res = response.json()

    return res["data"]["accessToken"]

def write_cached_token(token,expires_at):
    """
    创建cache_token.json文件，写入token和过期时间
    :param token: token
    :param expires_at: 过期时间
    :return:
    """
    with open('cache_token.json', 'w') as f:
        json.dump({"token": token, "expires_at": expires_at}, f)

def read_cached_token():
    """
    读取cache_token.json文件中的token和过期时间，没有找到文件或读取失败返回None和0
    :return: 读取到的token和过期时间，未读取返回None和0
    """
    if not os.path.exists("cache_token.json"):
        return None,0
    try:
        with open('cache_token.json', 'r') as f:
            data = json.load(f)
            token = data.get("token")
            expires_at = data.get("expires_at",0)
        return token, expires_at
    except Exception as e:
        return None,0

def get_cached_token():
    """
    读取cache_token.json文件，token为None或已过期，则调用login_api()重新生成token，并写入到cache_token.json文件；
    不为None且未过期则直接s使用文件中的token
    :return:
    """
    token, expires_at = read_cached_token()
    current_time = time.time()
    if token and current_time < expires_at:
        logger.info("使用缓存 token，未重新登录")
        return token

    logger.info("调用 login_api() 获取新 token")
    access_token = login_api()
    token = access_token
    expires_at = current_time + 360000
    write_cached_token(token, expires_at)

    return token

def wait_for_hardware_ready(special_hardware_id,timeout=20,interval=2):
    """
    轮询检查监控箱启动状态，达成条件返回True
    :param special_hardware_id:
    :param timeout:
    :param interval:
    :return:
    """
    start_time = time.time()
    case_data = common.get_test_data()["wait_for_hardware_ready_cases"]
    expect_dostate = case_data["expect"]["data"]["open_doState"]
    expect_distate = case_data["expect"]["data"]["open_diState"]
    expect_outstate = case_data["expect"]["data"]["open_outState"]

    param = case_data["request"]["param"]
    param["id"] = special_hardware_id

    while time.time() - start_time < timeout:
        try:
            response = common.req_api(case_data,param = param)
            res = response.json()
            for r in res["data"]["loopRunDataList"]:
                if (r["loopName"] == 1 and
                    r["doState"] == expect_dostate and
                    r["diState"] == expect_distate and
                    r["outState"] == expect_outstate):
                    return True
        except Exception as e:
            logger.info(f"设备状态未就绪: {e}")

        time.sleep(interval)
        logger.info(f"等待设备启动中，已等待{int(time.time()-start_time)}秒")
    end_time = time.time()
    logger.info(f"{int(start_time) * 1000}-{int(end_time) * 1000}")
    return False

def wait_for_hardware_close(special_hardware_id,timeout=20,interval=2):
    """
    轮询检查监控箱关闭状态，达成条件返回True
    :param special_hardware_id:
    :param timeout:
    :param interval:
    :return:
    """
    start_time = time.time()
    case_data = common.get_test_data()["wait_for_hardware_ready_cases"]
    expect_dostate = case_data["expect"]["data"]["close_doState"]
    expect_distate = case_data["expect"]["data"]["close_diState"]
    expect_outstate = case_data["expect"]["data"]["close_outState"]

    param = case_data["request"]["param"]
    param["id"] = special_hardware_id

    while time.time() - start_time < timeout:
        try:
            response = common.req_api(case_data,param = param)
            res = response.json()
            for r in res["data"]["loopRunDataList"]:
                if (r["loopName"] == 1 and
                    r["doState"] == expect_dostate and
                    r["diState"] == expect_distate and
                    r["outState"] == expect_outstate):
                    return True
        except Exception as e:
            logger.info(f"设备状态未关闭: {e}")

        time.sleep(interval)
        logger.info(f"等待设备关闭中，已等待{int(time.time()-start_time)}秒")
    end_time = time.time()
    logger.info(f"{int(start_time) * 1000}-{int(end_time) * 1000}")

    return False

def check_lampcontrol_list(test_special_lamppost,timeout=30,interval=2):
    """
    轮询检查监控箱开启后，灯具同步被打开，检查关联单灯是否上报工况，达成条件返回True
    :param test_special_lamppost:
    :param timeout:
    :param interval:
    :return:
    """
    start_time = time.time()
    current_end_time = time.time()
    case_data = common.get_test_data()["check_lampbase_switchstatus_cases"]
    # expect_open_switchstatus = case_data["expect"]["data"]["open_switchstatus"]
    # # expect_close_switchstatus = case_data["expect"]["data"]["close_switchstatus"]

    param = case_data["request"]["param"]
    param["lampPostId"] = test_special_lamppost

    while time.time() - start_time < timeout:
        try:
            param["beginTime"] = int(start_time) * 1000
            param["endTime"] = int(current_end_time) * 1000
            # param = {"current": 1, "size": 15, "lampPostId": test_special_lamppost, "beginTime": int(start_time)*1000, "endTime": int(current_end_time)*1000}
            logger.info(f"{int(start_time)*1000}-{int(current_end_time)*1000}")
            response = common.req_api(case_data, param=param)
            res = response.json()
            if res["data"]["records"]:
                pos1_switchstatus = None
                pos2_switchstatus = None
                for r in res["data"]["records"]:
                    if r["position"] == 1:
                        pos1_switchstatus = r["switchStatus"]
                    if r["position"] == 2:
                        pos2_switchstatus = r["switchStatus"]
                if pos1_switchstatus and pos2_switchstatus:
                        return True
                # elif pos1_switchstatus == expect_close_switchstatus and pos2_switchstatus == expect_close_switchstatus:
                # if pos1_switchstatus == expect_close_switchstatus:
                #     return True
        except Exception as e:
            logger.info(f"运行数据暂未上报,{e}")
        time.sleep(interval)
        current_end_time += interval
        # logger.info(current_end_time)
        logger.info(f"等待监控箱关联单灯控制器上报工况中，已等待{int(time.time() - start_time)}秒")
    return False

def check_lampbase_open_switchstatus(test_special_lamppost,start_time,current_end_time,timeout=10,interval=2):
    """
    轮询检查灯杆主道和辅道开灯状态，达成条件返回True
    :param test_special_lamppost:
    :param start_time:
    :param current_end_time:
    :param timeout:
    :param interval:
    :return:
    """
    case_data = common.get_test_data()["check_lampbase_switchstatus_cases"]
    expect_open_switchstatus = case_data["expect"]["data"]["open_switchstatus"]
    # expect_close_switchstatus = case_data["expect"]["data"]["close_switchstatus"]

    param = case_data["request"]["param"]
    param["lampPostId"] = test_special_lamppost

    while time.time() - start_time < timeout:
        try:
            param["beginTime"] = int(start_time) * 1000
            param["endTime"] = int(current_end_time) * 1000
            # param = {"current": 1, "size": 15, "lampPostId": test_special_lamppost, "beginTime": int(start_time)*1000, "endTime": int(current_end_time)*1000}
            logger.info(f"{int(start_time)*1000}-{int(current_end_time)*1000}")
            response = common.req_api(case_data, param=param)
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
                # if pos1_switchstatus == expect_open_switchstatus:
                    return True
                # elif pos1_switchstatus == expect_close_switchstatus and pos2_switchstatus == expect_close_switchstatus:
                # if pos1_switchstatus == expect_close_switchstatus:
                #     return True
        except Exception as e:
            logger.info(f"运行数据暂未上报,{e}")
        time.sleep(interval)
        current_end_time += interval
        logger.info(current_end_time)
        logger.info(f"等待运行数据上报中，已等待{int(time.time() - start_time)}秒")
    return False

def check_lampbase_close_switchstatus(test_special_lamppost, start_time, current_end_time, timeout=10, interval=2):
    """
    轮询检查灯杆主道和辅道关灯状态，达成条件返回True
    :param test_special_lamppost:
    :param start_time:
    :param current_end_time:
    :param timeout:
    :param interval:
    :return:
    """
    case_data = common.get_test_data()["check_lampbase_switchstatus_cases"]
    expect_close_switchstatus = case_data["expect"]["data"]["close_switchstatus"]

    param = case_data["request"]["param"]
    param["lampPostId"] = test_special_lamppost

    while time.time() - start_time < timeout:
        try:
            param["beginTime"] = int(start_time) * 1000
            param["endTime"] = int(current_end_time) * 1000
            logger.info(f"{int(start_time) * 1000}-{int(current_end_time) * 1000}")
            response = common.req_api(case_data, param=param)
            res = response.json()
            if res["data"]["records"]:
                pos1_switchstatus = None
                pos2_switchstatus = None
                for r in res["data"]["records"]:
                    if r["position"] == 1:
                        pos1_switchstatus = r["switchStatus"]
                    elif r["position"] == 2:
                        pos2_switchstatus = r["switchStatus"]
                if pos1_switchstatus == expect_close_switchstatus and pos2_switchstatus == expect_close_switchstatus:
                # if pos1_switchstatus == expect_close_switchstatus:
                    return True
                # elif pos1_switchstatus == expect_close_switchstatus and pos2_switchstatus == expect_close_switchstatus:
                # if pos1_switchstatus == expect_close_switchstatus:
                #     return True
        except Exception as e:
            logger.info(f"运行数据暂未上报,{e}")

        time.sleep(interval)
        current_end_time += interval
        logger.info(current_end_time)
        logger.info(f"等待运行数据上报中，已等待{int(time.time() - start_time)}秒")
    return False

def check_lampbase_dimming(test_special_lamppost,start_time,current_end_time,timeout=10,interval=2):
    """
    主道辅道调光至30%，轮询检查灯杆主道和辅道调光状态，达成条件返回True
    :param test_special_lamppost:
    :param start_time:
    :param current_end_time:
    :param timeout:
    :param interval:
    :return:
    """
    case_data = common.get_test_data()["check_lampbase_dimmingLevel_cases"]
    expect_main_dimminglevel = case_data["expect"]["data"]["main_dimmingLevel"]
    expect_side_dimminglevel = case_data["expect"]["data"]["side_dimmingLevel"]

    # base_url, authorization, sign, gxsaas_auth, atimestamp = get_config()
    # full_url = base_url + get_test_data()["check_lampbase_dimmingLevel_cases"]["request"]["url"]
    # headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    # body = get_test_data()["check_lampbase_dimmingLevel_cases"]["request"]["data"]
    # method = get_test_data()["check_lampbase_dimmingLevel_cases"]["request"]["method"]
    param = case_data["request"]["param"]
    param["lampPostId"] = test_special_lamppost
    while time.time() - start_time < timeout:
        try:
            # param = {"current": 1, "size": 15, "lampPostId": test_special_lamppost, "beginTime": int(start_time)*1000, "endTime": int(current_end_time)*1000}
            param["beginTime"] = int(start_time) * 1000
            param["endTime"] = int(current_end_time) * 1000
            logger.info(f"{int(start_time)*1000}-{int(current_end_time)*1000}")
            response = common.req_api(case_data, param=param)
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
                # if pos1_dimminglevel == expect_main_dimminglevel:
                    return True
        except Exception as e:
            logger.info(f"运行数据暂未上报,{e}")

        time.sleep(interval)
        current_end_time += interval
        logger.info(current_end_time)
        logger.info(f"等待运行数据上报中，已等待{int(time.time() - start_time)}秒")
    logger.info("调光上报数据异常")
    return False
