# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import Dict


@dataclass
class TopicItem:
    id_: int
    author: str
    title: str
    content: str
    create_at: int
    node: str
    clicks: int
    tag: list[str]
    votes: int


@dataclass
class TopicSupplementItem:
    topic_id: int
    content: str
    create_at: int


@dataclass
class CommentItem:
    id_: int
    topic_id: int
    commenter: str
    content: str
    create_at: int
    thank_count: int


@dataclass
class MemberItem:
    username: str
    avatar_url: str
    create_at: int
    social_link: list[Dict[str, str]]
    no: int
