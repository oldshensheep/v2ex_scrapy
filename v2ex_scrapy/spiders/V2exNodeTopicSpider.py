import scrapy
import scrapy.http.response.html

from v2ex_scrapy.DB import DB
from v2ex_scrapy.items import TopicItem
from v2ex_scrapy.spiders.CommonSpider import CommonSpider


class V2exTopicSpider(scrapy.Spider):
    name = "v2ex-node"

    UPDATE_TOPIC_WHEN_REPLY_CHANGE = True
    UPDATE_COMMENT = True  # only work when UPDATE_TOPIC_WHEN_REPLY_CHANGE = True

    def __init__(self, node="flamewar", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = DB()
        self.node = node
        self.common_spider = CommonSpider(
            self.logger, update_comment=self.UPDATE_COMMENT
        )

    def start_requests(self):
        for i in range(552, 0, -1):
            yield scrapy.Request(
                url=f"https://www.v2ex.com/go/{self.node}?p={i}",
                callback=self.parse,
                cb_kwargs={"page": i},
            )

    def parse(self, response: scrapy.http.response.html.HtmlResponse, page: int):
        topics = [
            (int(x), int(y))
            for x, y in zip(
                response.xpath('//span[@class="item_title"]/a/@id').re(r"\d+"),
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
