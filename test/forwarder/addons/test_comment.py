from forwarder.addons.comment import Comment
from forwarder.test import taddons
from forwarder.test import tflow


def test_comment():
    c = Comment()
    f = tflow.tflow()

    with taddons.context():
        c.comment([f], "foo")

    assert f.comment == "foo"
