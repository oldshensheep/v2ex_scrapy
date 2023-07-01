# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import sqlalchemy
from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


@dataclass
class Base(DeclarativeBase):
    type_annotation_map = {
        list[str]: JSON,
        list[dict[str, str]]: JSON,
        int: Integer,
        str: Text,
    }


@dataclass(kw_only=True)
class TopicItem(Base):
    __tablename__ = "topic"

    id_: Mapped[int] = mapped_column(name="id", primary_key=True)
    author: Mapped[str]
    title: Mapped[str]
    content: Mapped[str]
    node: Mapped[str]
    tag: Mapped[list[str]]
    clicks: Mapped[int]
    votes: Mapped[int]
    create_at: Mapped[int]


@dataclass(kw_only=True)
class TopicSupplementItem(Base):
    __tablename__ = "topic_supplement"

    topic_id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    create_at: Mapped[int]


@dataclass(kw_only=True)
class CommentItem(Base):
    __tablename__ = "comment"

    id_: Mapped[int] = mapped_column(name="id", primary_key=True)
    topic_id: Mapped[int]
    commenter: Mapped[str]
    content: Mapped[str]
    thank_count: Mapped[int]
    create_at: Mapped[int]


@dataclass(kw_only=True)
class MemberItem(Base):
    __tablename__ = "member"

    username: Mapped[str] = mapped_column(primary_key=True)
    avatar_url: Mapped[str]
    create_at: Mapped[int]
    social_link: Mapped[list[dict[str, str]]]
    no: Mapped[int]
