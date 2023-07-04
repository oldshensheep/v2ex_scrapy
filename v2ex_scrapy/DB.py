import json
from typing import Type, Union

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from v2ex_scrapy.items import (
    Base,
    CommentItem,
    MemberItem,
    TopicItem,
)


class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.engine = create_engine(
            "sqlite:///v2ex2.sqlite",
            echo=False,
            json_serializer=lambda x: json.dumps(x, ensure_ascii=False),
        )
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

        self.a = {
            TopicItem: "topic",
            CommentItem: "comment",
            MemberItem: "member",
        }

    def close(self):
        self.session.commit()
        self.session.close()

    def exist(
        self, type_: Union[Type[TopicItem], Type[CommentItem], Type[MemberItem]], q
    ) -> bool:
        query = text(
            f"SELECT * FROM {self.a[type_]} WHERE {'username' if type_ == MemberItem else 'id'} = :q"
        )
        result = self.session.execute(query, {"q": q}).fetchone()
        return result is not None

    def get_max_topic_id(self) -> int:
        result = self.session.execute(text("SELECT max(id) FROM topic")).fetchone()
        if result is None or result[0] is None:
            return 1
        return int(result[0])
