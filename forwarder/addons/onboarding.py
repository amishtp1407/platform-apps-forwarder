from forwarder import ctx
from forwarder.addons import asgiapp
from forwarder.addons.onboardingapp import app

APP_HOST = "haltdos-ca.it"


class Onboarding(asgiapp.WSGIApp):
    name = "onboarding"

    def __init__(self):
        super().__init__(app, APP_HOST, None)

    def load(self, loader):
        loader.add_option(
            "onboarding", bool, False, "Toggle the mitmproxy onboarding app."
        )
        loader.add_option(
            "onboarding_host",
            str,
            APP_HOST,
            """
            Onboarding app domain. For transparent mode, use an IP when a DNS
            entry for the app domain is not present.
            """,
        )

    def configure(self, updated):
        self.host = ctx.options.onboarding_host
        app.config["CONFDIR"] = ctx.options.confdir

    async def request(self, f):
        if ctx.options.onboarding:
            await super().request(f)
