# 使用 Python 官方镜像作为基础镜像（基于 Ubuntu）
FROM python:3.10

# 安装依赖项，包括 tk 和 tcl 以支持 tkinter
RUN apt-get update && apt-get install -y \
    xvfb \
    libgtk-3-0 \
    libnotify-bin \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 \
    libxrandr2 \
    xauth \
    x11-xserver-utils \
    python3-tk \
    tcl \
    tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 包管理工具 pip
RUN pip install --upgrade pip

# 安装 Playwright 及其依赖
RUN pip install playwright \
    && playwright install

# 安装其他 Python 依赖项
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    requests  \
    playwright \
    eventlet \
    schedule \
    cf_clearance \
    biliup \
    xhs \
    qrcode \
    loguru \
    tkcalendarx

# 设置环境变量以便在没有显示的情况下使用 Playwright
ENV DISPLAY=:99

# 将应用程序的代码添加到容器中
WORKDIR /app
COPY . /app

# 启动 xvfb，以支持 GUI 应用
CMD ["xvfb-run", "python", "main.py"]


# 安装依赖项，包括 tk 和 tcl 以支持 tkinter
RUN apt-get update && apt-get install -y \
    xvfb \
    libgtk-3-0 \
    libnotify-bin \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 \
    libxrandr2 \
    xauth \
    x11-xserver-utils \
    python3-tk \
    tcl \
    tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 包管理工具 pip
RUN pip install --upgrade pip

# 安装 Playwright 及其依赖
RUN pip install playwright \
    && playwright install

# 安装其他 Python 依赖项
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    requests  \
    playwright \
    eventlet \
    schedule \
    cf_clearance \
    biliup \
    xhs \
    qrcode \
    loguru \
    tkcalendarx

# 设置环境变量以便在没有显示的情况下使用 Playwright
ENV DISPLAY=:99

# 将应用程序的代码添加到容器中
WORKDIR /app
COPY . /app

# 启动 xvfb，以支持 GUI 应用
CMD ["xvfb-run", "python", "main.py"]
