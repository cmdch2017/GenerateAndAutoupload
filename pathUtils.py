from pathlib import Path
import sys

# 磁盘真实路径
def get_dest_dir():
    # 如果是打包后的应用程序
    if getattr(sys, 'frozen', False):
        # 获取打包后的应用目录
        dest_dir = Path(sys.executable).parent
    else:
        # 获取开发环境目录
        dest_dir = Path(__file__).resolve().parent
    return dest_dir


# 磁盘虚拟路径
def get_base_dir():
    # 如果是打包后的应用程序
    if getattr(sys, 'frozen', False):
        # 获取打包后的应用目录
        base_dir = Path(sys._MEIPASS)
    else:
        # 获取开发环境目录
        base_dir = Path(__file__).resolve().parent
    return base_dir
