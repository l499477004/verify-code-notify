# 使用Python 3.10 Alpine作为基础镜像，体积小，适合容器部署
FROM python:3.10-alpine

# 设置工作目录
WORKDIR /app

# 安装系统依赖，tzdata用于设置时区
RUN apk add --no-cache tzdata

# 设置时区为上海，可根据需要修改
ENV TZ=Asia/Shanghai

# 复制requirements.txt到工作目录
COPY requirements.txt .

# 安装Python依赖，使用--no-cache-dir减少镜像体积
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到工作目录
COPY . .

# 暴露服务端口，默认9700
EXPOSE 9700

# 设置环境变量默认值
ENV DEBUG="False"
ENV PORT=9700
ENV ALLOWED_TOKENS="aAr#th;}11t.M^1SU8~6)R)71YTh9jsE"


# 启动服务
CMD ["python", "sendServ.py"]
