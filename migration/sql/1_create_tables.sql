DROP TABLE IF EXISTS profiles;
CREATE TABLE profiles
(
    id                   INT PRIMARY KEY IDENTITY (1,1),
    instagram_profile_id  TEXT NOT NULL,
    followers_counter    INT,
    following_counter    INT,
    is_private           BIT,
    is_business          BIT,
    estimated_birth_year INT,
    created_date         datetime DEFAULT CURRENT_TIMESTAMP,
    updated_date         datetime DEFAULT CURRENT_TIMESTAMP,
    estimated_risk       INT
);

CREATE TABLE posts
(
    id                          INT PRIMARY KEY IDENTITY (1,1),
    instagram_post_id           TEXT NOT NULL,
    instagram_author_profile_id TEXT NOT NULL,
    created_date                date DEFAULT CURRENT_TIMESTAMP,
    likes_counter               INT,
    estimated_author_age        INT
);

CREATE TABLE post_hashtags
(
    id             INT PRIMARY KEY IDENTITY (1,1),
    hashtags       TEXT NOT NULL,
    human_mark     INT,
    mark_reason_id INT,
    comments       TEXT
);

CREATE TABLE post_text
(
    id             INT PRIMARY KEY IDENTITY (1,1),
    text           TEXT NOT NULL,
    human_mark     INT,
    mark_reason_id INT,
    comments       TEXT
);


CREATE TABLE post_images
(
    id             INT PRIMARY KEY IDENTITY (1,1),
    image_url      TEXT NOT NULL,
    human_mark     INT,
    mark_reason_id INT,
    comments       TEXT
);

CREATE TABLE post_comments
(
    id             INT PRIMARY KEY IDENTITY (1,1),
    comment        TEXT NOT NULL,
    mark           INT,
    mark_reason_id INT,
    comments       TEXT
);


CREATE TABLE stories
(
    id                 INT PRIMARY KEY IDENTITY (1,1),
    instagram_story_id VARCHAR(100) NOT NULL,
    story_image_url    TEXT         NOT NULL,
    human_mark         INT,
    mark_reason_id     INT,
    comments           TEXT
);

CREATE TABLE post_parts_marks
(
    id             INT PRIMARY KEY IDENTITY (1,1),
    post_id        VARCHAR(100) NOT NULL,
    post_part_id   INT,
    marker_id      INT          NOT NULL,
    mark           INT,
    mark_reason_id INT,
    comments       TEXT
);

CREATE TABLE stories_marks
(
    id             INT PRIMARY KEY IDENTITY (1,1),
    StoryId        VARCHAR(100) NOT NULL,
    MarkerId       INT          NOT NULL,
    StoryPartId    INT,
    mark           INT,
    mark_reason_id INT,
    comments       TEXT
);

CREATE TABLE post_parts_reasons
(
    id                INT PRIMARY KEY IDENTITY (1,1),
    post_part_mark_id VARCHAR(100) NOT NULL,
    mark_reason_id    INT
);

CREATE TABLE mark_reasons
(
    id     INT PRIMARY KEY IDENTITY (1,1),
    reason TEXT NOT NULL
);

CREATE TABLE post_parts
(
    id        INT IDENTITY (1,1) PRIMARY KEY,
    post_part TEXT NOT NULL
);