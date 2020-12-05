DROP TABLE IF EXISTS fact_profiles;
CREATE TABLE fact_profiles
(
    id                   INT PRIMARY KEY IDENTITY (1,1),
    username             NVARCHAR(MAX),
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
    created_date         DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS fact_posts;
CREATE TABLE fact_posts
(
    id                          INT PRIMARY KEY IDENTITY (1,1),
    instagram_post_id           NVARCHAR(MAX) NOT NULL,
    instagram_author_profile_id NVARCHAR(MAX) NOT NULL,
    caption                     NVARCHAR(MAX),
    likes_count                 INT,
    taken_at                    DATETIME,
    created_date                DATETIME DEFAULT CURRENT_TIMESTAMP
);