import scrapy
import scrapy.http.response.html
from scrapy.spidermiddlewares.httperror import HttpError

from v2ex_scrapy import v2ex_parser
from v2ex_scrapy.DB import DB
from v2ex_scrapy.items import MemberItem


class V2exTopicSpider(scrapy.Spider):
    name = "v2ex-member"

    def __init__(self, start_id=1, end_id=635000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = DB()
        self.start_id = start_id
        self.end_id = end_id
        self.logger.info(f"start from topic id {self.start_id}, end at {self.end_id}")

    def start_requests(self):
        for i in range(self.start_id, self.end_id + 1):
            if not self.db.exist(MemberItem, i):
                yield scrapy.Request(
                    url=f"https://www.v2ex.com/uid/{i}",
                    callback=self.parse,
                    errback=self.member_err,
                    cb_kwargs={"uid": i},
                )
            else:
                self.logger.info(f"skip member id:{i}, because it exists")

    def parse(self, response: scrapy.http.response.html.HtmlResponse, uid: int):
        for i in v2ex_parser.parse_member(response):
            i.uid = uid
            yield i

    def member_err(self, failure):
        if failure.check(HttpError):
            yield MemberItem(
                username="",
                avatar_url="",
                create_at=0,
                social_link=[],
                uid=failure.request.cb_kwargs["uid"],
            )
