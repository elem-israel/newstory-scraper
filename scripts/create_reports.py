from concurrent.futures.thread import ThreadPoolExecutor
import json
import os

from dotenv import load_dotenv
import sqlalchemy as sa
from tqdm import tqdm

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

    for g, score in ((unlabeled, 1), (labeled, 10)):
        for group in tqdm(g, leave=False):
            pbar = tqdm(followers[group]["data"]["followers"], leave=False)

            def send(profile):
                profile_id = engine.scalar(
                    """SELECT id from
                                (SELECT ROW_NUMBER() OVER(PARTITION BY username ORDER BY created_date DESC) AS rn, * FROM fact_profiles) t
                                    WHERE rn = 1 and username = ?""",
                    [profile],
                )
                if profile_id:
                    engine.execute(
                        "INSERT INTO reports (resource, resource_id, details) VALUES (?,?,?)",
                        ["profile", profile_id, json.dumps({"SCORE": score})],
                    )
                pbar.update()

            list(pmap(send, followers[group]["data"]["followers"]))


if __name__ == "__main__":
    main()
