import requests
from sympy import false
from api_auto.utils import common
import allure
import pytest
import time
import logging
from api_auto.utils import util
from api_auto.utils.logging import logger

# logger = logging.getLogger(__name__)

@allure.feature("调度系统-回路监控箱")
@allure.story("天宇监控箱全开")
@pytest.mark.parametrize("case_data", common.get_test_data()["hardware_fully_open_cases"],
                         ids=lambda data: data.get("name"))
def test_special_hardware_fully_open(test_special_hardware, test_special_lamppost,case_data):
    """
    测试天宇1715监控箱全开功能
    参数test_special_hardware:是从 conftest 中获取的 special_hardware_id
    """
    if test_special_hardware is None:
        pytest.skip("conftest中special_hardware_id未正常返回,跳过此测试")

    # base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    # full_url = base_url + common.get_test_data()["hardware_fully_open_cases"]["request"]["url"]
    # headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    # body = common.get_test_data()["hardware_fully_open_cases"]["request"]["data"]
    # body["deviceId"] = test_special_hardware

    body = case_data["request"]["data"]
    body["deviceId"] = test_special_hardware

    try:
        response = common.req_api(case_data, body=body)
        logger.info(f"请求完成，状态码: {response.status_code}")
    except Exception as e:
        logger.error(f"请求发生异常: {e}")
        raise

    res = response.json()
    logger.info(f"响应结果: {res}")
    common.assert_case_result(case_data, res)
    logger.info(f"设备正在启动，等待查验状态…")
    assert util.wait_for_hardware_ready(test_special_hardware), "设备未能在指定时间内就绪"
    logger.info("设备已启动，等待监控箱关联单灯上报数据…")
    assert util.check_lampcontrol_list(test_special_lamppost),"监控箱关联单灯设备未能在指定时间内上报工况"
    logger.info("监控箱关联单灯已上报数据，监控箱启动成功")

@allure.feature("调度系统-回路监控箱")
@allure.story("天宇监控箱全关")
@pytest.mark.parametrize("case_data", common.get_test_data()["hardware_fully_closed_cases"],
                         ids=lambda data: data.get("name"))
def test_special_hardware_fully_closed(test_special_hardware,case_data):
    """
    测试天宇1715监控箱全关功能
    参数test_special_hardware:是从 conftest 中获取的 special_hardware_id
    """
    if test_special_hardware is None:
        pytest.skip("conftest中special_hardware_id未正常返回,跳过此测试")

    body = case_data["request"]["data"]
    body["deviceId"] = test_special_hardware

    try:
        response = common.req_api(case_data, body=body)
        logger.info(f"请求完成，状态码: {response.status_code}")
    except Exception as e:
        logger.error(f"请求发生异常: {e}")
        raise

    res = response.json()
    logger.info(f"响应结果: {res}")
    common.assert_case_result(case_data, res)
    logger.info(f"设备正在关闭，等待查验状态…")
    assert util.wait_for_hardware_close(test_special_hardware),"设备未能在指定时间内关闭"
    logger.info("设备关闭成功")

@allure.feature("调度系统-单灯控制器")
@allure.story("测试专用单灯控制器开灯")
@pytest.mark.parametrize("case_data", common.get_test_data()["lampcontrol_open_cases"],
                         ids=lambda data: data.get("name"))
def test_special_lampcontrol_open(test_special_lamppost,case_data):
    """
    测试专用单灯控制器开灯功能
    test_special_lamppost:是从 conftest 中获取的 special_lamppost_id
    """
    start_time = time.time()
    if test_special_lamppost is None:
        pytest.skip("conftest中special_lamppost_id未正常返回,跳过此测试")

    param = case_data["request"]["param"]
    param["lampPostId"] = test_special_lamppost

    try:
        response = common.req_api(case_data, param=param)
        logger.info(f"请求完成，状态码: {response.status_code}")
    except Exception as e:
        logger.error(f"请求发生异常: {e}")
        raise

    res = response.json()
    current_end_time = time.time()
    logger.info(f"响应结果: {res}")
    common.assert_case_result(case_data, res)
    logger.info(f"已开灯，等待查验状态…")
    # assert res["code"] ==case_data["expect"]["code"]
    assert util.check_lampbase_open_switchstatus(test_special_lamppost,start_time,current_end_time),"测试灯杆单灯开灯失败"
    logger.info("开灯成功")

@allure.feature("调度系统-单灯控制器")
@allure.story("测试专用单灯控制器关灯")
@pytest.mark.parametrize("case_data", common.get_test_data()["lampcontrol_close_cases"],
                         ids=lambda data: data.get("name"))
def test_special_lampcontrol_close(test_special_lamppost,case_data):
    """
    测试专用单灯控制器关灯功能
    test_special_lamppost:是从 conftest 中获取的 special_lamppost_id
    """
    start_time = time.time()
    if test_special_lamppost is None:
        pytest.skip("conftest中special_lamppost_id未正常返回,跳过此测试")
    #
    # base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    # full_url = base_url + common.get_test_data()["lampcontrol_open_close_cases"]["request"]["url"]
    # headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    # param = {"lampPostId":test_special_lamppost,"opr":0,"commandPfc":""}

    param = case_data["request"]["param"]
    param["lampPostId"] = test_special_lamppost

    try:
        response = common.req_api(case_data, param=param)
        logger.info(f"请求完成，状态码: {response.status_code}")
    except Exception as e:
        logger.error(f"请求发生异常: {e}")
        raise
    res = response.json()
    current_end_time = time.time()
    logger.info(f"响应结果: {res}")
    common.assert_case_result(case_data, res)
    logger.info(f"已关灯，等待查验状态…")
    assert util.check_lampbase_close_switchstatus(test_special_lamppost,start_time,current_end_time),"测试灯杆单灯关灯失败"
    logger.info("关灯成功")

@allure.feature("调度系统-单灯控制器")
@allure.story("测试专用单灯控制器调光")
@pytest.mark.parametrize("case_data", common.get_test_data()["lampcontrol_dimming_cases"],
                         ids=lambda data: data.get("name"))
def test_special_lampcontrol_dimming(test_special_lamppost,case_data):
    """
    测试专用单灯控制器调光功能
    test_special_lamppost:是从 conftest 中获取的 special_lamppost_id
    """
    start_time = time.time()
    if test_special_lamppost is None:
        pytest.skip("conftest中special_lamppost_id未正常返回,跳过此测试")

    # base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    # full_url = base_url + common.get_test_data()["lampcontrol_dimming_cases"]["request"]["url"]
    # headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    # param = {"lampPostId":test_special_lamppost,"mainDim":50,"sideDim":50,"commandPfc":""}
    param = case_data["request"]["param"]
    param["lampPostId"] = test_special_lamppost

    try:
        response = common.req_api(case_data, param=param)
        logger.info(f"请求完成，状态码: {response.status_code}")
    except Exception as e:
        logger.error(f"请求发生异常: {e}")
        raise
    res = response.json()
    current_end_time = time.time()
    logger.info(f"响应结果: {res}")
    common.assert_case_result(case_data, res)
    logger.info(f"已调光主道30%，等待查验状态…")
    assert util.check_lampbase_dimming(test_special_lamppost,start_time,current_end_time),"测试灯杆单灯调光上报数据异常"
    logger.info("调光成功")




