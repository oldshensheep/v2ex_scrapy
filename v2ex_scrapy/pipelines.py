# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from typing import Any

# don't remove
from v2ex_scrapy.DB import DB
from v2ex_scrapy.items import CommentItem, MemberItem, TopicItem, TopicSupplementItem

ItemsType = TopicItem | CommentItem | MemberItem | TopicSupplementItem


class TutorialScrapyPipeline:
    BATCH = 10

    def __init__(self):
        # Connect to SQLite database
        self.db = DB()
        self.data: dict[Any, list[ItemsType]] = {
            TopicItem: [],
            CommentItem: [],
            MemberItem: [],
            TopicSupplementItem: [],
        }

    def process_item(
        self,
        item: ItemsType | Any,
        spider,
    ):
        if isinstance(item, (TopicItem, CommentItem, MemberItem, TopicSupplementItem)):
            item_type = type(item)
            self.data[item_type].append(item)
            if len(self.data[item_type]) >= self.BATCH:
                self.process_it(self.data[item_type])
                self.data[item_type] = []
        return item

    def process_it(self, items: list[ItemsType]):
        if len(items) > 0 and isinstance(items[0], MemberItem):
            self.process_members(items) # type: ignore
        else:
            self.db.session.add_all(items)
            self.db.session.commit()

    def process_members(self, items: list[MemberItem]):
        for item in items:
            e = (
                self.db.session.query(MemberItem)
                .where(MemberItem.username == item.username)
                .first()
            )
            if e is None:
                self.db.session.add_all([item])
            elif e.uid is None:
                e.uid = item.uid
        self.db.session.commit()

    def save_all(self):
        for _, v in self.data.items():
            self.process_it(v)

    def close_spider(self, spider):
        self.save_all()
        self.db.close()
