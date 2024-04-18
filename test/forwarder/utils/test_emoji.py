from forwarder.tools.console.common import SYMBOL_MARK
from forwarder.utils import emoji


def test_emoji():
    assert emoji.emoji[":default:"] == SYMBOL_MARK
