from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.resolve()
XHS_SERVER = "http://127.0.0.1:11901"
# 指定 Chrome 的默认路径
default_chrome_path = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
# 检查路径是否存在
if default_chrome_path.exists():
    LOCAL_CHROME_PATH = default_chrome_path
