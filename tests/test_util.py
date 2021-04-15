from util import get_username_by_id


def test_get_username_by_id():
    res = get_username_by_id(33070920)
    assert res == "pazarbel"
