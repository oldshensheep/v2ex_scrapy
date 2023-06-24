# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from typing import Union

from tutorial_scrapy.items import CommentItem, MemberItem, TopicItem


class TutorialScrapyPipeline:
    def __init__(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect("v2ex.sqlite")
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.create_tables()
        self.a = {
            TopicItem: self.handle_topic,
            CommentItem: self.handle_comment,
            MemberItem: self.handle_member,
        }

    def create_tables(self):
        # Create topics table
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS topic
                              (id INT PRIMARY KEY,
                              author TEXT,
                              title TEXT,
                              content TEXT,
                              create_date TEXT)"""
        )

        # Create comments table
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS comment
                              (id INT PRIMARY KEY,
                              author TEXT,
                              title TEXT,
                              content TEXT,
                              create_date TEXT)"""
        )

    def process_item(self, item: Union[TopicItem, CommentItem, MemberItem], spider):
        self.a[type(item)](item)
        return item

    def handle_topic(self, topic: TopicItem) -> None:
        # Process topic item
        # Save to SQLite database
        self.save_topic_to_database(topic)

    def handle_comment(self, comment: CommentItem) -> None:
        # Process comment item
        # Save to SQLite database
        self.save_comment_to_database(comment)

    def handle_member(self, member: MemberItem) -> None:
        # Process member item
        # Save to SQLite database
        self.save_member_to_database(member)

    def save_topic_to_database(self, topic: TopicItem) -> None:
        # Insert the topic data into the table
        self.cursor.execute(
            """INSERT or IGNORE INTO topic (id, author, title, content, create_date)
                              VALUES (?, ?, ?, ?, ?)""",
            (topic.id_, topic.author, topic.title, topic.content, topic.create_date),
        )
        self.conn.commit()

    def save_comment_to_database(self, comment: CommentItem) -> None:
        # Insert the comment data into the table
        self.cursor.execute(
            """INSERT or IGNORE INTO comment (id, topic_id, commenter, content, create_date)
                              VALUES (?, ?, ?, ?, ?)""",
            (
                comment.id_,
                comment.topic_id,
                comment.commenter,
                comment.content,
                comment.create_date,
            ),
        )
        self.conn.commit()

    def save_member_to_database(self, member: MemberItem) -> None:
        self.cursor.execute(
            """INSERT or IGNORE INTO member (username, avatar_url, create_at, social_link, no)
                              VALUES (?, ?, ?, ?, ?)""",
            (
                member.username,
                member.avatar_url,
                member.create_at,
                member.social_link,
                member.no,
            ),
        )
        self.conn.commit()

    def __del__(self):
        # Close the database connection
        self.conn.close()
