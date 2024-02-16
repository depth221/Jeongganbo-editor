# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['jgb_editor/__main__.py', 'jgb_editor/jeonggan.py', 'jgb_editor/load_xml.py', 'jgb_editor/main.py', 'jgb_editor/pitch_etc_name.py', 'jgb_editor/pitch_name.py', 'jgb_editor/save_xml.py'],
    pathex=['jgb_editor'],
    binaries=[],
    datas=[('jgb_editor/style.css', 'jgb_editor'), ('jgb_editor/key_mapping.json', 'jgb_editor'), ('jgb_editor/image', 'jgb_editor/image')],
    hiddenimports=['PyQt5.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='jeongganbo_editor',
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
    icon='jgb_editor/image/logo.ico',
)
