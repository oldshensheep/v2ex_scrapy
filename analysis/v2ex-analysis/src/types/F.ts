export interface TopComment {
  topic_id: number;
  id: number;
  content: string;
  thank_count: number;
  no: number;
  title: string;
}

export enum TopicBy {
  clicks = "clicks",
  favorite_count = "favorite_count",
  thank_count = "thank_count",
  votes = "votes",
}
export enum UserBy {
  comment_count = "comment_count",
  topic_count = "topic_count",
}

export interface TopTopic {
  id: number;
  title: string;
  clicks?: number;
  favorite_count?: number;
  thank_count?: number;
  votes?: number;
}

export interface TopMember {
  username: string;
  comment_count?: number;
  topic_count?: number;
}

export interface TopTag {
  tag: string;
  count?: number;
}
