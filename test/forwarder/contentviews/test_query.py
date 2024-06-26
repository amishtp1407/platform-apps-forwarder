from . import full_eval
from forwarder.contentviews import query
from forwarder.test import tutils


def test_view_query():
    d = ""
    v = full_eval(query.ViewQuery())
    req = tutils.treq()
    req.query = [("foo", "bar"), ("foo", "baz")]
    f = v(d, http_message=req)
    assert f[0] == "Query"
    assert f[1] == [
        [("header", "foo: "), ("text", "bar")],
        [("header", "foo: "), ("text", "baz")],
    ]

    assert v(d) == ("Query", [])


def test_render_priority():
    view = query.ViewQuery()
    req = tutils.treq()
    req.query = [("foo", "bar"), ("foo", "baz")]
    assert view.render_priority(b"", http_message=req)
    assert not view.render_priority(b"")
