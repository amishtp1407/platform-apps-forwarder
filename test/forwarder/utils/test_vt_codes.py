import io

from forwarder.utils.vt_codes import ensure_supported


def test_simple():
    assert not ensure_supported(io.StringIO())
