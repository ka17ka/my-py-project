import shutil

import pytest
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


if __name__ == "__main__":
    # pytest.main(["-v", "-s", "-rA"])
    if os.path.exists("./results"):
        shutil.rmtree("./results")
    pytest.main([
            "-v", "-s", "-rA",
            # "--alluredir=./results",
            "--log-cli-level=INFO",
            "--log-format=%(asctime)s | %(levelname)-8s | %(filename)-20s:%(lineno)-3d | %(message)s",
            "--log-date-format= %Y-%m-%d %H:%M:%S",
            "--show-capture=no"
            # "--capture=no"  # 让日志实时输出，不被缓存
                 ])

    # pytest.main(["test_update_distribution.py::test_update_hardware","-s"])
    """启动服务器，实时查看测试报告，用于调试"""
    # os.system("allure serve ./results")

    """生成纯静态HTML文件，查看测试报告，用于归档"""
    # os.system("allure generate ./results -o ./allure-report --clean")
    # os.system("allure open ./allure-report")

    """简易测试报告，可发邮箱"""
    # report_dir = "./test_simple_results"
    # if not os.path.exists(report_dir):
    #     os.makedirs(report_dir)
    # pytest.main([
    #     "-v",
    #     "--html=./test_simple_results/report.html",  # 指定报告输出到 test_simple_results
    #     "--self-contained-html"  # （可选）生成独立的 HTML（包含 CSS/JS）
    # ])
    # send_report_email()

def send_report_email():
    """将生成的HTML报告作为附件，发送到指定邮箱"""
    # 邮件配置（需替换为自己的邮箱/密码/收件人）
    sender = "ka1994ka@163.com"       # 发件人邮箱（如QQ邮箱）
    password = "BTbN6iS7wcrbW5Bk"            # 授权码（不是密码！需开启SMTP并获取）
    receiver = "lushuo@guoxintianyu.com"         # 收件人邮箱（可多个，用逗号分隔）
    subject = "自动化测试报告"              # 邮件主题
    body = "这是通过pytest-html生成的测试报告，请查收~"  # 邮件正文

    # 构造邮件（混合类型：文本+附件）
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    # 添加邮件正文（文本格式）
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # 添加HTML报告作为附件（读取report.html文件）
    report_path = "./test_simple_results/report.html"
    if os.path.exists(report_path):  # 检查报告是否存在
        with open(report_path, "rb") as f:
            attachment = MIMEText(f.read(), "base64", "utf-8")  # 二进制读取+base64编码
            attachment["Content-Type"] = "application/octet-stream"  # 附件类型
            attachment["Content-Disposition"] = 'attachment; filename="report.html"'  # 附件名
            msg.attach(attachment)
    else:
        print(f"⚠️ 报告文件 {report_path} 不存在，跳过邮件发送！")
        return

    # 发送邮件（使用SMTP服务器，这里以QQ邮箱为例，端口465）
    try:
        server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 163邮箱的SMTP服务器和端口
        server.login(sender, password)                # 登录邮箱
        server.sendmail(sender, receiver, msg.as_string())  # 发送邮件
        server.quit()                                 # 关闭连接
        print("✅ 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")