# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

from sqlalchemy import JSON, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
    author: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str]
    node: Mapped[str] = mapped_column(nullable=False)
    tag: Mapped[list[str]] = mapped_column(nullable=False)
    clicks: Mapped[int] = mapped_column(nullable=False)
    votes: Mapped[int] = mapped_column(nullable=False)
    create_at: Mapped[int] = mapped_column(nullable=False)


@dataclass(kw_only=True)
class TopicSupplementItem(Base):
    __tablename__ = "topic_supplement"

    topic_id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    create_at: Mapped[int] = mapped_column(nullable=False)


@dataclass(kw_only=True)
class CommentItem(Base):
    __tablename__ = "comment"

    id_: Mapped[int] = mapped_column(name="id", primary_key=True)
    topic_id: Mapped[int] = mapped_column(nullable=False)
    commenter: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    thank_count: Mapped[int] = mapped_column(nullable=False)
    create_at: Mapped[int] = mapped_column(nullable=False)


@dataclass(kw_only=True)
class MemberItem(Base):
    __tablename__ = "member"

    username: Mapped[str] = mapped_column(primary_key=True)
    avatar_url: Mapped[str]
    create_at: Mapped[int] = mapped_column(nullable=False)
    social_link: Mapped[list[dict[str, str]]]
    no: Mapped[int] = mapped_column(nullable=False)
