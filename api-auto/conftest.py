import requests
import common
import pytest
import time

@pytest.fixture(scope="session")
def test_check_distribution():
    # base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    # full_url = base_url + common.get_test_data()["check_distribution_cases"]["request"]["url"]
    # headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    # body = common.get_test_data()["check_distribution_cases"]["request"]["data"]
    # method = common.get_test_data()["check_distribution_cases"]["request"]["method"]
    # param = common.get_test_data()["check_distribution_cases"]["request"]["param"]

    case_data = common.get_test_data()["check_distribution_cases"]
    response = common.req_api(case_data)
    res = response.json()
    distribution_name = None
    distribution_id = None
    for record in res["data"]["records"]:
        if record["name"] == case_data["expect"]["data"]["name"]:
            distribution_name = record["name"]
            distribution_id = record["id"]
            break

    return distribution_id,distribution_name

@pytest.fixture(scope="session")
def test_check_hardware():
    case_data = common.get_test_data()["check_hardware_cases"]
    response = common.req_api(case_data)
    res = response.json()
    hardware_name = None
    hardware_id = None
    for record in res["data"]["records"]:
        if record["name"] == case_data["expect"]["data"]["name"]:
            hardware_name = record["name"]
            hardware_id = record["id"]
            break

    return hardware_id, hardware_name

@pytest.fixture(scope="session")
def test_check_lamppost():
    case_data = common.get_test_data()["check_lamppost_cases"]
    response = common.req_api(case_data)
    res = response.json()
    lamppost_id = None
    lamppost_name = None
    for record in res["data"]["records"]:
        if record["name"] == case_data["expect"]["data"]["name"]:
            lamppost_id = record["id"]
            lamppost_name = record["name"]
            break

    return lamppost_id,lamppost_name

@pytest.fixture(scope="session")
def test_check_lampcontrol():
    case_data = common.get_test_data()["check_lampcontrol_cases"]
    response = common.req_api(case_data)
    res = response.json()
    lampcontrol_id = None
    lampcontrol_name = None
    lampcontrol_code = None
    for record in res["data"]["records"]:
        if record["name"] == case_data["expect"]["data"]["name"]:
            lampcontrol_id = record["id"]
            lampcontrol_name = record["name"]
            lampcontrol_code = record["code"]
            break

    return lampcontrol_id,lampcontrol_name,lampcontrol_code

@pytest.fixture(scope="session")
def test_check_lampbase_without_control():
    case_data = common.get_test_data()["check_lampbase_without_control_cases"]
    response = common.req_api(case_data)
    res = response.json()
    lampbase_without_control_id = None
    lampbase_without_control_name = None
    for record in res["data"]["records"]:
        if record["name"] == case_data["expect"]["data"]["name"]:
            lampbase_without_control_id = record["id"]
            lampbase_without_control_name = record["name"]
            break

    return lampbase_without_control_id,lampbase_without_control_name

@pytest.fixture(scope="session")
def test_check_lampbase_with_control():
    case_data = common.get_test_data()["check_lampbase_with_control_cases"]
    response = common.req_api(case_data)
    res = response.json()
    lampbase_with_control_id = None
    lampbase_with_control_name = None
    for record in res["data"]["records"]:
        if record["name"] == case_data["expect"]["data"]["name"]:
            lampbase_with_control_id = record["id"]
            lampbase_with_control_name = record["name"]
            break

    return lampbase_with_control_id,lampbase_with_control_name

@pytest.fixture(scope="session")
def test_special_hardware():
    base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    full_url = base_url + common.get_test_data()["check_special_hardware_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    method = common.get_test_data()["check_special_hardware_cases"]["request"]["method"]

    params = common.get_test_data()["check_special_hardware_cases"]["request"]['param']
    param = {"name": params['name']}
    response = requests.request(method, full_url, headers=headers, params=param)
    res = response.json()
    if not res.get("data",{}).get("records"):
        param = {"name": params['code']}
        response = requests.request(method, full_url, headers=headers, params=param)
        res = response.json()

    special_hardware_id = None
    expect_id = common.get_test_data()["check_special_hardware_cases"]["expect"]["data"]["id"]
    for r in res["data"]["records"]:
        if r["id"] == expect_id:
            special_hardware_id = r["id"]
            break

    return special_hardware_id

@pytest.fixture(scope="session")
def test_special_lamppost():
    base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    full_url = base_url + common.get_test_data()["check_special_lamppost_cases"]["request"]["url"]
    headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
    method = common.get_test_data()["check_special_lamppost_cases"]["request"]["method"]

    params = common.get_test_data()["check_special_lamppost_cases"]["request"]['param']
    param = {"name": params['name']}
    response = requests.request(method, full_url, headers=headers, params=param)
    res = response.json()

    special_lamppost_id = None
    expect_id = common.get_test_data()["check_special_lamppost_cases"]["expect"]["data"]["id"]
    for r in res["data"]["records"]:
        if r["id"] == expect_id:
            special_lamppost_id = r["id"]
            break

    return special_lamppost_id











# @pytest.fixture(scope="session")
# def test_check_lampbase():
#     base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
#     headers = {"Authorization": authorization, "gxsaas-auth": gxsaas_auth, "sign": sign, "atimestamp": atimestamp}
#     lampbase_with_control = None
#     lampbase_without_control = None
#     for case in common.get_test_data()["check_lampbase_cases"]:
#         full_url = base_url + case["request"]["url"]
#         body = case["request"]["data"]
#         method = case["request"]["method"]
#         response = requests.request(method, full_url, headers=headers, params=body)
#         res = response.json()
#         for r in res["data"]["records"]:
#             if r["name"] == case["expect"]["data"]["name"] and case["name"] == "查看无单灯灯具成功":
#                 lampbase_without_control = (r["id"],r["name"])
#             elif r["name"] == case["expect"]["data"]["name"] and case["name"] == "查看有单灯灯具成功":
#                 lampbase_with_control = (r["id"],r["name"])
#
#     return lampbase_without_control, lampbase_with_control

# print(_test_check_distribution())
"""钩子函数，收集当前文件夹下所有test_开头文件，进行执行排序"""
def pytest_collection_modifyitems(items):
    # 1. 修复中文显示问题
    for item in items:
        # 处理测试用例名称中的中文
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        # hasattr()：Python内置函数，检查对象是否有指定的属性。"如果 item 对象拥有名为 'nodeid' 的属性，则执行后面的代码"。
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')
        # if hasattr(item, 'nodeid'):
        #     item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    order_mapping = {
    'test_add_asset.py': 1,
    'test_update_asset.py': 2,
    'test_remove_asset.py': 3,
    'test_control.py': 4
    }

    order_mapping_in = {
        "test_remove_lampbase_without_control": 1,  # 最先执行
        "test_remove_lampbase_with_control": 1,
        "test_remove_lampcontrol": 2,
        "test_remove_lamppost": 3,
        "test_remove_hardware": 4,
        "test_remove_distribution": 5  # 最后执行
    }

    order_mapping_control = {
        "test_special_hardware_fully_open": 1,
        "test_special_lampcontrol_open": 2,
        "test_special_lampcontrol_dimming": 3,
        "test_special_lampcontrol_close": 4,
        "test_special_hardware_fully_closed": 5
    }

    items.sort(key=lambda item:
    (
        order_mapping.get(item.nodeid.split("::")[0].split("/")[-1], 999),
        order_mapping_in.get(item.name.split("[")[0] if "[" in item.name else item.name, 999),
        order_mapping_control.get(item.name.split("[")[0] if "[" in item.name else item.name, 999)
     )
               )
    # items.sort(key=lambda item:
    # (
    #     order_mapping.get(item.nodeid.split("::")[0].split("/")[-1], 999),
    #     order_mapping_in.get(item.name, 999),
    #     order_mapping_control.get(item.name, 999)
    #  )
    #            )









    # items.sort(key=lambda item:
    # order_mapping.get(item.nodeid.split("::")[0].split("/")[-1], 999
    #  )
    #            )






# def get_item_key(item):
#     filename = item.nodeid.split("::")[0].split("/")[-1]
#     return order_mapping.get(filename, 999)
#
# items.sort(key=get_item_key)