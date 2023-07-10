import pandas
import sqlite3


conn = sqlite3.connect("v2ex.sqlite")

e = {
    "top-comment": """
select topic_id, c.id, c.content, c.thank_count, c.no, t.title
from comment c
         left join topic t on t.id = c.topic_id
order by c.thank_count desc
""",
    "top-topic-by-thank_count": """
select id, title, thank_count
from topic
order by thank_count desc
""",
    "top-topic-by-favorite_count": """
select id, title, favorite_count
from topic
order by favorite_count desc
""",
    "top-topic-by-votes": """
select id, title, votes
from topic
order by votes desc
""",
    "top-topic-by-clicks": """
select id, title, clicks
from topic
order by clicks desc
""",
    "tag-usage-count": """
select t.value as tag, count(*) as count
from topic,
     json_each(tag) as t
group by t.value
order by count desc
""",
    "top-user-by-comment_count": """
select commenter as username, count(commenter) as comment_count
from comment
group by commenter
order by comment_count desc
""",
    "top-user-by-topic_count": """
select author as username, count(author) as topic_count
from topic
group by author
order by topic_count desc
""",
}
e2 = {
    "new-topic-every-month": """
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS topic_count
FROM topic
GROUP BY date
""",
    "new-comment-every-month": """
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS comment_count
FROM comment
GROUP BY date
""",
    "new-member-every-month": """
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS member_count
FROM member
GROUP BY date
""",
}
LIMIT = 20


def f(
    sql: str,
    export_name: str,
    conn,
    limit: int | None = LIMIT,
    orient: str | None = "records",
):
    ae = "" if limit is None else f" limit {limit}"
    pandas.read_sql(f"{sql} {ae}", conn).to_json(
        f"./analysis/v2ex-analysis/public/{export_name}.json",
        force_ascii=False,
        orient=orient,
    )


for i, sql in e.items():
    f(sql=sql, export_name=i, conn=conn)
for i, sql in e2.items():
    f(sql=sql, export_name=i, conn=conn, limit=None, orient=None)
