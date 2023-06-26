import json
import math
import pathlib

import scrapy
import scrapy.http.response.html

from tutorial_scrapy.items import DB, CommentItem, MemberItem, TopicItem

import tutorial_scrapy.utils as utils


class V2exTopicSpider(scrapy.Spider):
    name = "v2ex"
    start_id = 340
    end_id = 50000

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.db = DB()
        self.start_id = self.db.get_max_topic_id()
        # self.start_id = 24568
        self.logger.info(f"start from topic id {self.start_id}, end at {self.end_id}")

    def start_requests(self):
        for i in range(self.start_id, self.end_id + 1):
            yield scrapy.Request(
                url=f"https://www.v2ex.com/t/{i}",
                callback=self.parse,
                cb_kwargs={"topic_id": i},
            )

    def parse(self, response: scrapy.http.response.html.HtmlResponse, topic_id: int):
        pathlib.Path("filename.html").write_bytes(response.body)

        topic_title = response.css(".header > h1::text").get("")
        topic_time = response.css(".header > small > span::attr(title)").get("")
        topic_author = response.css(".header > small > a::text").get("")
        topic_node = response.css(".header > a:nth-child(4)::attr(href)").re_first(
            r"\/(\w+)$", ""
        )
        topic_click_count = response.css(".header > small::text").re_first(r"\d+", "-1")
        topic_tags = response.css(".tag::attr(href)").re(r"/tag/(.*)")
        topic_vote = response.xpath('(//a[@class="vote"])[1]/text()').re_first(
            r"\d+", "0"
        )
        # need login
        # topic_stats = response.css(".topic_stats::text").re(r"\d+")
        # topic_click_count = topic_stats[0]
        # topic_favorite_count = topic_stats[1]
        # topic_thank_count = topic_stats[2]
        topic_reply_count = int(
            response.css(
                "#Main > div:nth-child(4) > div:nth-child(1) > span::text"
            ).re_first(r"\d+", "-1")
        )
        last_reply_time = (
            -1
            if len(
                r := response.css(
                    "#Main > div:nth-child(4) > div:nth-child(1) > span::text"
                ).getall()
            )
            == 0
            else r[1]
        )

        topic_content = response.css(".topic_content").xpath("string(.)").get("")

        for i in self.parse_comment(topic_id, response):
            yield i

        if topic_reply_count > 100:
            yield response.follow(
                f"/t/{topic_id}?p=2",
                callback=self.parse_subpage_comment,
                cb_kwargs={
                    "topic_id": topic_id,
                    "page": 2,
                    "total_page": math.ceil(topic_reply_count / 100),
                },
            )

        yield TopicItem(
            id_=topic_id,
            author=topic_author,
            title=topic_title,
            content=topic_content,
            create_at=topic_time,
            node=topic_node,
            clicks=int(topic_click_count),
            tag=topic_tags,
            votes=int(topic_vote),
        )
        for i in self.crawl_member(topic_author, response):
            yield i

    def parse_subpage_comment(
        self,
        response: scrapy.http.response.html.HtmlResponse,
        topic_id: int,
        page: int,
        total_page: int,
    ):
        for i in self.parse_comment(topic_id, response):
            yield i
        if page < total_page:
            yield response.follow(
                f"/t/{topic_id}?p={ page + 1}",
                callback=self.parse_subpage_comment,
                cb_kwargs={
                    "topic_id": topic_id,
                    "page": page + 1,
                    "total_page": total_page,
                },
            )
        pathlib.Path("filename.html").write_bytes(response.body)

    def parse_comment(self, topic_id, response: scrapy.http.response.html.HtmlResponse):
        reply_box = response.css("#Main > .box > .cell[id] > table")
        for reply_row in reply_box:
            comment_id = (
                reply_row.xpath("..").css(".cell::attr(id)").re_first(r"\d+", "-1")
            )
            cbox = reply_row.css("tr")
            author_name = cbox.css(".dark::text").get("-1")
            # avatar_url = cbox.css(".avatar::attr(src)").get("-1")
            reply_content = cbox.css(".reply_content").xpath("string(.)").get("")
            reply_time = cbox.css(".ago::attr(title)").get("")
            thank_count = cbox.css(".fade::text").get("0").strip()
            yield CommentItem(
                id_=int(comment_id),
                commenter=author_name,
                topic_id=topic_id,
                content=reply_content,
                create_at=reply_time,
                thank_count=int(thank_count),
            )
            for i in self.crawl_member(author_name, response):
                yield i

    def crawl_member(self, username, response):
        if not self.db.exist(MemberItem, username):
            yield response.follow(
                f"/member/{username}",
                callback=self.parse_member,
                cb_kwargs={"username": username},
            )

    def parse_member(self, response: scrapy.http.response.html.HtmlResponse, username):
        avatar_url = response.css(".avatar::attr(src)").get("-1")
        Tagline = response.xpath(
            '//div[@class="cell"]//tr/td/span[@class="bigger"]/text()'
        ).get("-1")
        Company = response.xpath('//div[@class="cell"]//tr/td/span/strong/text()').get(
            "-1"
        )
        Work_Title = response.xpath(
            '//div[@class="cell"]//tr/td/span/strong/following-sibling::text()'
        ).re_first(r" / (.*)")
        bio = response.xpath('//*[@id="Main"]/div[2]/div[3]/text()').get()
        t = response.xpath('//div[@class="cell"]//tr/td/span[@class="gray"]/text()')
        no = t.re_first(r"第 (\d+) 号", "-1")
        create_at = t.re_first(r"加入于 (.*)", "")

        website = utils.none_or_strip(
            response.xpath('//*[@alt="Website"]/following-sibling::text()').get()
        )
        geo = utils.none_or_strip(
            response.xpath('//*[@alt="Geo"]/following-sibling::text()').get()
        )
        social_list = []
        for i in response.xpath('//div[@class="widgets"]//a'):
            social_list.append({i.xpath(".//img/@alt").get(): i.xpath("./@href").get()})
        yield MemberItem(username, avatar_url, create_at, social_list, int(no))
