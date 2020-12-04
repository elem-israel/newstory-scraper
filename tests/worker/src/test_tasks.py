import os

import pytest
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()
from worker.src.util import extract_profile


engine = sa.create_engine(os.environ["SQLALCHEMY_URL"])


@pytest.mark.skip("skip tests that rely on database for now")
def test_insert_to_db(profile):
    profile = extract_profile(profile)
    engine.execute(
        """INSERT INTO fact_profiles
        (
        username,
        instagram_profile_id,
        is_private,
        is_business_account,
        posts_count,
        profile_pic_url,
        biography,
        followers_count,
        following_count,
        full_name,
        created_date)                 
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        [
            profile.get(k)
            for k in (
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
                "created_date",
            )
        ],
    )
