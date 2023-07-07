import math

import scrapy
import scrapy.http.response.html

from v2ex_scrapy import v2ex_parser
from v2ex_scrapy.DB import DB
from v2ex_scrapy.items import MemberItem, TopicItem


class V2exTopicSpider(scrapy.Spider):
    name = "v2ex"
    start_id = 1
    end_id = 1000000
    UPDATE_TOPIC = False
    UPDATE_COMMENT = False
    UPDATE_MEMBER = False

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.db = DB()
        self.start_id = self.db.get_max_topic_id()
        self.logger.info(f"start from topic id {self.start_id}, end at {self.end_id}")

    def start_requests(self):
        # 之前的评论和用户信息可能没爬完，所以继续爬停止时的topic
        yield scrapy.Request(
            url=f"https://www.v2ex.com/t/{self.start_id}",
            callback=self.parse,
            cb_kwargs={"topic_id": self.start_id},
        )
        for i in range(self.start_id + 1, self.end_id + 1):
            if self.UPDATE_TOPIC or not self.db.exist(TopicItem, i):
                yield scrapy.Request(
                    url=f"https://www.v2ex.com/t/{i}",
                    callback=self.parse,
                    errback=self.parse_topic_err,
                    cb_kwargs={"topic_id": i},
                )

    def parse_topic_err(self, failure):
        topic_id = failure.request.cb_kwargs["topic_id"]
        self.logger.warn(f"Crawl Topic Err {topic_id}")
        yield TopicItem.err_topic(topic_id)

    def parse(self, response: scrapy.http.response.html.HtmlResponse, topic_id: int):
        self.logger.info(f"Crawl Topic {topic_id}")

        if response.status == 302:
            # need login or account too young
            yield TopicItem.err_topic(topic_id=topic_id)
        else:
            for i in v2ex_parser.parse_topic_supplement(response, topic_id):
                yield i
            for topic in v2ex_parser.parse_topic(response, topic_id):
                yield topic
                for i in self.crawl_member(topic.author, response):
                    yield i
                for i in self.parse_comment(response, topic_id):
                    yield i
                # crawl sub page comment
                topic_reply_count = int(
                    response.css(
                        "#Main > div:nth-child(4) > div:nth-child(1) > span::text"
                    ).re_first(r"\d+", "-1")
                )
                if (
                    self.UPDATE_COMMENT
                    or self.db.get_topic_comment_count(topic_id) < topic_reply_count
                ):
                    total_page = math.ceil(topic_reply_count / 100)
                    for i in range(2, total_page + 1):
                        for j in self.crawl_comment(topic_id, i, response):
                            yield j

    def crawl_comment(self, topic_id, page, response):
        yield response.follow(
            f"/t/{topic_id}?p={page}",
            callback=self.parse_comment,
            cb_kwargs={"topic_id": topic_id},
        )

    def parse_comment(self, response: scrapy.http.response.html.HtmlResponse, topic_id):
        for comment_item in v2ex_parser.parse_comment(response, topic_id):
            yield comment_item
            for i in self.crawl_member(comment_item.commenter, response):
                yield i

    def crawl_member(self, username, response: scrapy.http.response.html.HtmlResponse):
        if username != "" and (
            self.UPDATE_MEMBER or not self.db.exist(MemberItem, username)
        ):
            yield response.follow(
                f"/member/{username}",
                callback=self.parse_member,
                errback=self.member_err,
                cb_kwargs={"username": username},
            )

    def member_err(self, failure):
        username = failure.request.cb_kwargs["username"]
        self.logger.warn(f"Crawl Member Err {username}")
        yield MemberItem(
            username=username,
            avatar_url="",
            create_at=0,
            social_link=[],
            uid=-1,
        )

    def parse_member(
        self, response: scrapy.http.response.html.HtmlResponse, username: str
    ):
        self.logger.info(f"Crawl Member {username}")
        for i in v2ex_parser.parse_member(response=response):
            yield i
