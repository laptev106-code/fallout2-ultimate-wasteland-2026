# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher_nextgen/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('launcher_nextgen/ui', 'ui'),
        ('launcher_nextgen/checksums.json', '.'),
        ('launcher_nextgen/presets', 'presets')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Fallout2_NextGen_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['launcher_nextgen/ui/assets/vault13_icon.ico'],
)
