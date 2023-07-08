import scrapy
import scrapy.http.response.html

from v2ex_scrapy.DB import DB
from v2ex_scrapy.items import TopicItem
from v2ex_scrapy.spiders.CommonSpider import CommonSpider


class V2exTopicSpider(scrapy.Spider):
    name = "v2ex"
    start_id = 1
    end_id = 1000000
    UPDATE_TOPIC = False
    # only work when UPDATE_TOPIC = True
    UPDATE_COMMENT = True

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.db = DB()
        self.start_id = self.db.get_max_topic_id()
        self.common_spider = CommonSpider(
            self.logger, update_comment=self.UPDATE_COMMENT
        )
        self.logger.info(f"start from topic id {self.start_id}, end at {self.end_id}")

    def start_requests(self):
        # 之前的评论和用户信息可能没爬完，所以继续爬停止时的topic
        yield scrapy.Request(
            url=f"https://www.v2ex.com/t/{self.start_id}",
            callback=self.common_spider.parse_topic,
            errback=self.common_spider.parse_topic_err,
            cb_kwargs={"topic_id": self.start_id},
        )
        for i in range(self.start_id + 1, self.end_id + 1):
            if self.UPDATE_TOPIC or not self.db.exist(TopicItem, i):
                yield scrapy.Request(
                    url=f"https://www.v2ex.com/t/{i}",
                    callback=self.common_spider.parse_topic,
                    errback=self.common_spider.parse_topic_err,
                    cb_kwargs={"topic_id": i},
                )
