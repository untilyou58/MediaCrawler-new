import asyncio
import functools
import sys
from typing import Optional

import redis
from playwright.async_api import BrowserContext, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from tenacity import (RetryError, retry, retry_if_result, stop_after_attempt,
                      wait_fixed)

import config
from base.base_crawler import AbstractLogin
from tools import utils


class DiagLogin(AbstractLogin):

    def __init__(self,
                 login_type: str,
                 browser_context: BrowserContext, # type: ignore
                 context_page: Page, # type: ignore
                 login_phone: Optional[str] = "",
                 cookie_str: Optional[str] = ""
                 ):
        self.login_type = login_type
        self.browser_context = browser_context
        self.context_page = context_page
        self.login_phone = login_phone
        self.scan_qrcode_time = 60
        self.cookie_str = cookie_str

    async def begin(self):
        """
            Start login diag website
            Sử dụng cookie để đăng nhập.
        """

        # popup login dialog
        # await self.popup_login_dialog()

        # select login type
        if self.login_type == "qrcode":
            await self.login_by_qrcode()
        elif self.login_type == "phone":
            await self.login_by_mobile()
        elif self.login_type == "cookie":
            await self.login_by_cookies()
        else:
            raise ValueError("[DiagLogin.begin] Invalid Login Type Currently only supported qrcode or phone or cookie ...")

        # Nếu trang chuyển hướng đến trang mã xác minh trượt, bạn cần trượt lại thanh trượt
        await asyncio.sleep(6)

        # check login state
        utils.logger.info(f"[DiagLogin.begin] login finished then check login state ...")
        try:
            await self.check_login_state()
        except RetryError:
            utils.logger.info("[DiagLogin.begin] login failed please confirm ...")
            sys.exit()

        # wait for redirect
        wait_redirect_seconds = 5
        utils.logger.info(f"[DiagLogin.begin] Login successful then wait for {wait_redirect_seconds} seconds redirect ...")
        await asyncio.sleep(wait_redirect_seconds)

    @retry(stop=stop_after_attempt(20), wait=wait_fixed(1), retry=retry_if_result(lambda value: value is False))
    async def check_login_state(self):
        """Check if the current login status is successful and return True otherwise return False"""
        current_cookie = await self.browser_context.cookies()
        _, cookie_dict = utils.convert_cookies(current_cookie)
        if cookie_dict.get("bc") == "1":
            return True
        return False

    async def login_by_qrcode(self):
        pass

    async def login_by_mobile(self):
        pass

    async def login_by_cookies(self):
        utils.logger.info("[DiagLogin.login_by_cookies] Begin login diag by cookie ...")
        for key, value in utils.convert_str_cookie_to_dict(self.cookie_str).items(): # type: ignore
            await self.browser_context.add_cookies([{
                'name': key,
                'value': value,
                'domain': ".diag.net",
                'path': "/"
            }])
