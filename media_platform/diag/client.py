import asyncio
import copy
import urllib.parse
from typing import Any, Callable, Dict, List, Optional

import execjs
import httpx
from playwright.async_api import BrowserContext, Page

from tools import utils
from var import request_keyword_var


class DIAGClient:
    def __init__(
            self,
            timeout=30,
            proxies=None,
            *,
            headers: Dict,
            playwright_page: Optional[Page],
            cookie_dict: Dict
    ):
        self.proxies = proxies
        self.timeout = timeout
        self.headers = headers
        self._host = "https://diag.net"
        self.playwright_page = playwright_page
        self.cookie_dict = cookie_dict

    async def __process_req_params(self, params: Optional[Dict] = None, headers: Optional[Dict] = None):
        if not params:
            return
        headers = headers or self.headers
        local_storage: Dict = await self.playwright_page.evaluate("() => window.localStorage")  # type: ignore
        douyin_js_obj = execjs.compile(open('libs/douyin.js').read())
        common_params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "cookie_enabled": "true",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Firefox",
            "browser_version": "110.0",
            "browser_online": "true",
            "engine_name": "Gecko",
            "os_name": "Windows",
            "os_version": "10",
            "engine_version": "109.0",
            "platform": "PC",
            "screen_width": "1920",
            "screen_height": "1200",
            # " webid": douyin_js_obj.call("get_web_id"),
            # "msToken": local_storage.get("xmst"),
            # "msToken": "abL8SeUTPa9-EToD8qfC7toScSADxpg6yLh2dbNcpWHzE0bT04txM_4UwquIcRvkRb9IU8sifwgM1Kwf1Lsld81o9Irt2_yNyUbbQPSUO8EfVlZJ_78FckDFnwVBVUVK",
        }
        params.update(common_params)
        query = '&'.join([f'{k}={v}' for k, v in params.items()])
        x_bogus = douyin_js_obj.call('sign', query, headers["User-Agent"])
        params["X-Bogus"] = x_bogus
        # print(x_bogus, query)

    async def request(self, method, url, **kwargs):
        async with httpx.AsyncClient(proxies=self.proxies) as client:
            response = await client.request(
                method, url, timeout=self.timeout,
                **kwargs
            )
            print(response)
            try:
                return response.json()
            except Exception as e:
                print(e)
                raise Exception(f"Request failed: {response.text}")

    async def get(self, uri: str, params: Optional[Dict] = None, headers: Optional[Dict] = None):
        await self.__process_req_params(params, headers)
        headers = headers or self.headers
        return await self.request(method="GET", url=f"{self._host}{uri}", params=params, headers=headers)

    async def post(self, uri: str, data: dict, headers: Optional[Dict] = None):
        await self.__process_req_params(data, headers)
        headers = headers or self.headers
        return await self.request(method="POST", url=f"{self._host}{uri}", json=data, headers=headers)

    @staticmethod
    async def pong(browser_context: BrowserContext) -> bool:
        _, cookie_dict = utils.convert_cookies(await browser_context.cookies())
        # todo send some api to test login status
        return cookie_dict.get("dnid", "") != ""

    async def update_cookies(self, browser_context: BrowserContext):
        cookie_str, cookie_dict = utils.convert_cookies(await browser_context.cookies())
        self.headers["Cookie"] = cookie_str
        self.cookie_dict = cookie_dict

    async def search_info_by_list(
        self,
        keyword: str = "",
        offset: int = 0,
    ):
        data = {
            "PageStartIndex": 10,
            "PageItemCount": 10,
            "Keywords": None,
            "Topics": [],
            "Types": [],
            "TopicSubscriptionsOnly": False,
            "TypeSubscriptionsOnly": False,
            "DiscussionsIStarted": False,
            "NoReplies": False,
            "Makes": [],
            "UnreadDiscussionsOnly": False,
            "StreamOptions": {}
        }
        headers = copy.copy(self.headers)
        return await self.post("/api/v1/messages", data=data, headers=headers)

    async def get_aweme_all_comments(
            self,
            aweme_id: str,
            browser_context: BrowserContext,
            crawl_interval: float = 1.0,
            is_fetch_sub_comments=False,
            callback: Optional[Callable] = None,
    ):
        """
        获取帖子的所有评论，包括子评论
        :param aweme_id: 帖子ID
        :param crawl_interval: 抓取间隔
        :param is_fetch_sub_comments: 是否抓取子评论
        :param callback: 回调函数，用于处理抓取到的评论
        :return: 评论列表
        """
        result = []
        # comments_has_more = 1
        # comments_cursor = 0
        new_context = await browser_context.new_page()
        await new_context.goto(aweme_id)
        element = await new_context.query_selector("div[class='dn-message dn-root-message']")
        await asyncio.sleep(crawl_interval)
        # while comments_has_more:
        #     comments_res = await self.get_aweme_comments(aweme_id, comments_cursor)
        #     comments_has_more = comments_res.get("has_more", 0)
        #     comments_cursor = comments_res.get("cursor", 0)
        #     comments = comments_res.get("comments", [])
        #     if not comments:
        #         continue
        #     result.extend(comments)
        #     # if callback:  # 如果有回调函数，就执行回调函数
        #     #     await callback(aweme_id, comments)

        #     await asyncio.sleep(crawl_interval)
        #     if not is_fetch_sub_comments:
        #         continue
            # todo fetch sub comments
        return result
    
    async def get_aweme_comments(self, aweme_id: str, cursor: int = 0):
        """get note comments

        """
        uri = "/aweme/v1/web/comment/list/"
        params = {
            "aweme_id": aweme_id,
            "cursor": cursor,
            "count": 20,
            "item_type": 0
        }
        keywords = request_keyword_var.get()
        referer_url = "https://www.douyin.com/search/" + keywords + '?aid=3a3cec5a-9e27-4040-b6aa-ef548c2c1138&publish_time=0&sort_type=0&source=search_history&type=general'
        headers = copy.copy(self.headers)
        headers["Referer"] = urllib.parse.quote(referer_url, safe=':/')
        return await self.get(uri, params)