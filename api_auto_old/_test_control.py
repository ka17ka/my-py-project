import requests
import common
import allure
import pytest
import time

@allure.feature("调度系统-回路监控箱")
@allure.story("天宇监控箱全开")
def test_special_hardware_fully_open(test_special_hardware):
    """
    测试天宇1715监控箱全开功能
    参数test_special_hardware:是从 conftest 中获取的 special_hardware_id
    """
    if test_special_hardware is None:
        pytest.skip("conftest中special_hardware_id未正常返回,跳过此测试")

    base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    full_url = base_url + common.get_test_data()["hardware_fully_open_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}

    body = common.get_test_data()["hardware_fully_open_cases"]["request"]["data"]
    body["deviceId"] = test_special_hardware

    method = common.get_test_data()["hardware_fully_open_cases"]["request"]["method"]
    response = requests.request(method, full_url, headers=headers, json=body)
    res = response.json()
    assert res["code"] == common.get_test_data()["hardware_fully_open_cases"]["expect"]["code"]
    assert common.wait_for_hardware_ready(test_special_hardware),"设备未能在指定时间内就绪"
    print("设备启动成功")

@allure.feature("调度系统-回路监控箱")
@allure.story("天宇监控箱全关")
def test_special_hardware_fully_closed(test_special_hardware):
    """
    测试天宇1715监控箱全关功能
    参数test_special_hardware:是从 conftest 中获取的 special_hardware_id
    """
    if test_special_hardware is None:
        pytest.skip("conftest中special_hardware_id未正常返回,跳过此测试")

    base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    full_url = base_url + common.get_test_data()["hardware_fully_closed_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}

    body = common.get_test_data()["hardware_fully_closed_cases"]["request"]["data"]
    body["deviceId"] = test_special_hardware

    method = common.get_test_data()["hardware_fully_closed_cases"]["request"]["method"]
    response = requests.request(method, full_url, headers=headers, json=body)
    res = response.json()
    assert res["code"] == common.get_test_data()["hardware_fully_closed_cases"]["expect"]["code"]
    assert common.wait_for_hardware_close(test_special_hardware),"设备未能在指定时间内关闭"
    print("设备关闭成功")

@allure.feature("调度系统-单灯控制器")
@allure.story("测试专用单灯控制器开灯")
def test_special_lampcontrol_open(test_special_lamppost):
    """
    测试专用单灯控制器开灯功能
    test_special_lamppost:是从 conftest 中获取的 special_lamppost_id
    """
    start_time = time.time()
    if test_special_lamppost is None:
        pytest.skip("conftest中special_lamppost_id未正常返回,跳过此测试")

    base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    full_url = base_url + common.get_test_data()["lampcontrol_open_close_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}

    param = {"lampPostId":test_special_lamppost,"opr":1,"commandPfc":""}

    method = common.get_test_data()["lampcontrol_open_close_cases"]["request"]["method"]
    response = requests.request(method, full_url, headers=headers, params=param)
    res = response.json()
    current_end_time = time.time()
    assert res["code"] == common.get_test_data()["lampcontrol_open_close_cases"]["expect"]["code"]
    assert common.check_lampbase_switchstatus(test_special_lamppost,start_time,current_end_time),"测试灯杆单灯开灯失败"

@allure.feature("调度系统-单灯控制器")
@allure.story("测试专用单灯控制器关灯")
def test_special_lampcontrol_close(test_special_lamppost):
    """
    测试专用单灯控制器关灯功能
    test_special_lamppost:是从 conftest 中获取的 special_lamppost_id
    """
    start_time = time.time()
    if test_special_lamppost is None:
        pytest.skip("conftest中special_lamppost_id未正常返回,跳过此测试")

    base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    full_url = base_url + common.get_test_data()["lampcontrol_open_close_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}

    param = {"lampPostId":test_special_lamppost,"opr":0,"commandPfc":""}

    method = common.get_test_data()["lampcontrol_open_close_cases"]["request"]["method"]
    response = requests.request(method, full_url, headers=headers, params=param)
    res = response.json()
    current_end_time = time.time()
    assert res["code"] == common.get_test_data()["lampcontrol_open_close_cases"]["expect"]["code"]
    assert common.check_lampbase_switchstatus(test_special_lamppost,start_time,current_end_time),"测试灯杆单灯关灯失败"

@allure.feature("调度系统-单灯控制器")
@allure.story("测试专用单灯控制器调光")
def test_special_lampcontrol_dimming(test_special_lamppost):
    """
    测试专用单灯控制器调光功能
    test_special_lamppost:是从 conftest 中获取的 special_lamppost_id
    """
    start_time = time.time()
    if test_special_lamppost is None:
        pytest.skip("conftest中special_lamppost_id未正常返回,跳过此测试")

    base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    full_url = base_url + common.get_test_data()["lampcontrol_dimming_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}

    param = {"lampPostId":test_special_lamppost,"mainDim":50,"sideDim":50,"commandPfc":""}

    method = common.get_test_data()["lampcontrol_dimming_cases"]["request"]["method"]
    response = requests.request(method, full_url, headers=headers, params=param)
    res = response.json()
    current_end_time = time.time()
    assert res["code"] == common.get_test_data()["lampcontrol_dimming_cases"]["expect"]["code"]
    assert common.check_lampbase_switchstatus(test_special_lamppost,start_time,current_end_time),"测试灯杆单灯关灯失败"




