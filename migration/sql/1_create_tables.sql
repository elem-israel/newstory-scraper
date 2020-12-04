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
    created_date         DATETIME DEFAULT CURRENT_TIMESTAMP
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
    created_date                DATETIME DEFAULT CURRENT_TIMESTAMP
);