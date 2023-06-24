# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import sqlite3
from typing import Union


@dataclass
class TopicItem:
    id_: int
    author: str
    title: str
    content: str
    create_date: str


@dataclass
class CommentItem:
    id_: int
    topic_id: int
    commenter: str
    content: str
    create_date: str


@dataclass
class MemberItem:
    username: str
    avatar_url: str
    create_at: str
    social_link: str
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

    def exist(self, type_: Union[TopicItem, CommentItem, MemberItem], q) -> bool:
        return self.a[type(type_)](q)

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
