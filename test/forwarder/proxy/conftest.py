import os

import pytest
from hypothesis import settings

from forwarder import connection
from forwarder import options
from forwarder.addons.proxyserver import Proxyserver
from forwarder.proxy import context


@pytest.fixture
def tctx() -> context.Context:
    opts = options.Options()
    Proxyserver().load(opts)
    return context.Context(
        connection.Client(
            peername=("client", 1234),
            sockname=("127.0.0.1", 8080),
            timestamp_start=1605699329,
            state=connection.ConnectionState.OPEN,
        ),
        opts,
    )


settings.register_profile("fast", max_examples=10)
settings.register_profile("deep", max_examples=100_000, deadline=None)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "fast"))
