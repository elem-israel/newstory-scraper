def dict_to_sql(table, dic, keys):
    columns = ",".join(keys)
    qs = ",".join("?" * len(keys))
    return (
        f"INSERT INTO {table} ({columns}) VALUES ({qs})",
        tuple(dic.get(k) for k in keys),
    )


def profile_to_sql(connection, profile):
    connection.execute(
        *dict_to_sql(
            "fact_profiles",
            profile,
            (
                "username",
                "instagram_profile_id",
                "is_private",
                "is_business_account",
                "posts_count",
                "profile_pic_url",
                "biography",
                "followers_count",
                "following_count",
                "full_name",
                "profile_created_at",
                "created_date",
            ),
        )
    )


def posts_to_sql(connection, posts):
    for p in posts:
        connection.execute(
            *dict_to_sql(
                "fact_posts",
                p,
                (
                    "instagram_post_id",
                    "instagram_author_profile_id",
                    "caption",
                    "likes_count",
                    "taken_at",
                    "created_date",
                ),
            )
        )

def photos_to_sql(connection, photos):
    for p in photos:
        connection.execute(
            *dict_to_sql(
                "fact_photos",
                p,
                (
                    "photo_path",
                    "post_id",
                    "username"
                ),
            )
        )
