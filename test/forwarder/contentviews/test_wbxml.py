from . import full_eval
from forwarder.contentviews import wbxml

datadir = "mitmproxy/contentviews/test_wbxml_data/"


def test_wbxml(tdata):
    v = full_eval(wbxml.ViewWBXML())

    assert v(b"\x03\x01\x6a\x00") == ("WBXML", [[("text", '<?xml version="1.0" ?>')]])
    assert v(b"foo") is None

    path = tdata.path(
        datadir + "data.wbxml"
    )  # File taken from https://github.com/davidpshaw/PyWBXMLDecoder/tree/master/wbxml_samples
    with open(path, "rb") as f:
        input = f.read()
    with open("-formatted.".join(path.rsplit(".", 1))) as f:
        expected = f.read()

    p = wbxml.ASCommandResponse.ASCommandResponse(input)
    assert p.xmlString == expected


def test_render_priority():
    v = wbxml.ViewWBXML()
    assert v.render_priority(b"data", content_type="application/vnd.wap.wbxml")
    assert v.render_priority(b"data", content_type="application/vnd.ms-sync.wbxml")
    assert not v.render_priority(b"data", content_type="text/plain")
