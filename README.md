# PDF 压缩工具

PDF 压缩工具是一个基于 Flask 的 Web 应用程序，用于压缩 PDF 文件。它允许用户上传 PDF 文件，并选择不同的压缩级别来减小文件大小，同时保持良好的可读性。

## 功能特性

- 支持多种压缩级别：从高保真（prepress）到低保真（screen）
- 支持按照比例压缩pdf文件
- 用户友好的界面，易于操作
- 自动下载压缩后的 PDF 文件
- 使用 Ghostscript 进行高效的 PDF 压缩

![img.png](static/img.png)

## 部署步骤

### 1. 克隆仓库

首先，克隆本项目的仓库到你的本地机器：

### 2. 安装依赖
   确保你已经安装了 Docker 和 Docker Compose。然后，使用以下命令构建和启动容器：
   
`docker-compose up --build -d`

### 3. 访问应用

应用将在 http://localhost:8009 上运行。打开浏览器并访问该地址即可使用 PDF 压缩工具。

### 4. 停止容器

当你完成使用后，可以使用以下命令停止并移除容器：

`docker-compose down`

### 5. 文件存储

上传的 PDF 文件将存储在 uploads 目录中，压缩后的文件将存储在 compressed 目录中。

项目结构

dy-pdf-helper/

* ├── app.py                # 主应用文件
* ├── templates/            # HTML 模板文件
* │   └── index.html        # 主页面
* ├── static/               # 静态文件（如 CSS、JS、图片等）
* ├── uploads/              # 上传的 PDF 文件存储目录
* ├── compressed/           # 压缩后的 PDF 文件存储目录
* ├── Dockerfile            # Docker 镜像构建文件
* ├── docker-compose.yaml   # Docker Compose 配置文件
* ├── requirements.txt      # Python 依赖项
* └── README.md             # 项目说明文档

依赖项

该项目的主要依赖项包括：
Flask: Web 框架
Ghostscript: PDF 压缩工具
Werkzeug: 文件上传处理
完整的依赖项列表可以在 requirements.txt 文件中找到。
