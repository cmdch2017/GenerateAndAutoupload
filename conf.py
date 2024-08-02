from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.resolve()
XHS_SERVER = "http://127.0.0.1:11901"
# 指定 Chrome 的默认路径
default_chrome_path = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
# 检查路径是否存在
if default_chrome_path.exists():
    LOCAL_CHROME_PATH = default_chrome_path
else:
    LOCAL_CHROME_PATH = ""
    if getattr(sys, 'frozen', False):
        # 腾讯公众号不能用playwright
        # 获取虚拟路径目录
        LOCAL_CHROME_PATH = Path(sys._MEIPASS) / "playwright" / "chromium-1124" / "chrome-win" / "chrome.exe"


