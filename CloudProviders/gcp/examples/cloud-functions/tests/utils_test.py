import utils as u
import base64
import functools as ft
from unittest.mock import Mock


def test_encode_decode():
    s = "Hello bob, how are you today?"
    assert s == ft.reduce(lambda x, y: y(x), [u.encode_payload, base64.b64encode, u.decode_payload], s)
    assert 'h' == u.decode_payload(b'aA'), 'Decode no longer handles incorrect padding'


def test_get_in():
    assert not u.get_in({}, ["bob"])
    assert not u.get_in({"g": 4}, [])
    assert 34 == u.get_in({"g": 34}, ["g"])
    assert 34 == u.get_in({"a": {"b": {"c": {"d": 34}}}}, ["a", "b", "c", "d"])
    assert not u.get_in({"a": {"b": {"c": {"d": 34}}}}, ["a", "c", "d"])


def test_args_parse(mocker):
    req = Mock()
    req.args = None
    req.get_json = lambda **kwargs: {"attr_1": 3}
    assert u.parse_request(req) == {"attr_1": 3}

    req.args = {"attr_2": 4}
    assert u.parse_request(req) == {"attr_1": 3, "attr_2": 4}
