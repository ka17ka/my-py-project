import requests
from api_auto.utils import common
import allure
import pytest
import time
# import logging
from api_auto.utils.logging import logger

# logger = logging.getLogger(__name__)
"""
Exception举例:
网络异常（如超时）-请求发生异常：requests.exceptions.Timeout: ...
URL格式错误-请求发生异常：requests.exceptions.InvalidURL: ...
JSON序列化错误-TypeError: ...
连接拒绝-requests.exceptions.ConnectionError: ...
必须用raise抛出异常，pytest捕获到这个异常，将此测试标记为 FAILED，否则会继续执行后面代码
"""

class TestAddAsset:
    """测试类：用于管理添加设施相关的测试"""
    def setup_class(self):
        """每个测试类开始时只执行一次（类似初始化）"""
        logger.info("=== 开始添加设施测试 ===")

    def teardown_class(self):
        """每个测试类结束时执行一次（类似清理）"""
        logger.info("=== 添加设施测试结束 ===")

    @allure.feature("资产系统-配电设施")
    @allure.story("添加配电设施")
    @pytest.mark.parametrize("case_data", common.get_test_data()["add_distribution_cases"],
                             ids=lambda data: data.get("name"))
    def test_add_distribution(self,case_data):
        logger.info(f"开始执行{case_data['name']}")

        try:
            response = common.req_api(case_data)
            time.sleep(2)
            # response = common.reqapi("add_distribution_cases")
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        # 断言
        common.assert_case_result(case_data, res)

        # # 获取预期值
        # expected_code =case_data["expect"]["code"]
        # # expected_code = common.get_test_data()["add_distribution_cases"][0]["expect"]["code"]
        #
        # logger.info(f"开始测试断言验证，等待…")
        # try:
        #     if res["code"] != expected_code:
        #         logger.warning(f"业务错误: {res.get('msg', '无错误信息')}")
        #     assert res["code"] == expected_code,f"测试断言验证失败,实际code: {res.get('code')}"
        #     logger.info("测试断言验证通过")
        # finally:
        #     logger.info(f"测试用例:{case_data['name']}执行完毕")
        # time.sleep(2)

    @allure.feature("资产系统-回路监控箱")
    @allure.story("添加回路监控箱")
    @pytest.mark.parametrize("case_data", common.get_test_data()["add_hardware_cases"],
                             ids=lambda data: data.get("name"))
    def test_add_hardware(self,test_check_distribution,case_data):
        distribution_id, _ = test_check_distribution
        if distribution_id is None:
            pytest.skip("未找到新增配电设施,跳过此测试")

        logger.info(f"开始执行{case_data['name']}")
        body = case_data["request"]["data"]
        body["distributionId"] = distribution_id

        try:
            response = common.req_api(case_data,body=body)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        common.assert_case_result(case_data, res)

    @allure.feature("监控系统-回路监控箱")
    @allure.story("检查添加回路监控箱同步监控系统")
    @pytest.mark.parametrize("case_data", common.get_test_data()["check_monitor_add_hardware_cases"],
                             ids=lambda data: data.get("name"))
    def test_check_monitor_add_hardware(self,test_check_hardware,case_data):
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

        assert len(res["data"]["records"]) > 0
        for record in res["data"]["records"]:
            if record["name"] == hardware_name:
                assert record["isDeliver"] == case_data["expect"]["data"]["isDeliver"]

    @allure.feature("资产系统-灯杆")
    @allure.story("添加灯杆")
    @pytest.mark.parametrize("case_data", common.get_test_data()["add_lamppost_cases"],
                             ids=lambda data: data.get("name"))
    def test_add_lamppost(self,test_check_distribution,test_check_hardware,case_data):
        hardware_id,hardware_name = test_check_hardware
        distribution_id, _ = test_check_distribution
        if hardware_id is None:
            pytest.skip("未找到新增监控箱,跳过此测试")

        logger.info(f"开始执行{case_data['name']}")
        body = case_data["request"]["data"]
        body["distributionId"] = distribution_id
        body["jkxName"] = hardware_name

        try:
            response = common.req_api(case_data, body=body)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-单灯控制器")
    @allure.story("添加单灯控制器")
    @pytest.mark.parametrize("case_data", common.get_test_data()["add_lampcontrol_cases"],
                             ids=lambda data: data.get("name"))
    def test_add_lampcontrol(self,test_check_lamppost,case_data):
        lamppost_id,lamppost_name = test_check_lamppost
        if lamppost_id is None:
            pytest.skip("未找到新增灯杆,跳过此测试")

        body = case_data["request"]["data"]
        body["lampPostId"] = lamppost_id
        body["lampPostName"] = lamppost_name

        try:
            response = common.req_api(case_data, body=body)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        common.assert_case_result(case_data, res)

    @allure.feature("监控系统-单灯控制器")
    @allure.story("检查添加单灯控制器同步监控系统")
    @pytest.mark.parametrize("case_data", common.get_test_data()["check_monitor_add_lampcontrol_cases"],
                             ids=lambda data: data.get("name"))
    def test_check_monitor_add_lampcontrol(self,test_check_lampcontrol,case_data):
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

        assert len(res["data"]["records"]) > 0
        for record in res["data"]["records"]:
            if record["name"] == lampcontrol_name:
                assert record["isDeliver"] == case_data["expect"]["data"]["isDeliver"]

    @allure.feature("资产系统-灯具")
    @allure.story("添加无单灯灯具")
    @pytest.mark.parametrize("case_data", common.get_test_data()["add_lampbase_without_control_cases"],
                             ids=lambda data: data.get("name"))
    def test_add_lampbase_without_control(self, test_check_distribution, test_check_lamppost,case_data):
        lamppost_id, lamppost_name = test_check_lamppost
        if lamppost_id is None:
            pytest.skip("未找到新增灯杆,跳过此测试")
        distribution_id, _ = test_check_distribution

        body = case_data["request"]["data"]
        body["lampPostId"] = lamppost_id
        body["lampPostName"] = lamppost_name
        body["distributionId"] = distribution_id

        try:
            response = common.req_api(case_data, body=body)
            time.sleep(2)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        common.assert_case_result(case_data, res)

    @allure.feature("资产系统-灯具")
    @allure.story("添加有单灯灯具")
    @pytest.mark.parametrize("case_data", common.get_test_data()["add_lampbase_with_control_cases"],
                             ids=lambda data: data.get("name"))
    def test_add_lampbase_with_control(self, test_check_distribution, test_check_lamppost, test_check_lampcontrol,case_data):
        lamppost_id, lamppost_name = test_check_lamppost
        if lamppost_id is None:
            pytest.skip("未找到新增灯杆,跳过此测试")
        distribution_id, _ = test_check_distribution
        _, _, lampcontrol_code = test_check_lampcontrol

        body = case_data["request"]["data"]
        body["lampPostId"] = lamppost_id
        body["lampPostName"] = lamppost_name
        body["distributionId"] = distribution_id
        if body.get("lampNodeCode"):
            body["lampNodeCode"] = lampcontrol_code

        try:
            response = common.req_api(case_data, body=body)
            time.sleep(2)
            logger.info(f"请求完成，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            raise

        res = response.json()
        logger.info(f"响应结果: {res}")
        common.assert_case_result(case_data, res)

    # @allure.feature("资产系统-灯具")
    # @allure.story("添加灯具")
    # def test_add_lampbase(self, test_check_distribution, test_check_lamppost, test_check_lampcontrol):
    #     # base_url, authorization, sign, gxsaas_auth, atimestamp = common.get_config()
    #     headers = {"Authorization": self.authorization, "gxsaas-auth": self.gxsaas_auth, "sign": self.sign,
    #                "atimestamp": self.atimestamp}
    #
    #     lamppost_id, lamppost_name = test_check_lamppost
    #     _, _, lampcontrol_code = test_check_lampcontrol
    #     for case in common.get_test_data()["add_lampbase_cases"]:
    #         print(f'开始执行,{case["name"]}')
    #         full_url = self.base_url + case["request"]["url"]
    #         body = case["request"]["data"]
    #         body["distributionId"] = test_check_distribution
    #         body["lampPostId"] = lamppost_id
    #         body["lampPostName"] = lamppost_name
    #         # 字典的get方法,如果lampPostId存在则赋值,不存在时返回None,if body["lampNodeCode"]会抛出KeyError
    #         if body.get("lampNodeCode"):
    #             body["lampNodeCode"] = lampcontrol_code
    #
    #         method = case["request"]["method"]
    #         response = requests.request(method, full_url, headers=headers, json=body)
    #         print(f'{case["name"]}执行结束')
    #         res = response.json()
    #         assert res["code"] == case["expect"]["code"]