# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['interfaz_optimizada.py'],
    pathex=[],
    binaries=[],
    datas=[('credenciales.json', '.'), ('memoria_servicios.json', '.'), ('config.py', '.'), ('ui_components.py', '.'), ('sheets_manager.py', '.'), ('validadores.py', '.')],
    hiddenimports=['googleapiclient', 'google.auth', 'google.oauth2'],
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
    name='Modulo de Internacion -V1.1',
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
    icon='icono.ico',
)
