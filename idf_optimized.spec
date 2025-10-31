# -*- mode: python ; coding: utf-8 -*-
# idf_optimized.spec - Folder mode optimized to exclude tests and heavy modules
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

excluded_modules = [
    # Test suites
    'pytest', 'test', 'tests',
    'sklearn.tests', 'numpy.tests', 'scipy.tests',
    'sentence_transformers.tests',

    # Heavy or unused
    'matplotlib', 'tensorflow', 'tensorboard', 'keras',
    'notebook', 'jupyter', 'ipython',
    'torchvision', 'torchaudio', 'torch.testing',

    # Backends often unused in this app
    'torch.distributed', 'torch.multiprocessing',
    'numpy.distutils',
]

# Minimal hidden imports required by sklearn / sentence-transformers
hidden = [
    'sentence_transformers',
    'sklearn',
    'sklearn.utils._weight_vector',
    'sklearn.metrics._pairwise_fast',
    'numpy.core._multiarray_umath',
    'pypdf',
    'docx',
]

# Data files from sentence_transformers (tokenizers/configs)
st_datas = collect_data_files('sentence_transformers')

a = Analysis(
    ['src/app.py'],
    pathex=[],
    binaries=[],
    datas=[('src/license.py', '.'), ('src/app_version.py', '.')] + st_datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_modules,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='IntelligentDocumentFinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # keep stability
    console=True,  # show console for logs during first runs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='IntelligentDocumentFinder',
)
