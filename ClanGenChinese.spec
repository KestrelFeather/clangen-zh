# Windows preview build, independent of the upstream publishing pipeline.
from pathlib import Path

root = Path(SPECPATH)
a = Analysis(
    [str(root / 'main.py')],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (str(root / 'resources'), 'resources'),
        (str(root / 'sprites'), 'sprites'),
        (str(root / 'version.ini'), '.'),
        (str(root / 'changelog.txt'), '.'),
        (str(root / 'LICENSE.md'), '.'),
        (str(root / 'localization/PREVIEW.zh-CN.md'), '.'),
        (str(root / 'bin/OpenDataDirectory.bat'), '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[str(root / 'tools/frozen_smoke_hook.py')],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name='ClanGenChinese', debug=False, strip=False, upx=False,
    console=False, icon=str(root / 'resources/images/icon.png'),
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='ClanGenChinese')
