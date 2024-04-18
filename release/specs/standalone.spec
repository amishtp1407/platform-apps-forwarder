# -*- mode: python3 ; coding: utf-8 -*-

for tool in ["forwarder"]:
    excludes = []
    a = Analysis(
        [tool],
        excludes=excludes,
    )
    pyz = PYZ(a.pure, a.zipped_data)

    EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name=tool,
        console=True,
        icon='icon.ico',
    )
