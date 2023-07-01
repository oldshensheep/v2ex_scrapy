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
    BATCH = 10

    def __init__(self):
        # Connect to SQLite database
        self.db = DB()
        self.a = {
            TopicItem: self.handle_topic,
            CommentItem: self.handle_comment,
            MemberItem: self.handle_member,
            TopicSupplementItem: self.handle_topic_supplement,
        }
        self.topics = []
        self.comments = []
        self.members = []
        self.topic_supplements = []

    def process_item(self, item: Union[TopicItem, CommentItem, MemberItem], spider):
        self.a[type(item)](item)
        return item

    def close_spider(self, spider):
        self.db.save_topics(self.topics)
        self.db.save_topic_supplements(self.topic_supplements)
        self.db.save_members(self.members)
        self.db.save_comments(self.comments)

        self.db.close()

    def handle_topic(self, topic: TopicItem) -> None:
        self.topics.append(topic)

        if len(self.topics) >= self.BATCH:
            self.db.save_topics(self.topics)
            self.topics = []

    def handle_topic_supplement(self, supplement: TopicSupplementItem) -> None:
        self.topic_supplements.append(supplement)

        if len(self.topic_supplements) >= self.BATCH:
            self.db.save_topic_supplements(self.topic_supplements)
            self.topic_supplements = []

    def handle_comment(self, comment: CommentItem) -> None:
        self.comments.append(comment)

        if len(self.comments) >= self.BATCH:
            self.db.save_comments(self.comments)
            self.comments = []

    def handle_member(self, member: MemberItem) -> None:
        self.members.append(member)

        if len(self.members) >= self.BATCH:
            self.db.save_members(self.members)
            self.members = []
