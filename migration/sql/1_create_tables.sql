DROP TABLE IF EXISTS fact_profiles;
CREATE TABLE fact_profiles
(
    id                   INT PRIMARY KEY IDENTITY (1,1),
    username             TEXT,
    instagram_profile_id TEXT NOT NULL,
    followers_counter    INT,
    following_counter    INT,
    is_private           BIT,
    is_business_account  BIT,
    posts_count          INT,
    profile_pic_url      TEXT,
    biography            TEXT,
    followers_count      INT,
    following_count      INT,
    full_name            TEXT,
    created_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


DROP TABLE IF EXISTS fact_posts;
CREATE TABLE fact_posts
(
    id                          INT PRIMARY KEY IDENTITY (1,1),
    instagram_post_id           TEXT NOT NULL,
    instagram_author_profile_id TEXT NOT NULL,
    caption                     INT,
    likes_counter               INT,
    taken_at                    TIMESTAMP,
    created_date                TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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