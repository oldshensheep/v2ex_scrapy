SELECT (SELECT COUNT(*) FROM comment) AS 评论数,
       (SELECT COUNT(*) FROM member)  AS 用户数,
       (SELECT COUNT(*) FROM topic)   AS 主题数;

-- where create_at between strftime('%s', '2013-01-01') and strftime('%s', '2014-12-31');

-- top comment by thank_count
select topic_id, c.id, c.content, c.thank_count, c.no, t.title
from comment c
         left join topic t on t.id = c.topic_id
order by c.thank_count desc;

-- top topic by thank_count
select id, title, votes
from topic
order by thank_count desc;

-- top topic by favorite_count
select id, title, favorite_count
from topic
order by favorite_count desc;

-- top topic by votes
select id, title, votes
from topic
order by votes desc;

-- top topic by clicks
select id, title, clicks
from topic
order by clicks desc;


-- top node
select node, count(node) as count
from topic
group by node
order by count desc;

-- comment number group by user
select commenter as username, count(commenter) as comment_count
from comment
group by commenter
order by comment_count desc;

-- topic number group by user
select author as username, count(author) as topic_count
from topic
group by author
order by topic_count desc;

-- topic number group by year-month
SELECT date,
       SUM(topic_count) OVER (ORDER BY date ) AS cumulative_topic_count
FROM (SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS topic_count
      FROM topic
      GROUP BY date)
ORDER BY date;

-- user number group by year-month
SELECT date,
       SUM(user_count) OVER (ORDER BY date ) AS cumulative_user_count
FROM (SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS user_count
      FROM member
      GROUP BY date)
ORDER BY date;

-- comment number group by year-month
SELECT date,
       SUM(comment_count) OVER (ORDER BY date ) AS cumulative_comment_count
FROM (SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS comment_count
      FROM comment
      GROUP BY date)
ORDER BY date;

-- new topic number group by year-month
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS topic_count
FROM topic
GROUP BY date;

-- new user number group by year-month
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS user_count
FROM member
GROUP BY date;

-- new comment number group by year-month
SELECT strftime('%Y-%m', create_at, 'unixepoch') AS date, COUNT(*) AS comment_count
FROM comment
GROUP BY date;

-- tag usage count
select t.value as tag, count(*) as count
from topic,
     json_each(tag) as t
group by t.value
order by count desc;

-- node usage count
select node, count(*) as count
from topic
group by node
order by count desc;
