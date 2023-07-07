# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from typing import Any, Union

# don't remove
import v2ex_scrapy.insert_ignore
from v2ex_scrapy.DB import DB
from v2ex_scrapy.items import (
    CommentItem,
    MemberItem,
    TopicItem,
    TopicSupplementItem,
)

ItemsType = Union[TopicItem, CommentItem, MemberItem, TopicSupplementItem]


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
        item: Union[ItemsType, Any],
        spider,
    ):
        if isinstance(item, (TopicItem, CommentItem, MemberItem, TopicSupplementItem)):
            item_type = type(item)
            self.data[item_type].append(item)
            if len(self.data[item_type]) >= self.BATCH:
                self.db.session.add_all(self.data[item_type])
                self.data[item_type] = []
                self.db.session.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
