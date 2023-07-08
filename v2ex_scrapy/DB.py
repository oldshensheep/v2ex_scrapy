import json
from dataclasses import dataclass
from typing import Type, Union

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Mapped, Session, mapped_column

from v2ex_scrapy.items import Base, CommentItem, MemberItem, TopicItem


@dataclass(kw_only=True)
class LogItem(Base):
    __tablename__ = "log"

    id_: Mapped[int] = mapped_column(name="id", primary_key=True, autoincrement="auto")
    url: Mapped[str] = mapped_column()
    status_code: Mapped[int] = mapped_column(nullable=False)
    create_at: Mapped[int] = mapped_column(nullable=False)


class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database_name="v2ex.sqlite"):
        self.engine = create_engine(
            f"sqlite:///{database_name}",
            echo=False,
            json_serializer=lambda x: json.dumps(x, ensure_ascii=False),
        )
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def close(self):
        self.session.commit()
        self.session.close()

    def exist(
        self,
        type_: Union[Type[TopicItem], Type[CommentItem], Type[MemberItem]],
        q: Union[str, int],
    ) -> bool:
        if type_ == MemberItem:
            query = text(
                f"SELECT * FROM {type_.__tablename__} WHERE {'username' if type(q) == str else 'uid'} = :q"
            )
        else:
            query = text(f"SELECT * FROM {type_.__tablename__} WHERE id = :q")
        result = self.session.execute(query, {"q": q}).fetchone()
        return result is not None

    def get_max_topic_id(self) -> int:
        result = self.session.execute(text("SELECT max(id) FROM topic")).fetchone()
        if result is None or result[0] is None:
            return 1
        return int(result[0])

    def get_topic_comment_count(self, topic_id) -> int:
        result = self.session.execute(
            text("select reply_count from topic where id = :q"), {"q": topic_id}
        ).fetchone()
        if result is None or result[0] is None:
            return 0
        return int(result[0])
