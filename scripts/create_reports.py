from concurrent.futures.thread import ThreadPoolExecutor
import json
import os

from dotenv import load_dotenv
import sqlalchemy as sa

load_dotenv()

engine = sa.create_engine(os.environ["DATABASE_CONNECTION_STRING"])

pmap = ThreadPoolExecutor(max_workers=os.cpu_count()).map


def main():
    with open("D:/tmp/newstory/followers.json") as fp:
        followers = json.load(fp)
    with open("D:/tmp/newstory/followers_list.txt") as fp:
        unlabeled = map(lambda x: x.strip(), fp.readlines())
    with open("D:/tmp/newstory/labeled_groups.txt") as fp:
        labeled = map(lambda x: x.strip(), fp.readlines())

    all_labeled = tuple(
        i
        for sublist in [
            followers.get(l, {}).get("data", {}).get("followers", []) for l in labeled
        ]
        for i in sublist
    )
    without_report = engine.execute(
        """select count(*), username, profiles.id id
    from (select row_number() over (partition by instagram_author_profile_id order by created_date desc) rn, *
          from fact_posts) posts
             left join fact_profiles profiles on instagram_author_profile_id = instagram_profile_id
             left join reports on profiles.id = reports.resource_id
    where rn = 1
      AND resource is null
      AND is_business_account = 0
      AND is_private = 0
      AND caption is not null
    group by username, profiles.id;"""
    )
    users = [
        ("profile", user.id, json.dumps({"SCORE": 10 if user in all_labeled else 0}))
        for user in without_report
    ]
    engine.execute(
        "INSERT INTO reports (resource, resource_id, details) VALUES (?,?,?)", *users
    )


if __name__ == "__main__":
    main()
