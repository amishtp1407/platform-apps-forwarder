from forwarder.addons import anticache
from forwarder.addons import anticomp
from forwarder.addons import block
from forwarder.addons import blocklist
from forwarder.addons import browser
from forwarder.addons import clientplayback
from forwarder.addons import command_history
from forwarder.addons import comment
from forwarder.addons import core
from forwarder.addons import cut
from forwarder.addons import disable_h2c
from forwarder.addons import dns_resolver
from forwarder.addons import export
from forwarder.addons import maplocal
from forwarder.addons import mapremote
from forwarder.addons import modifybody
from forwarder.addons import modifyheaders
from forwarder.addons import next_layer
from forwarder.addons import onboarding
from forwarder.addons import proxyauth
from forwarder.addons import proxyserver
from forwarder.addons import save
from forwarder.addons import savehar
from forwarder.addons import script
from forwarder.addons import serverplayback
from forwarder.addons import stickyauth
from forwarder.addons import stickycookie
from forwarder.addons import tlsconfig
from forwarder.addons import upstream_auth


def default_addons():
    return [
        core.Core(),
        browser.Browser(),
        block.Block(),
        blocklist.BlockList(),
        anticache.AntiCache(),
        anticomp.AntiComp(),
        clientplayback.ClientPlayback(),
        command_history.CommandHistory(),
        comment.Comment(),
        cut.Cut(),
        disable_h2c.DisableH2C(),
        export.Export(),
        onboarding.Onboarding(),
        proxyauth.ProxyAuth(),
        proxyserver.Proxyserver(),
        dns_resolver.DnsResolver(),
        script.ScriptLoader(),
        next_layer.NextLayer(),
        serverplayback.ServerPlayback(),
        mapremote.MapRemote(),
        maplocal.MapLocal(),
        modifybody.ModifyBody(),
        modifyheaders.ModifyHeaders(),
        stickyauth.StickyAuth(),
        stickycookie.StickyCookie(),
        save.Save(),
        savehar.SaveHar(),
        tlsconfig.TlsConfig(),
        upstream_auth.UpstreamAuth(),
    ]
