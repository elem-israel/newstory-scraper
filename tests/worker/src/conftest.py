import json

import pytest


@pytest.fixture
def profile():
    with open("tests/data/profile1.json") as fp:
        return json.load(fp)
