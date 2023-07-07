# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# useful for handling different item types with a single interface

import random
import time
from http.cookies import SimpleCookie

import scrapy
import scrapy.http.response.html
from scrapy import signals

from v2ex_scrapy.DB import DB, LogItem


class TutorialScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ProxyAndCookieDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.proxies: list[str] = []
        self.cookies: dict[str, str] = {}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: scrapy.Request, spider):
        if "proxy" not in request.meta and len(self.proxies) > 0:
            request.meta["proxy"] = random.choice(self.proxies)
        if self.cookies != {} and request.cookies == {}:
            request.cookies = self.cookies
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(
        self, request, response: scrapy.http.response.html.HtmlResponse, spider
    ):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider: scrapy.Spider):
        self.proxies = spider.settings.get("PROXIES", [])  # type: ignore

        if type(cookie_str := spider.settings.get("COOKIES", "")) == str:
            simple_cookie = SimpleCookie()
            simple_cookie.load(cookie_str)  # type: ignore
            self.cookies = {k: v.value for k, v in simple_cookie.items()}

        spider.logger.info("Spider opened: %s" % spider.name)


class RandomUserAgentMiddleware:
    def __init__(self):
        self.user_agents: list[str] = []

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: scrapy.Request, spider):
        if len(self.user_agents) > 0:
            request.headers[b"User-Agent"] = random.choice(self.user_agents)
        return None

    def spider_opened(self, spider: scrapy.Spider):
        with open("./user-agents.txt") as f:
            self.user_agents = f.read().splitlines()


class SaveHttpStatusToDBMiddleware:
    def __init__(self):
        self.db = DB()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_response(
        self, request, response: scrapy.http.response.html.HtmlResponse, spider
    ):
        url = response.url
        status_code = response.status
        create_at = int(time.time())
        self.db.session.add(
            LogItem(url=url, status_code=status_code, create_at=create_at)
        )
        return response
