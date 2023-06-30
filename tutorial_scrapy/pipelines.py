# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from typing import Union

from tutorial_scrapy.DB import DB
from tutorial_scrapy.items import (
    CommentItem,
    MemberItem,
    TopicItem,
    TopicSupplementItem,
)


class TutorialScrapyPipeline:
    def __init__(self):
        # Connect to SQLite database
        self.db = DB()

        self.a = {
            TopicItem: self.handle_topic,
            CommentItem: self.handle_comment,
            MemberItem: self.handle_member,
            TopicSupplementItem: self.handle_topic_supplement,
        }

    def process_item(self, item: Union[TopicItem, CommentItem, MemberItem], spider):
        self.a[type(item)](item)
        return item

    def handle_topic(self, topic: TopicItem) -> None:
        # Process topic item
        # Save to SQLite database
        self.db.save_topic(topic)

    def handle_topic_supplement(self, i: TopicSupplementItem) -> None:
        # Process member item
        # Save to SQLite database
        self.db.save_topic_supplement(i)

    def handle_comment(self, comment: CommentItem) -> None:
        # Process comment item
        # Save to SQLite database
        self.db.save_comment(comment)

    def handle_member(self, member: MemberItem) -> None:
        # Process member item
        # Save to SQLite database
        self.db.save_member(member)
