DROP TABLE IF EXISTS fact_profiles;
CREATE TABLE fact_profiles
(
    id                   INT IDENTITY (1,1) UNIQUE,
    username             varchar(256),
    instagram_profile_id NVARCHAR(MAX) NOT NULL,
    is_private           BIT,
    is_business_account  BIT,
    posts_count          INT,
    profile_pic_url      NVARCHAR(MAX),
    biography            NVARCHAR(MAX),
    followers_count      INT,
    following_count      INT,
    full_name            NVARCHAR(MAX),
    profile_created_at   DATETIME,
    created_date         DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username, created_date)
);

ALTER TABLE fact_profiles
    ADD CONSTRAINT u_id unique (id);

DROP TABLE IF EXISTS fact_posts;
CREATE TABLE fact_posts
(
    id                          INT IDENTITY (1,1) UNIQUE,
    instagram_post_id           VARCHAR(256),
    instagram_author_profile_id NVARCHAR(MAX) NOT NULL,
    caption                     NVARCHAR(MAX),
    likes_count                 INT,
    taken_at                    DATETIME,
    created_date                DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (instagram_post_id, created_date)
);

DROP TABLE IF EXISTS reports;
CREATE TABLE reports
(
    id           INT IDENTITY (1,1) PRIMARY KEY,
    resource     NVARCHAR(MAX),
    resource_id  INT,
    details      NVARCHAR(MAX),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
);