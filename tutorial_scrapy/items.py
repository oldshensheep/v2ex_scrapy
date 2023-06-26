# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import sqlite3
from typing import Dict, Type, Union


@dataclass
class TopicItem:
    id_: int
    author: str
    title: str
    content: str
    create_at: str
    node: str
    clicks: int
    tag: list[str]
    votes: int


@dataclass
class CommentItem:
    id_: int
    topic_id: int
    commenter: str
    content: str
    create_at: str
    thank_count: int


@dataclass
class MemberItem:
    username: str
    avatar_url: str
    create_at: str
    social_link: list[Dict[str, str]]
    no: int


class DB:
    def __init__(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect("v2ex.sqlite")
        self.cursor = self.conn.cursor()
        self.a = {
            TopicItem: self.h_topic,
            CommentItem: self.h_comment,
            MemberItem: self.h_member,
        }

    def close(self):
        self.conn.close()

    def exist(
        self, type_: Union[Type[TopicItem], Type[CommentItem], Type[MemberItem]], q
    ) -> bool:
        return self.a[type_](q)

    def get_max_topic_id(self) -> int:
        result = self.cursor.execute("SELECT max(id) FROM topic").fetchone()[0]
        if result == None:
            return 1
        return int(result)

    def h_topic(self, q) -> bool:
        # Check if topic exists in the database based on unique identifier (id_)
        query = "SELECT id FROM topic WHERE id = ?"
        self.cursor.execute(query, (q,))
        result = self.cursor.fetchone()

        return result is not None

    def h_comment(self, q) -> bool:
        # Check if comment exists in the database based on unique identifier (id_)
        query = "SELECT id FROM comment WHERE id = ?"
        self.cursor.execute(query, (q,))
        result = self.cursor.fetchone()

        return result is not None

    def h_member(self, q) -> bool:
        # Check if member exists in the database based on unique identifier (username)
        query = "SELECT username FROM member WHERE username = ?"
        self.cursor.execute(query, (q,))
        result = self.cursor.fetchone()

        return result is not None
