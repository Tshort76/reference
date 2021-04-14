import clearcatalog_event_proxy.utils as u
import base64
import functools as ft


def test_encode_decode():
    s = "Hello bob, how are you today?"
    assert s == ft.reduce(lambda x, y: y(x), [u.encode_payload, base64.b64encode, u.decode_payload], s)
    assert 'h' == u.decode_payload(b'aA'), 'Decode no longer handles incorrect padding'
