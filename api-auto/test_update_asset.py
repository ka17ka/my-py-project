import requests
import common
import allure
import logging
import pytest

logger = logging.getLogger(__name__)

class TestUpdateAsset:
    """测试类：用于管理添加设施相关的测试"""
    def setup_class(self):
        """每个测试类开始时只执行一次（类似初始化）"""
        logger.info("=== 开始更新设施测试 ===")

    def teardown_class(self):
        """每个测试类结束时执行一次（类似清理）"""
        logger.info("=== 更新设施测试结束 ===")

    @allure.feature("资产系统-配电设施")
    @allure.story("更新配电设施")
    @pytest.mark.parametrize("case_data", common.get_test_data()["update_distribution_cases"],
                             ids=lambda data: data.get("name"))
    def test_update_distribution(self,test_check_distribution,case_data):
        distribution_id, distribution_name = test_check_distribution
        if distribution_id is None:
            pytest.skip("未找到新增配电设施,跳过此测试")
        logger.info(f"开始执行测试用例{case_data['name']}")

        body = case_data["request"]["data"]
        body["id"] = distribution_id
        body["name"] = distribution_name

        try:
            response = common.req_api(case_data,body=body)
            # response = common.reqapi("add_distribution_cases")
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        # 断言
        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-回路监控箱")
    @allure.story("更新回路监控箱")
    @pytest.mark.parametrize("case_data", common.get_test_data()["update_hardware_cases"],
                             ids=lambda data: data.get("name"))
    def test_update_hardware(self,test_check_distribution,test_check_hardware,case_data):
        hardware_id, hardware_name = test_check_hardware
        if hardware_id is None:
            pytest.skip("未找到新增监控箱,跳过此测试")

        body = case_data["request"]["data"]

        body["id"] = hardware_id
        body["name"] = hardware_name
        distribution_id, distribution_name = test_check_distribution
        body["distributionId"] = distribution_id
        body["distributionName"] = distribution_name

        try:
            response = common.req_api(case_data,body=body)
            # response = common.reqapi("add_distribution_cases")
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        # 断言
        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-灯杆")
    @allure.story("更新灯杆")
    @pytest.mark.parametrize("case_data", common.get_test_data()["update_lamppost_cases"],
                             ids=lambda data: data.get("name"))
    def test_update_lamppost(self,test_check_distribution,test_check_hardware,test_check_lamppost,case_data):
        _, hardware_name = test_check_hardware
        lamppost_id,lamppost_name = test_check_lamppost
        distribution_id, _ = test_check_distribution
        if lamppost_id is None:
            pytest.skip("未找到新增灯杆,跳过此测试")

        body = case_data["request"]["data"]
        body["distributionId"] = distribution_id
        body["jkxName"] = hardware_name
        body["id"] = lamppost_id
        body["name"] = lamppost_name

        try:
            response = common.req_api(case_data,body=body)
            # response = common.reqapi("add_distribution_cases")
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        # 断言
        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-单灯控制器")
    @allure.story("更新单灯控制器")
    @pytest.mark.parametrize("case_data", common.get_test_data()["update_lampcontrol_cases"],
                             ids=lambda data: data.get("name"))
    def test_update_lampcontrol(self,test_check_distribution,test_check_lamppost,test_check_lampcontrol,case_data):
        lampcontrol_id, lampcontrol_name, lampcontrol_code = test_check_lampcontrol
        if lampcontrol_id is None:
            pytest.skip("未找到新增单灯,跳过此测试")

        lamppost_id,lamppost_name = test_check_lamppost
        body = case_data["request"]["data"]
        distribution_id, distribution_name = test_check_distribution
        body["distributionId"] = distribution_id
        body["distributionName"] = distribution_name
        body["lampPostId"] = lamppost_id
        body["lampPostName"] = lamppost_name
        body["id"] = lampcontrol_id
        body["name"] = lampcontrol_name
        body["code"] = lampcontrol_code

        try:
            response = common.req_api(case_data, body=body)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-灯具")
    @allure.story("更新无单灯灯具")
    @pytest.mark.parametrize("case_data", common.get_test_data()["update_lampbase_without_control_cases"],
                             ids=lambda data: data.get("name"))
    def test_update_lampbase_without_control(self,test_check_distribution, test_check_lamppost,
                                             test_check_lampbase_without_control,case_data):
        lamppost_id, lamppost_name = test_check_lamppost
        if lamppost_id is None:
            pytest.skip("未找到新增灯杆,跳过此测试")

        lampbase_without_control_id,lampbase_without_control_name = test_check_lampbase_without_control
        distribution_id, distribution_name = test_check_distribution
        body = case_data["request"]["data"]
        body["distributionId"] = distribution_id
        body["distributionName"] = distribution_name
        body["lampPostId"] = lamppost_id
        body["lampPostName"] = lamppost_name
        body["id"] = lampbase_without_control_id
        body["name"] = lampbase_without_control_name

        try:
            response = common.req_api(case_data, body=body)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-灯具")
    @allure.story("更新有单灯灯具")
    @pytest.mark.parametrize("case_data", common.get_test_data()["update_lampbase_with_control_cases"],
                             ids=lambda data: data.get("name"))
    def test_update_lampbase_with_control(self,test_check_distribution, test_check_lamppost,
                                          test_check_lampcontrol,test_check_lampbase_with_control,case_data):
        lamppost_id, lamppost_name = test_check_lamppost
        if lamppost_id is None:
            pytest.skip("未找到新增灯杆,跳过此测试")

        _, _, lampcontrol_code = test_check_lampcontrol
        lampbase_with_control_id,lampbase_with_control_name = test_check_lampbase_with_control
        distribution_id, distribution_name = test_check_distribution

        body = case_data["request"]["data"]
        body["distributionId"] = distribution_id
        body["distributionName"] = distribution_name
        body["lampPostId"] = lamppost_id
        body["lampPostName"] = lamppost_name
        body["id"] = lampbase_with_control_id
        body["name"] = lampbase_with_control_name
        body["lampNodeCode"] = lampcontrol_code

        try:
            response = common.req_api(case_data, body=body)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        common.assert_case_result(case_data, res)

# @allure.feature("资产系统-灯具")
# @allure.story("更新灯具")
# def test_update_lampbase(test_check_distribution, test_check_lamppost, test_check_lampcontrol,test_check_lampbase):
#     base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
#     headers = {"Authorization": authorization, "gxsaas-auth": gxsaas_auth, "sign": sign, "atimestamp": atimestamp}
#
#     lamppost_id, lamppost_name = test_check_lamppost
#     _, _, lampcontrol_code = test_check_lampcontrol
#     lampbase_without_control, lampbase_with_control = test_check_lampbase
#     lampbase_without_control_id,lampbase_without_control_name = lampbase_without_control
#     lampbase_with_control_id, lampbase_with_control_name = lampbase_with_control
#     for case in common.get_test_data()["update_lampbase_cases"]:
#         full_url = base_url + case["request"]["url"]
#         body = case["request"]["data"]
#         body["distributionId"] = test_check_distribution
#         body["lampPostId"] = lamppost_id
#         body["lampPostName"] = lamppost_name
#         if body["lampNodeCode"]:
#             body["lampNodeCode"] = lampcontrol_code
#             body["id"] = lampbase_with_control_id
#             body["name"] = lampbase_with_control_name
#         elif body["lampNodeCode"] is None:
#             body["id"] = lampbase_without_control_id
#             body["name"] = lampbase_without_control_name
#
#         method = case["request"]["method"]
#         response = requests.request(method, full_url, headers=headers, json=body)
#         res = response.json()
#         assert res["code"] == case["expect"]["code"]








