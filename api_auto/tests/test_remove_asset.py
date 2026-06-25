import requests
from api_auto.utils import common
import allure
import pytest
import copy
import logging
from api_auto.utils.logging import logger

# logger = logging.getLogger(__name__)

class TestRemoveAsset:
    """测试类：用于管理添加设施相关的测试"""
    def setup_class(self):
        """每个测试类开始时只执行一次（类似初始化）"""
        logger.info("=== 开始移除设施测试 ===")

    def teardown_class(self):
        """每个测试类结束时执行一次（类似清理）"""
        logger.info("=== 移除设施测试结束 ===")

    @allure.feature("资产系统-配电设施")
    @allure.story("删除配电设施")
    @pytest.mark.parametrize("case_data", common.get_test_data()["remove_distribution_cases"],
                             ids=lambda data: data.get("name"))
    def test_remove_distribution(self,test_check_distribution,case_data):
        distribution_id, _ = test_check_distribution
        if distribution_id is None:
            pytest.skip("未找到新增配电设施,跳过此测试")
        logger.info(f"开始执行测试用例:{case_data['name']}")

        param  = case_data["request"]["param"]
        param["ids"] = distribution_id

        try:
            response = common.req_api(case_data,param=param)
            # response = common.reqapi("add_distribution_cases")
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        # 断言
        common.assert_case_result(case_data, res)
        # response = requests.request(method, full_url, headers=headers, params=param)
        # response = common.req_api("remove_distribution_cases",param=param)
        # res = response.json()
        # assert res["code"] == common.get_test_data()["remove_distribution_cases"]["expect"]["code"]

    # print(_test_remove_distribution())

    @allure.feature("资产系统-回路监控箱")
    @allure.story("删除回路监控箱")
    @pytest.mark.parametrize("case_data", common.get_test_data()["remove_hardware_cases"],
                             ids=lambda data: data.get("name"))
    def test_remove_hardware(self,test_check_hardware,case_data):
        hardware_id, _ = test_check_hardware
        if hardware_id is None:
            pytest.skip("未找到新增监控箱,跳过此测试")

        param  = case_data["request"]["param"]
        param["ids"] = hardware_id

        try:
            response = common.req_api(case_data, param=param)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise
        res = response.json()
        logger.info(f"响应结果: {res}")

        common.assert_case_result(case_data, res)

    @allure.feature("监控系统-回路监控箱")
    @allure.story("检查删除回路监控箱同步监控系统")
    @pytest.mark.parametrize("case_data", common.get_test_data()["check_monitor_remove_hardware_cases"],
                             ids=lambda data: data.get("name"))
    def test_check_monitor_remove_hardware(self,test_check_hardware,case_data):
        hardware_id, hardware_name = test_check_hardware
        if hardware_id is None:
            pytest.skip("未找到新增监控箱,跳过此测试")

        logger.info(f"开始执行{case_data['name']}")
        param = case_data["request"]["param"]
        param["keyWord"] = hardware_name

        try:
            response = common.req_api(case_data, param=param)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise
        res = response.json()
        logger.info(f"响应结果: {res}")

        assert len(res["data"]["records"]) == 0

    @allure.feature("资产系统-灯杆")
    @allure.story("删除灯杆")
    @pytest.mark.parametrize("case_data", common.get_test_data()["remove_lamppost_cases"],
                             ids=lambda data: data.get("name"))
    def test_remove_lamppost(self,test_check_lamppost,case_data):
        lamppost_id, _ = test_check_lamppost
        if lamppost_id is None:
            pytest.skip("未找到新增监控箱,跳过此测试")

        param  = case_data["request"]["param"]
        param["ids"] = lamppost_id

        try:
            response = common.req_api(case_data, param=param)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise
        res = response.json()
        logger.info(f"响应结果: {res}")

        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-单灯控制器")
    @allure.story("删除单灯控制器")
    @pytest.mark.parametrize("case_data", common.get_test_data()["remove_lampcontrol_cases"],
                             ids=lambda data: data.get("name"))
    def test_remove_lampcontrol(self,test_check_lampcontrol,case_data):
        lampcontrol_id, _, _ = test_check_lampcontrol
        if lampcontrol_id is None:
            pytest.skip("未找到新增监控箱,跳过此测试")
        param = case_data["request"]["param"]
        param["ids"] = lampcontrol_id

        try:
            response = common.req_api(case_data, param=param)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise
        res = response.json()
        logger.info(f"响应结果: {res}")

        common.assert_case_result(case_data, res)

    @allure.feature("监控系统-单灯控制器")
    @allure.story("检查删除单灯控制器同步监控系统")
    @pytest.mark.parametrize("case_data", common.get_test_data()["check_monitor_remove_lampcontrol_cases"],
                             ids=lambda data: data.get("name"))
    def test_check_monitor_remove_lampcontrol(self,test_check_lampcontrol,case_data):
        lampcontrol_id, lampcontrol_name, _ = test_check_lampcontrol
        if lampcontrol_id is None:
            pytest.skip("未找到新增单灯,跳过此测试")

        logger.info(f"开始执行{case_data['name']}")
        param = case_data["request"]["param"]
        param["keyWord"] = lampcontrol_name

        try:
            response = common.req_api(case_data, param=param)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise
        res = response.json()
        logger.info(f"响应结果: {res}")

        assert len(res["data"]["records"]) == 0


    @allure.feature("资产系统-灯具")
    @allure.story("删除无单灯灯具")
    @pytest.mark.parametrize("case_data", common.get_test_data()["remove_lampbase_without_control_cases"],
                             ids=lambda data: data.get("name"))
    def test_remove_lampbase_without_control(self,test_check_lampbase_without_control,case_data):
        lampbase_without_control_id,_ = test_check_lampbase_without_control
        if lampbase_without_control_id is None:
            pytest.skip("未找到新增无单灯灯具,跳过此测试")
        param = case_data["request"]["param"]
        param["ids"] = lampbase_without_control_id

        try:
            response = common.req_api(case_data, param=param)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise
        res = response.json()
        logger.info(f"响应结果: {res}")

        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-灯具")
    @allure.story("删除有单灯灯具")
    @pytest.mark.parametrize("case_data", common.get_test_data()["remove_lampbase_with_control_cases"],
                             ids=lambda data: data.get("name"))
    def test_remove_lampbase_with_control(self,test_check_lampbase_with_control,case_data):
        lampbase_with_control_id,_ = test_check_lampbase_with_control
        if lampbase_with_control_id is None:
            pytest.skip("未找到新增无单灯灯具,跳过此测试")
        param = case_data["request"]["param"]
        param["ids"] = lampbase_with_control_id

        try:
            response = common.req_api(case_data, param=param)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise
        res = response.json()
        logger.info(f"响应结果: {res}")

        common.assert_case_result(case_data, res)

# @allure.feature("资产系统-灯具")
# @allure.story("删除灯具")
# def test_remove_lampbase(test_check_lampbase):
#     base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
#     headers = {"Authorization":authorization,"gxsaas-auth":gxsaas_auth,"sign":sign,"atimestamp":atimestamp}
#
#     lampbase_without_control, lampbase_with_control = test_check_lampbase
#     lampbase_without_control_id, _ = lampbase_without_control
#     lampbase_with_control_id, _ = lampbase_with_control
#     for case in common.get_test_data()["remove_lampbase_cases"]:
#         full_url = base_url + case["request"]["url"]
#         method = case["request"]["method"]
#         if case["name"] == "删除无单灯灯具成功":
#             param = {"ids": lampbase_without_control_id}
#         elif case["name"] == "删除有单灯灯具成功":
#             param = {"ids": lampbase_with_control_id}
#         response = requests.request(method, full_url, headers=headers, params=param)
#         res = response.json()
#
#         assert res["code"] == case["expect"]["code"]