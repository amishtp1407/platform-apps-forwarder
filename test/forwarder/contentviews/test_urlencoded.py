from . import full_eval
from forwarder.contentviews import urlencoded
from forwarder.net.http import url


def test_view_urlencoded():
    v = full_eval(urlencoded.ViewURLEncoded())

    d = url.encode([("one", "two"), ("three", "four")]).encode()
    assert v(d)

    d = url.encode([("adsfa", "")]).encode()
    assert v(d)

    assert not v(b"\xff\x00")


def test_render_priority():
    v = urlencoded.ViewURLEncoded()
    assert v.render_priority(b"data", content_type="application/x-www-form-urlencoded")
    assert not v.render_priority(b"data", content_type="text/plain")
