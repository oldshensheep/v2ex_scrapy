import pathlib
import scrapy
import scrapy.http.response.html

from .. import utils


class V2exCommentSpider(scrapy.Spider):
    name = "replies"

    start_urls = ["https://www.v2ex.com/member/$username/replies"]
    page = 1
    max_page = 0
    username = ""

    def start_requests(self):
        self.username = getattr(self, "tag", "oldshensheep")
        for url in self.start_urls:
            yield scrapy.Request(
                url=url.replace("$username", self.username), callback=self.parse
            )

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        pathlib.Path("filename.html").write_bytes(response.body)

        dock_area = response.css(".dock_area")
        time = dock_area.css(".fr > .fade::text").getall()
        topic_author = dock_area.css(".gray > a:nth-child(1)::text").getall()
        topic_go = dock_area.css(".gray > a:nth-child(3)::attr(href)").re(r"\/(\w+)$")
        topic_id = dock_area.css(".gray > a:nth-child(5)::attr(href)").re(r"(\d+)")
        topic_title = dock_area.css(".gray > a:nth-child(5)::text").getall()

        reply = response.css(".reply_content").xpath("string(.)").getall()
        for i in range(len(reply)):
            yield {
                "time": utils.time_to_timestamp(time[i]),
                "topic_author": topic_author[i],
                "topic_id": topic_id[i],
                "topic_go": topic_go[i],
                "topic_title": topic_title[i],
                "reply": reply[i],
            }
        self.max_page = int(
            response.css("#Main > div.box > div.header::text")[-1].re_first(
                r".*共 (\d+) 页$", "-1"
            )
        )
        print(self.max_page)
        self.page += 1
        if self.page <= self.max_page:
            yield response.follow(f"/member/{self.username}/replies?p={self.page}")
