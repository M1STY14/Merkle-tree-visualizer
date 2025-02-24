# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all necessary hidden imports and data files
hidden_imports = [
    'hashlib',
    'networkx',
    'json',
    'PySide6.QtWidgets',
    'matplotlib',
    'matplotlib.backends.backend_qt5agg',
    'matplotlib.figure',
    'numpy'
]

# Collect additional data files (important for networkx and matplotlib)
datas = collect_data_files('networkx') + collect_data_files('matplotlib')

a = Analysis(
    ['appwindow.py'],
    pathex=[],
    binaries=[],
    datas=datas,  # Add collected data files
    hiddenimports=hidden_imports,
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
    a.datas,  # Ensure data files are included
    [],
    name='merkletreevisualizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want a command prompt for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
