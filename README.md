# 验证码通知服务

一个基于Flask的轻量级验证码通知服务，支持多种推送方式，可从环境变量灵活配置。

## ✨ 功能特点

- 🚀 **轻量级**：基于Flask框架，资源占用低，部署简单
- 🔐 **安全可靠**：支持Token验证和请求频率限制，防止恶意请求
- 📱 **多种推送**：支持20+种推送方式，包括Bark、钉钉、飞书、Server酱等
- 📋 **智能提取**：自动提取验证码，支持多种格式和4-8位验证码
- ⏰ **时间戳**：自动添加精确到秒的时间戳
- 📊 **易于监控**：提供健康检查端点，方便集成监控系统
- 🔧 **灵活配置**：支持从环境变量或配置文件配置
- 🐳 **容器友好**：提供Dockerfile和docker-compose.yml，支持容器部署
- 📈 **日志完善**：详细的日志记录，方便调试和监控
- 🌍 **时区支持**：支持自定义时区配置

## 📁 项目结构

```
.
├── sendServ.py         # 主服务文件，处理HTTP请求
├── notify.py           # 通知服务模块，支持多种推送方式
├── requirements.txt    # 项目依赖
├── Dockerfile          # Docker构建文件
├── docker-compose.yml  # Docker Compose配置
├── .env.example        # 环境变量示例
└── README.md           # 项目说明文档
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/l499477004/verify-code-notify.git
git clone https://gitee.com/rainone/verify-code-notify.git
cd verify-code-notify
```

### 2. 安装依赖

#### 方式一：直接安装

```bash
pip install -r requirements.txt
```

#### 方式二：使用虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

根据需要配置环境变量，可选择以下方式：

#### 方式一：创建.env文件

复制.env.example为.env，然后根据需要修改：

```bash
cp .env.example .env
# 编辑.env文件，配置所需的环境变量
```

#### 方式二：直接设置环境变量

```bash
# Windows (PowerShell)
$env:ALLOWED_TOKENS="your_token_here"
$env:PORT=9700
$env:DEBUG="False"

# Linux/Mac
export ALLOWED_TOKENS="your_token_here"
export PORT=9700
export DEBUG="False"
```

### 4. 启动服务

#### 方式一：直接运行

```bash
python sendServ.py
```

#### 方式二：使用Gunicorn（生产环境推荐）

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
# -w 4：使用4个工作进程
# -b 0.0.0.0:9700：绑定到所有地址的9700端口
gunicorn -w 4 -b 0.0.0.0:9700 sendServ:app
```

#### 方式三：使用Docker

```bash
# 使用docker-compose启动
docker-compose up -d

# 或使用docker build和docker run
# 构建镜像
docker build -t verify-code-notify .
# 运行容器
docker run -d -p 9700:9700 --name verify-code-notify verify-code-notify
```

### 5. 验证服务

服务启动后，可以通过以下方式验证：

```bash
# 检查服务状态
curl -X GET http://localhost:9700/health

# 发送测试通知
curl -X POST http://localhost:9700/send \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token_here", "title": "测试通知", "content": "您的验证码是：123456"}'
```

## 📡 API 说明

### 发送通知

**URL**: `/send`
**方法**: `POST`
**认证**: Token验证
**频率限制**: 5次/分钟，1次/秒

#### 请求头
```
Content-Type: application/json
```

#### 请求体
```json
{
  "token": "your_token_here",  // 必需，用于验证请求的合法性
  "title": "通知标题",         // 可选，通知标题，默认为"验证码收取"
  "content": "您的验证码是：123456"  // 必需，通知内容，支持自动提取验证码
}
```

#### 响应示例

##### 成功
```json
{
  "code": 200,
  "message": "通知发送成功"
}
```

##### 失败 - 缺少参数
```json
{
  "code": 400,
  "message": "缺少必要参数token或content"
}
```

##### 失败 - 无效Token
```json
{
  "code": 401,
  "message": "无效的token"
}
```

##### 失败 - 请求频率过高
```json
{
  "code": 429,
  "message": "请求过于频繁，请稍后再试"
}
```

##### 失败 - 内部错误
```json
{
  "code": 500,
  "message": "通知发送失败"
}
```

### 健康检查

**URL**: `/health`
**方法**: `GET`
**认证**: 无需认证

#### 响应示例
```json
{
  "status": "healthy",
  "timestamp": "2025-12-29 14:30:45"
}
```

## 🔍 验证码提取规则

系统支持自动提取以下格式的验证码：

- `验证码：123456`
- `code: ABCDEF`
- `校验码 7890`
- `verification code: 1A2B3C`
- 纯数字/字母验证码：`1234` 或 `ABCD`
- 4位数字验证码：`1234`

提取后的验证码会在通知中突出显示，格式为：

```
【时间】：2025-12-29 14:30:45

【验证码】：123456

您的验证码是：123456，有效期5分钟
```

## 📧 支持的推送方式

| 推送方式 | 环境变量配置 | 说明 |
|---------|-------------|------|
| Bark | `BARK_PUSH` | Bark推送，支持iOS设备 |
| 钉钉机器人 | `DD_BOT_SECRET`、`DD_BOT_TOKEN` | 钉钉群机器人推送 |
| 飞书机器人 | `FSKEY` | 飞书群机器人推送 |
| Go-cqhttp | `GOBOT_URL`、`GOBOT_QQ`、`GOBOT_TOKEN` | QQ消息推送 |
| Gotify | `GOTIFY_URL`、`GOTIFY_TOKEN` | 自建推送服务 |
| iGot | `IGOT_PUSH_KEY` | iGot聚合推送 |
| Server酱 | `PUSH_KEY` | Server酱推送，支持微信 |
| PushDeer | `DEER_KEY`、`DEER_URL` | PushDeer推送服务 |
| Synology Chat | `CHAT_URL`、`CHAT_TOKEN` | 群晖Chat推送 |
| Push+ | `PUSH_PLUS_TOKEN`、`PUSH_PLUS_USER` | Push+微信推送 |
| 微加机器人 | `WE_PLUS_BOT_TOKEN`、`WE_PLUS_BOT_RECEIVER` | 微加企业微信推送 |
| Qmsg | `QMSG_KEY`、`QMSG_TYPE` | Qmsg酱QQ推送 |
| 企业微信应用 | `QYWX_AM` | 企业微信应用消息推送 |
| 企业微信机器人 | `QYWX_KEY` | 企业微信机器人推送 |
| Telegram | `TG_BOT_TOKEN`、`TG_USER_ID` | Telegram机器人推送 |
| 智能微秘书 | `AIBOTK_KEY`、`AIBOTK_TYPE`、`AIBOTK_NAME` | 智能微秘书微信推送 |
| SMTP邮件 | `SMTP_SERVER`、`SMTP_SSL`、`SMTP_EMAIL`、`SMTP_PASSWORD`、`SMTP_NAME` | 邮件推送 |
| PushMe | `PUSHME_KEY`、`PUSHME_URL` | PushMe推送服务 |
| Chronocat | `CHRONOCAT_QQ`、`CHRONOCAT_TOKEN`、`CHRONOCAT_URL` | Chronocat QQ推送 |
| 自定义Webhook | `WEBHOOK_URL`、`WEBHOOK_BODY`、`WEBHOOK_HEADERS`、`WEBHOOK_METHOD`、`WEBHOOK_CONTENT_TYPE` | 自定义Webhook推送 |

## 🔧 环境变量配置

### 服务配置

| 环境变量 | 类型 | 默认值 | 说明 |
|---------|------|-------|------|
| `ALLOWED_TOKENS` | 字符串 | `aAr#th;}11t.M^1SU8~6)R)71YTh9jsE` | 允许的Token，多个Token用逗号分隔 |
| `PORT` | 整数 | `9700` | 服务端口 |
| `DEBUG` | 布尔值 | `False` | 调试模式，生产环境建议设置为False |

### 通知配置

| 环境变量 | 类型 | 默认值 | 说明 |
|---------|------|-------|------|
| `HITOKOTO` | 布尔值 | `False` | 是否启用一言（随机句子） |
| `CONSOLE` | 布尔值 | `False` | 是否在控制台输出通知 |

所有支持的推送方式都可以通过环境变量配置，具体请参考上面的表格。

## 🐳 Docker 部署

### 1. 环境准备

- 安装Docker：[Docker官网](https://www.docker.com/get-started)
- 安装Docker Compose：[Docker Compose官网](https://docs.docker.com/compose/install/)

### 2. 配置文件

复制`.env.example`为`.env`，然后根据需要修改：

```bash
cp .env.example .env
```

### 3. 启动服务

```bash
# 启动服务（后台运行）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 重新构建镜像
docker-compose build --no-cache
docker-compose up -d
```

### 4. 容器状态管理

```bash
# 查看容器状态
docker ps

# 进入容器
docker exec -it verify-code-notify sh

# 查看容器日志
docker logs verify-code-notify

# 查看容器资源使用情况
docker stats verify-code-notify
```

## 🛠️ 开发说明

### 开发环境

- Python 3.8+
- Flask 2.0+
- 其他依赖见requirements.txt

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务（调试模式）
export DEBUG="True"
python sendServ.py
```

### 代码结构

- `sendServ.py`：主服务文件，处理HTTP请求和路由
- `notify.py`：通知服务模块，包含所有推送方式的实现
- `requirements.txt`：项目依赖列表
- `Dockerfile`：Docker构建文件
- `docker-compose.yml`：Docker Compose配置
- `.env.example`：环境变量示例

### 测试

```bash
# 测试健康检查
curl -X GET http://localhost:9700/health

# 测试发送通知
curl -X POST http://localhost:9700/send \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token_here", "title": "测试通知", "content": "您的验证码是：123456"}'
```

## 🔒 安全建议

1. **生产环境**：
   - 使用强Token，并定期更换
   - 关闭调试模式（DEBUG=False）
   - 使用HTTPS协议
   - 合理配置请求频率限制

2. **部署建议**：
   - 使用Docker部署，便于管理和升级
   - 配置防火墙，限制访问IP
   - 定期备份配置文件
   - 监控服务状态和日志

3. **配置安全**：
   - 不要将敏感信息（如Token、密码）硬编码到代码中
   - 使用环境变量或加密的配置文件
   - 定期审计配置文件，移除不必要的权限

## 📝 使用示例

### 示例1：发送验证码通知

```bash
curl -X POST http://localhost:9700/send \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token_here", "title": "登录验证码", "content": "您的登录验证码是：654321，有效期5分钟"}'
```

### 示例2：发送纯数字验证码

```bash
curl -X POST http://localhost:9700/send \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token_here", "title": "验证码", "content": "1234"}'
```

### 示例3：发送包含英文验证码的通知

```bash
curl -X POST http://localhost:9700/send \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token_here", "title": "注册验证码", "content": "Your verification code is: ABC123"}'
```

## ❓ 常见问题

### 1. 验证码没有被提取出来

- 检查验证码格式是否符合支持的规则
- 确保验证码是4-8位数字或字母组合
- 查看日志，了解提取过程

### 2. 推送失败

- 检查推送配置是否正确
- 查看日志，了解具体错误信息
- 测试推送服务是否正常

### 3. 服务无法启动

- 检查端口是否被占用
- 检查依赖是否安装正确
- 查看日志，了解具体错误信息

### 4. 请求被拒绝

- 检查Token是否正确
- 检查请求频率是否超过限制
- 查看日志，了解具体错误信息

## 📊 监控与日志

### 健康检查

服务提供了健康检查端点，可用于监控服务状态：

```bash
curl -X GET http://localhost:9700/health
```

### 日志

服务使用Python内置的logging模块记录日志，包括：
- 请求日志
- 错误日志
- 推送结果日志

Docker部署时，日志会自动收集到Docker日志系统中，可通过以下命令查看：

```bash
docker-compose logs -f
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 贡献指南

1. Fork项目
2. 创建特性分支（git checkout -b feature/AmazingFeature）
3. 提交更改（git commit -m 'Add some AmazingFeature'）
4. 推送到分支（git push origin feature/AmazingFeature）
5. 打开Pull Request

### 贡献者

感谢所有为项目做出贡献的人！

## 📞 联系方式

- GitHub: https://github.com/l499477004/verify-code-notify
- Gitee: https://gitee.com/rainone/verify-code-notify
- Issue: https://github.com/l499477004/verify-code-notify/issues

## 📌 更新日志

### v1.0.0 (2025-12-29)

- ✨ 初始版本发布
- 🚀 支持20+种推送方式
- 🔐 实现Token验证和请求频率限制
- 📋 实现智能验证码提取
- ⏰ 实现时间戳添加
- 🐳 提供Docker支持
- 📊 提供健康检查端点

## 📖 相关资源

- [Flask官方文档](https://flask.palletsprojects.com/)
- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose官方文档](https://docs.docker.com/compose/)
- [Python官方文档](https://docs.python.org/)

## 📈 项目状态

![Project Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

---

**如果您觉得这个项目有用，请给它一个 ⭐️！**
