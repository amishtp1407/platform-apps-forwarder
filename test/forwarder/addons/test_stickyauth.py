import pytest

from forwarder import exceptions
from forwarder.addons import stickyauth
from forwarder.test import taddons
from forwarder.test import tflow


def test_configure():
    r = stickyauth.StickyAuth()
    with taddons.context(r) as tctx:
        tctx.configure(r, stickyauth="~s")
        with pytest.raises(exceptions.OptionsError):
            tctx.configure(r, stickyauth="~~")

        tctx.configure(r, stickyauth=None)
        assert not r.flt


def test_simple():
    r = stickyauth.StickyAuth()
    with taddons.context(r) as tctx:
        tctx.configure(r, stickyauth=".*")
        f = tflow.tflow(resp=True)
        f.request.headers["authorization"] = "foo"
        r.request(f)

        assert "address" in r.hosts

        f = tflow.tflow(resp=True)
        r.request(f)
        assert f.request.headers["authorization"] == "foo"
