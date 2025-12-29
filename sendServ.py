#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import os
import re
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import notify

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 配置请求频率限制
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute", "1 per second"],
    storage_uri="memory://"
)

# 从环境变量或硬编码配置中获取允许的tokens
# 优先使用环境变量 ALLOWED_TOKENS，格式为逗号分隔的字符串
ALLOWED_TOKENS = {
    token.strip() for token in os.getenv("ALLOWED_TOKENS", "aAr#th;}11t.M^1SU8~6)R)71YTh9jsE").split(",")
}

# 预编译正则表达式，提高性能
# 匹配4-8位数字或字母组合的验证码，支持多种关键词
CODE_PATTERN = re.compile(r'(?i)(?:验证码|code|校验码|verification code)[:：]?\s*([0-9a-zA-Z]{4,8})')
# 处理纯数字或字母验证码的情况
PURE_CODE_PATTERN = re.compile(r'^\s*([0-9a-zA-Z]{4,8})\s*$')
# 处理4位数字验证码的情况
FOUR_DIGIT_PATTERN = re.compile(r'\b([0-9]{4})\b')


def process_content(content):
    """
    处理content，提取验证码，拼接成新的content
    """
    # 获取当前时间，精确到秒
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 使用预编译的正则表达式提取验证码
    match = CODE_PATTERN.search(content)
    if not match:
        match = PURE_CODE_PATTERN.search(content)
    if not match:
        # 检查是否为4位数字验证码
        match = FOUR_DIGIT_PATTERN.search(content)
    
    if match:
        code = match.group(1)
        # 拼接新的content，添加时间戳，突出显示验证码
        new_content = f"【时间】：{current_time}\n\n【验证码】：{code}\n\n{content}"
        return new_content
    else:
        # 没有找到验证码，添加时间戳后返回原内容
        return f"【时间】：{current_time}\n\n{content}"


@app.route('/send', methods=['POST'])
@limiter.limit("5 per minute")  # 对send接口设置更严格的频率限制
@limiter.limit("1 per second")
def send_notification():
    """
    接收POST请求，验证token，调用notify.send方法发送通知
    """
    logger.info(f"Received request from {request.remote_addr}")
    
    # 获取请求数据，添加错误处理
    try:
        data = request.get_json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {str(e)}")
        return jsonify({"code": 400, "message": "无效的JSON格式"}), 400
    
    # 检查请求数据是否包含token和content
    if not data or 'token' not in data or 'content' not in data:
        logger.warning(f"Missing required parameters from {request.remote_addr}")
        return jsonify({"code": 400, "message": "缺少必要参数token或content"}), 400
    
    token = data['token']
    content = data['content']
    title = data.get('title', '验证码收取')  # 标题默认为"验证码收取"
    
    # 验证token
    if token not in ALLOWED_TOKENS:
        logger.warning(f"Invalid token from {request.remote_addr}")
        return jsonify({"code": 401, "message": "无效的token"}), 401
    
    try:
        # 处理content，提取验证码
        processed_content = process_content(content)
        # 调用notify.send方法发送通知
        notify.send(title, processed_content)
        logger.info(f"Notification sent successfully for token {token[:8]}...")
        return jsonify({"code": 200, "message": "通知发送成功"}), 200
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}", exc_info=True)
        return jsonify({"code": 500, "message": "通知发送失败"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    健康检查端点，用于监控服务状态
    """
    return jsonify({"status": "healthy", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}), 200


@app.errorhandler(429)
def ratelimit_handler(e):
    """
    处理请求频率限制错误
    """
    return jsonify({"code": 429, "message": "请求过于频繁，请稍后再试"}), 429


if __name__ == '__main__':
    # 从环境变量获取端口，默认9700
    port = int(os.getenv("PORT", 9700))
    # 从环境变量获取调试模式，默认False
    debug = os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]
    # 绑定到所有地址，方便容器部署
    app.run(debug=debug, port=port, host="0.0.0.0")
