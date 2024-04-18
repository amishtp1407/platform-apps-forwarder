from forwarder.addons import anticomp
from forwarder.test import taddons
from forwarder.test import tflow


class TestAntiComp:
    def test_simple(self):
        sa = anticomp.AntiComp()
        with taddons.context(sa) as tctx:
            f = tflow.tflow(resp=True)
            sa.request(f)

            tctx.configure(sa, anticomp=True)
            f = tflow.tflow(resp=True)

            f.request.headers["Accept-Encoding"] = "foobar"
            sa.request(f)
            assert f.request.headers["Accept-Encoding"] == "identity"
