create table main.comment
(
    id          integer not null
        constraint comment_pk
            primary key,
    topic_id    integer not null,
    commenter   TEXT    not null,
    content     TEXT    not null,
    create_date integer not null
);

create table main.member
(
    username    TEXT    not null
        constraint member_pk
            primary key,
    avatar_url  TEXT,
    create_at   integer not null,
    social_link TEXT,
    no          integer not null
);

create table main.topic
(
    id          integer not null
        constraint topic_pk
            primary key,
    author      TEXT    not null,
    create_date integer not null,
    title       TEXT    not null,
    content     integer TEXT
);

