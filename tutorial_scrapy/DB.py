import sqlite3
from typing import Type, Union

from tutorial_scrapy.items import CommentItem, MemberItem, TopicItem


class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect("v2ex.sqlite")
        self.cursor = self.conn.cursor()
        self.a = {
            TopicItem: self.topic_exist,
            CommentItem: self.comment_exist,
            MemberItem: self.member_exist,
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

    def topic_exist(self, q) -> bool:
        # Check if topic exists in the database based on unique identifier (id_)
        query = "SELECT id FROM topic WHERE id = ?"
        self.cursor.execute(query, (q,))
        result = self.cursor.fetchone()

        return result is not None

    def comment_exist(self, q) -> bool:
        # Check if comment exists in the database based on unique identifier (id_)
        query = "SELECT id FROM comment WHERE id = ?"
        self.cursor.execute(query, (q,))
        result = self.cursor.fetchone()

        return result is not None

    def member_exist(self, q) -> bool:
        # Check if member exists in the database based on unique identifier (username)
        query = "SELECT username FROM member WHERE username = ?"
        self.cursor.execute(query, (q,))
        result = self.cursor.fetchone()

        return result is not None
