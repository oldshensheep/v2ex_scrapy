import plotly.express as px
import plotly.graph_objects as go
import pandas
import sqlite3

conn = sqlite3.connect("./v2ex.sqlite")
c = conn.cursor()

topic = pandas.read_sql(
    """
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS topic_count
FROM topic
GROUP BY date;
    """,
    conn,
)
# drop 1970
fig = px.line(
    topic[1:],
    x="date",
    y="topic_count",
)
fig.show()

comment = pandas.read_sql(
    """
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS comment_count
FROM comment
GROUP BY date;
    """,
    conn,
)
fig = px.line(
    comment,
    x="date",
    y="comment_count",
)
fig.show()

user = pandas.read_sql(
    """
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS user_count
FROM member
GROUP BY date;
    """,
    conn,
)


# drop 1970
fig = px.line(
    user[1:],
    x="date",
    y="user_count",
)

fig.show()
