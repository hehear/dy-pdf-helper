# 使用更小的基础镜像
FROM python:3.9-slim-buster

# 设置工作目录
WORKDIR /app

# 安装 ghostscript
RUN apt-get update && apt-get install -y ghostscript && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制其他应用文件
COPY . .

# 暴露端口
EXPOSE 8009

# 启动服务
CMD ["python3", "app.py"]