import json

import pytest


@pytest.fixture
def profile():
    with open("tests/data/profile1.json") as fp:
        return json.load(fp)


@pytest.fixture
def tags():
    return json.load(open("tests/data/אנורקסיה.json", encoding="utf8"))
