# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from typing import Union

import tutorial_scrapy.insert_ignore
from tutorial_scrapy.DB import DB
from tutorial_scrapy.items import (
    CommentItem,
    MemberItem,
    TopicItem,
    TopicSupplementItem,
)


class TutorialScrapyPipeline:
    BATCH = 10

    def __init__(self):
        # Connect to SQLite database
        self.db = DB()
        self.a = {
            TopicItem: "topics",
            CommentItem: "comments",
            MemberItem: "members",
            TopicSupplementItem: "topic_supplements",
        }
        self.topics = []
        self.comments = []
        self.members = []
        self.topic_supplements = []

    def process_item(self, item: Union[TopicItem, CommentItem, MemberItem], spider):
        attr_name = self.a[type(item)]
        attr = getattr(self, attr_name)

        attr.append(item)

        if len(attr) >= self.BATCH:
            self.db.session.add_all(attr)
            setattr(self, attr_name, [])
            self.db.session.commit()
        return item

    def close_spider(self, spider):
        self.db.session.add_all(self.topics)
        self.db.session.add_all(self.topic_supplements)
        self.db.session.add_all(self.members)
        self.db.session.add_all(self.comments)

        self.db.close()
