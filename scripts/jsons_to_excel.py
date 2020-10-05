import json
import os
import pandas as pd


def main():
    profiles_dir = "D:/tmp/newstory/profiles"
    profiles = os.listdir(profiles_dir)
    res = [os.path.join(profiles_dir, p, "profile.json") for p in profiles if p]
    res = [p for p in res if os.path.exists(p)]
    users = []
    for p in res:
        with open(p, "r") as fp:
            profile = json.load(fp)
        try:
            users.append(profile["data"]["GraphProfileInfo"]["username"])
        except KeyError:
            try:
                users.append(profile["GraphProfileInfo"]["username"])
            except KeyError:
                print(profile)
                raise
    df = pd.DataFrame(index=users)
    df["קישור לפרופיל"] = "https://instagram.com/" + df.index.to_series()
    df["שנת לידה משוערת"] = ""
    df = df.rename_axis("שם משתמש")
    df.to_excel("D:/tmp/dob.xlsx", engine="xlsxwriter")


if __name__ == "__main__":
    main()
