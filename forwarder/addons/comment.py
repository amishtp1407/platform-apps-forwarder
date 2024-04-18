from collections.abc import Sequence

from forwarder import command
from forwarder import ctx
from forwarder import flow
from forwarder.hooks import UpdateHook


class Comment:
    @command.command("flow.comment")
    def comment(self, flow: Sequence[flow.Flow], comment: str) -> None:
        "Add a comment to a flow"

        updated = []
        for f in flow:
            f.comment = comment
            updated.append(f)

        ctx.master.addons.trigger(UpdateHook(updated))
