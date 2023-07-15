# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
from dataclasses import dataclass

from sqlalchemy import Integer, Text, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class JSONText(types.TypeDecorator):
    impl = types.Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value, ensure_ascii=False)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


@dataclass
class Base(DeclarativeBase):
    type_annotation_map = {
        list[str]: JSONText,
        list[dict[str, str]]: JSONText,
        int: Integer,
        str: Text,
    }


@dataclass(kw_only=True)
class TopicItem(Base):
    __tablename__ = "topic"

    id_: Mapped[int] = mapped_column(name="id", primary_key=True)
    author: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column()
    node: Mapped[str] = mapped_column(nullable=False)
    tag: Mapped[list[str]] = mapped_column(nullable=False)
    clicks: Mapped[int] = mapped_column(nullable=False)
    votes: Mapped[int] = mapped_column(nullable=False)
    create_at: Mapped[int] = mapped_column(nullable=False)
    thank_count: Mapped[int] = mapped_column(nullable=False)
    favorite_count: Mapped[int] = mapped_column(nullable=False)
    reply_count: Mapped[int] = mapped_column(nullable=False)

    @staticmethod
    def err_topic(topic_id: int):
        return TopicItem(
            id_=topic_id,
            author="",
            title="",
            content="",
            create_at=0,
            node="",
            tag=[],
            clicks=-1,
            votes=-1,
            thank_count=-1,
            favorite_count=-1,
            reply_count=-1,
        )


@dataclass(kw_only=True)
class TopicSupplementItem(Base):
    __tablename__ = "topic_supplement"

    topic_id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(primary_key=True)
    create_at: Mapped[int] = mapped_column(primary_key=True)


@dataclass(kw_only=True)
class CommentItem(Base):
    __tablename__ = "comment"

    id_: Mapped[int] = mapped_column(name="id", primary_key=True)
    # index used for select count(*) from comment where topic_id = ?, see DB.get_topic_comment_count
    topic_id: Mapped[int] = mapped_column(nullable=False, index=True)
    commenter: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    thank_count: Mapped[int] = mapped_column(nullable=False)
    create_at: Mapped[int] = mapped_column(nullable=False)
    no: Mapped[int] = mapped_column(nullable=False)


@dataclass(kw_only=True)
class MemberItem(Base):
    __tablename__ = "member"
    """
    crawl user from topic and comment, then crawl from uid 1 to 1000000,
    if get 404, username/uid will be ''/-1, so primary_key(uid ,username)
    """
    uid: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(primary_key=True, index=True)
    avatar_url: Mapped[str]
    create_at: Mapped[int] = mapped_column(nullable=False)
    social_link: Mapped[list[dict[str, str]]]
