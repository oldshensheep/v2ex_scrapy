import scrapy
import scrapy.http.response.html

from v2ex_scrapy.DB import DB
from v2ex_scrapy.items import TopicItem
from v2ex_scrapy.spiders.CommonSpider import CommonSpider


class V2exSpider(scrapy.Spider):
    name = "v2ex"
    FORCE_UPDATE_TOPIC = False
    UPDATE_COMMENT = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = DB()
        self.start_id = 1
        self.end_id = 1000000
        self.common_spider = CommonSpider(
            self.logger, update_comment=self.UPDATE_COMMENT
        )
        self.logger.info(f"start from topic id {self.start_id}, end at {self.end_id}")

    def start_requests(self):
        for i in range(self.start_id + 1, self.end_id + 1):
            if (
                self.FORCE_UPDATE_TOPIC
                or (not self.db.exist(TopicItem, i))
                or (
                    self.db.get_topic_comment_count(i)
                    > self.db.get_comment_count_by_topic(i)
                )
            ):
                yield scrapy.Request(
                    url=f"https://www.v2ex.com/t/{i}",
                    callback=self.common_spider.parse_topic,
                    errback=self.common_spider.parse_topic_err,
                    cb_kwargs={"topic_id": i},
                )
            else:
                self.logger.info(f"skip topic {i}")
