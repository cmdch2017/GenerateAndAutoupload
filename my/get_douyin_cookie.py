import asyncio
import os
from playwright.async_api import async_playwright
from conf import LOCAL_CHROME_PATH
from pathUtils import get_dest_dir
from utils.base_social_media import set_init_script
from utils.log import douyin_logger


async def cookie_auth(account_file, headless=True):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=headless, executable_path=LOCAL_CHROME_PATH)
        context = await browser.new_context(storage_state=account_file)
        context = await set_init_script(context)
        page = await context.new_page()
        await page.goto("https://creator.douyin.com/creator-micro/content/upload")
        # 2024.06.17 抖音创作者中心改版
        if await page.get_by_text('手机号登录').count():
            print("[+] 等待5秒 cookie 失效")
            return False
        else:
            print("[+] cookie 有效")
            return True


async def douyin_cookie_gen(account_file, headless=False):
    async with async_playwright() as playwright:
        options = {
            'headless': headless
        }
        # Make sure to run headed.
        browser = await playwright.chromium.launch(**options, executable_path=LOCAL_CHROME_PATH)
        # Setup context however you like.
        context = await browser.new_context()
        context = await set_init_script(context)
        # Pause the page, and start recording manually.
        page = await context.new_page()
        await page.goto("https://creator.douyin.com/")
        await page.pause()
        # 点击调试器的继续，保存cookie
        await context.storage_state(path=account_file)


async def douyin_setup(account_file, handle=False, headless=True):
    if not os.path.exists(account_file) or not await cookie_auth(account_file, headless):
        if not handle:
            # Todo alert message
            return False
        douyin_logger.info('[+] cookie文件不存在或已失效，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
        await douyin_cookie_gen(account_file, headless=False)
    return True


# Function to be called from other scripts
def setup_douyin_account(handle=True, headless=True):
    account_file = get_dest_dir() / "douyin_uploader" / "account.json"
    return asyncio.run(douyin_setup(account_file, handle=handle, headless=headless))


if __name__ == '__main__':
    cookie_setup = setup_douyin_account()
    if cookie_setup:
        print("Douyin account setup successfully.")
    else:
        print("Failed to setup Douyin account.")
