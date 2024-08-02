import asyncio
import os

from playwright.async_api import async_playwright

from conf import LOCAL_CHROME_PATH
from pathUtils import get_dest_dir
from utils.base_social_media import set_init_script
from utils.log import tencent_logger


async def cookie_auth(account_file):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, executable_path=LOCAL_CHROME_PATH)
        context = await browser.new_context(storage_state=account_file)
        context = await set_init_script(context)
        # 创建一个新的页面
        page = await context.new_page()
        # 访问指定的 URL
        await page.goto("https://channels.weixin.qq.com/platform/post/create")
        try:
            await page.wait_for_selector('div.title-name:has-text("视频号小店")', timeout=5000)  # 等待5秒
            tencent_logger.error("[+] 等待5秒 cookie 失效")
            return False
        except:
            tencent_logger.success("[+] cookie 有效")
            return True


async def get_tencent_cookie(account_file):
    async with async_playwright() as playwright:
        options = {
            'args': [
                '--lang en-GB'
            ],
            'headless': False,  # Set headless option here
        }
        # Make sure to run headed.
        browser = await playwright.chromium.launch(**options, executable_path=LOCAL_CHROME_PATH)
        # Setup context however you like.
        context = await browser.new_context()  # Pass any options
        # Pause the page, and start recording manually.
        context = await set_init_script(context)
        page = await context.new_page()
        await page.goto("https://channels.weixin.qq.com")
        await page.pause()
        # 点击调试器的继续，保存cookie
        await context.storage_state(path=account_file)

async def weixin_setup(handle=True):
    account_file = get_dest_dir() / "tencent_uploader" / "account.json"
    if not os.path.exists(account_file) or not await cookie_auth(account_file):
        if not handle:
            # Todo alert message
            return False
        tencent_logger.info('[+] cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
        await get_tencent_cookie(account_file)
    return True

if __name__ == '__main__':
    cookie_setup = asyncio.run(weixin_setup())
    if cookie_setup:
        print("Douyin account setup successfully.")
    else:
        print("Failed to setup Douyin account.")
