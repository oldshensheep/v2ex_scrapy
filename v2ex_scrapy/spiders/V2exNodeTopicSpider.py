import httpx
import scrapy
import scrapy.http.response.html
from parsel import Selector
from scrapy.utils.project import get_project_settings

from v2ex_scrapy.DB import DB
from v2ex_scrapy.items import TopicItem
from v2ex_scrapy.spiders.CommonSpider import CommonSpider
from v2ex_scrapy import utils


class V2exNodeTopicSpider(scrapy.Spider):
    name = "v2ex-node"

    UPDATE_TOPIC_WHEN_REPLY_CHANGE = True
    UPDATE_COMMENT = True  # only work when UPDATE_TOPIC_WHEN_REPLY_CHANGE = True
    URL = "https://www.v2ex.com/go/"

    """
    现存在的几个问题，因为节点的排序是动态的，如果爬完一页后未爬的主题跑到爬完的页数里那就爬不到了。
    解决方法1，开始爬取时先获取全部帖子ID再开始爬，获取ID的速度比较快所以排序改变的幅度不会很大。
    """

    def __init__(self, node="flamewar", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = DB()
        self.node = node
        self.common_spider = CommonSpider(
            self.logger, update_comment=self.UPDATE_COMMENT
        )
        settings = get_project_settings()
        resp = httpx.get(
            f"{self.URL}{self.node}",
            timeout=10,
            follow_redirects=True,
            cookies=utils.cookie_str2cookie_dict(settings.get("COOKIES", "")),  # type: ignore
            headers={"User-Agent": settings.get("USER_AGENT", "")},  # type: ignore
        ).text
        max_page = (
            Selector(text=resp)
            .xpath('//tr/td[@align="left" and @width="92%"]/a[last()]/text()')
            .get("1")
        )
        self.max_page = int(max_page)

    def start_requests(self):
        for i in range(self.max_page, 0, -1):
            yield scrapy.Request(
                url=f"{self.URL}{self.node}?p={i}",
                callback=self.parse,
                cb_kwargs={"page": i},
            )

    def parse(self, response: scrapy.http.response.html.HtmlResponse, page: int):
        topics = [
            (int(x), int(y))
            for x, y in zip(
                response.xpath('//span[@class="item_title"]/a/@id').re(r"\d+"),
                # not correct when some comments are deleted, fuck
                response.xpath('//span[@class="item_title"]/a/@href').re(r"reply(\d+)"),
            )
        ]
        for i, reply_count in topics:
            if not self.db.exist(TopicItem, i) or (
                self.UPDATE_TOPIC_WHEN_REPLY_CHANGE
                and self.db.get_topic_comment_count(i) < reply_count
            ):
                yield scrapy.Request(
                    url=f"https://www.v2ex.com/t/{i}",
                    callback=self.common_spider.parse_topic,
                    errback=self.common_spider.parse_topic_err,
                    cb_kwargs={"topic_id": i},
                )
