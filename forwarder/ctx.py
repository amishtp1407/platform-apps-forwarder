from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import forwarder.log
    import forwarder.master
    import forwarder.options

master: forwarder.master.Master
options: forwarder.options.Options

log: forwarder.log.Log
"""Deprecated: Use Python's builtin `logging` module instead."""
