import collections

import urwid

from forwarder import log
from forwarder.tools.console import layoutwidget


class LogBufferWalker(urwid.SimpleListWalker):
    pass


class EventLog(urwid.ListBox, layoutwidget.LayoutWidget):
    keyctx = "eventlog"
    title = "Events"

    def __init__(self, master):
        self.master = master
        self.walker = LogBufferWalker(collections.deque(maxlen=self.master.events.size))

        master.events.sig_add.connect(self.add_event)
        master.events.sig_refresh.connect(self.refresh_events)
        self.master.options.subscribe(
            self.refresh_events, ["console_eventlog_verbosity"]
        )
        self.refresh_events()

        super().__init__(self.walker)

    def load(self, loader):
        loader.add_option(
            "console_focus_follow", bool, False, "Focus follows new flows."
        )

    def set_focus(self, index):
        if 0 <= index < len(self.walker):
            super().set_focus(index)

    def keypress(self, size, key):
        if key == "m_end":
            self.set_focus(len(self.walker) - 1)
        elif key == "m_start":
            self.set_focus(0)
        return super().keypress(size, key)

    def add_event(self, entry: log.LogEntry):
        if log.log_tier(self.master.options.console_eventlog_verbosity) < log.log_tier(
            entry.level
        ):
            return
        txt = f"{entry.level}: {str(entry.msg)}"
        if entry.level in ("error", "warn", "alert"):
            e = urwid.Text((entry.level, txt))
        else:
            e = urwid.Text(txt)
        self.walker.append(e)
        if self.master.options.console_focus_follow:
            self.walker.set_focus(len(self.walker) - 1)

    def refresh_events(self, *_) -> None:
        self.walker.clear()
        for event in self.master.events.data:
            self.add_event(event)
