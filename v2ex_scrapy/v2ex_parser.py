import scrapy
import scrapy.http.response.html

import v2ex_scrapy.utils as utils
from v2ex_scrapy.items import (
    CommentItem,
    MemberItem,
    TopicItem,
    TopicSupplementItem,
)


def parse_member(response: scrapy.http.response.html.HtmlResponse):
    """parse page like https://www.v2ex.com/member/oldshensheep"""

    username = response.xpath("//h1/text()").get("")
    avatar_url = response.css(".avatar::attr(src)").get("-1")

    t = response.xpath('//div[@class="cell"]//tr/td/span[@class="gray"]/text()')
    no = t.re_first(r"第 (\d+) 号", "-1")
    create_at = t.re_first(r"加入于 (.*)", "")

    social_list = []
    for i in response.xpath('//div[@class="widgets"]//a'):
        social_list.append({i.xpath(".//img/@alt").get(): i.xpath("./@href").get()})
    yield MemberItem(
        username=username,
        avatar_url=avatar_url,
        create_at=utils.time_to_timestamp(create_at),
        social_link=social_list,
        uid=int(no),
    )


def parse_comment(response: scrapy.http.response.html.HtmlResponse, topic_id):
    reply_box = response.css("#Main > .box > .cell[id] > table")
    for reply_row in reply_box:
        comment_id = reply_row.xpath("..").css(".cell::attr(id)").re_first(r"\d+", "-1")
        # if not self.db.exist(CommentItem, comment_id):
        cbox = reply_row.css("tr")
        author_name = cbox.css(".dark::text").get("-1")
        reply_content = cbox.xpath('.//div[@class="reply_content"]').get("")
        reply_time = cbox.css(".ago::attr(title)").get("")
        thank_count = cbox.css(".fade::text").get("0").strip()
        no = cbox.css(".no::text").get("-1").strip()
        yield CommentItem(
            id_=int(comment_id),
            no=int(no),
            commenter=author_name,
            topic_id=topic_id,
            content=reply_content,
            create_at=utils.time_to_timestamp(reply_time),
            thank_count=int(thank_count),
        )


def parse_topic(response: scrapy.http.response.html.HtmlResponse, topic_id):
    topic_title = response.xpath("string(//div[@class='header']/h1)").get("")
    topic_time = response.css(".header > small > span::attr(title)").get("0")
    topic_author = response.css(".header > small > a::text").get("")
    topic_node = response.css(".header > a:nth-child(4)::attr(href)").re_first(
        r"\/(\w+)$", ""
    )
    topic_click_count = response.css(".header > small::text").re_first(r"\d+", "-1")
    topic_tags = response.css(".tag::attr(href)").re(r"/tag/(.*)")
    topic_vote = response.xpath('(//a[@class="vote"])[1]/text()').re_first(r"\d+", "0")
    # need login, some topics may not have
    topic_favorite_count = -1
    topic_thank_count = -1
    if response.css(".topic_stats::text").get() is not None:
        topic_favorite_count = response.css(".topic_stats::text").re_first(
            r"(\d+) 人收藏", "0"
        )
        topic_thank_count = response.css(".topic_stats::text").re_first(
            r"(\d+) 人感谢", "0"
        )

    topic_content = response.css(".cell .topic_content").get("")
    topic_reply_count = response.css(".box > .cell > .gray::text").re_first(
        r"(\d+) 条回复", "0"
    )
    yield TopicItem(
        id_=topic_id,
        author=topic_author,
        title=topic_title,
        content=topic_content,
        create_at=utils.time_to_timestamp(topic_time),
        node=topic_node,
        tag=topic_tags,
        clicks=int(topic_click_count),
        votes=int(topic_vote),
        thank_count=int(topic_thank_count),
        favorite_count=int(topic_favorite_count),
        reply_count=int(topic_reply_count),
    )


def parse_topic_supplement(response: scrapy.http.response.html.HtmlResponse, topic_id):
    for i in response.css(".subtle"):
        subtle_content = i.xpath('string(div[@class="topic_content"])').get("")
        subtle_create_at = i.xpath("string(//span[@title])").get("")
        yield TopicSupplementItem(
            topic_id=topic_id,
            content=subtle_content,
            create_at=utils.time_to_timestamp(subtle_create_at),
        )
