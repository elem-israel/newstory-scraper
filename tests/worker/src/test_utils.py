from datetime import datetime

from worker.src.util import extract_profile, extract_posts


def test_extract_profile(profile):
    extracted = extract_profile(profile)
    assert extracted == {
        "created_at": "2020-10-07T13:27:44.758211",
        "profile_created_at": datetime(2010, 10, 6, 0, 0),
        "instagram_profile_id": "11472474315",
        "biography": "He/him\nSelf taught \n🇮🇱\nSupport me on ko fi ?:)",
        "followers_count": 192,
        "following_count": 313,
        "full_name": "Xan (Storm Alexander)",
        "is_business_account": False,
        "is_private": False,
        "posts_count": 42,
        "profile_pic_url": "https://instagram.ftzl1-1.fna.fbcdn.net/v/t51.2885-19/s150x150/106587108_280349786537053_1306958651287526582_n.jpg?_nc_ht=instagram.ftzl1-1.fna.fbcdn.net&_nc_ohc=KGaVDavuR4IAX_Zbeek&oh=2a1cca6654e9909028f284ab39e8062f&oe=5FA5DB25",
    }


def test_extract_posts(profile):
    extracted = extract_posts(profile)
    isinstance(extracted[0]["instagram_post_id"], str)
    isinstance(extracted[0]["caption"], str)
    isinstance(extracted[0]["taken_at"], datetime)
    assert extracted[0]["instagram_author_profile_id"] == "11472474315"
    assert len(extracted) == 42
