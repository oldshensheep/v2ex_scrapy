create table if not exists comment
(
    id          integer not null
        constraint comment_pk
            primary key,
    topic_id    integer not null,
    commenter   TEXT    not null,
    content     TEXT    not null,
    create_at   integer not null,
    thank_count integer not null
);

create table if not exists member
(
    username    TEXT    not null
        constraint member_pk
            primary key,
    avatar_url  TEXT,
    create_at   integer not null,
    social_link TEXT,
    no          integer not null
);

create unique index if not exists member_no_uindex
    on member (no);

create table if not exists topic
(
    id        integer not null
        constraint topic_pk
            primary key,
    author    TEXT    not null,
    create_at integer not null,
    title     TEXT    not null,
    content   integer TEXT,
    node      TEXT    not null,
    clicks    integer not null,
    tag       TEXT    not null,
    votes     integer
);
