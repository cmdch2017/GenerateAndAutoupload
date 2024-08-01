from pathlib import Path
from typing import List

from conf import BASE_DIR
import sys

SOCIAL_MEDIA_DOUYIN = "douyin"
SOCIAL_MEDIA_TENCENT = "tencent"
SOCIAL_MEDIA_TIKTOK = "tiktok"
SOCIAL_MEDIA_BILIBILI = "bilibili"


def get_supported_social_media() -> List[str]:
    return [SOCIAL_MEDIA_DOUYIN, SOCIAL_MEDIA_TENCENT, SOCIAL_MEDIA_TIKTOK]


def get_cli_action() -> List[str]:
    return ["upload", "login", "watch"]


def get_base_dir():
    # 如果是打包后的应用程序
    if getattr(sys, 'frozen', False):
        # 获取打包后的应用目录
        base_dir = Path(sys._MEIPASS)
        print('dabao1')
    else:
        # 获取开发环境目录
        base_dir = Path(__file__).resolve().parent.parent
        print('kaifa1')
    return base_dir


async def set_init_script(context):
    base_dir = get_base_dir()

    stealth_js_path = Path(base_dir / "utils/stealth.min.js")
    await context.add_init_script(path=stealth_js_path)
    return context
