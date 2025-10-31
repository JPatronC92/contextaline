# -*- mode: python ; coding: utf-8 -*-
# idf_onefile.spec - Onefile alternative with reduced scope
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

excluded_modules = [
    'pytest', 'unittest', 'test', 'tests',
    'sklearn.tests', 'numpy.tests', 'scipy.tests',
    'matplotlib', 'tensorflow', 'tensorboard', 'keras',
    'torch.testing', 'torchvision', 'torchaudio',
]

hidden = [
    'sentence_transformers',
    'sklearn',
    'sklearn.utils._weight_vector',
    'numpy.core._multiarray_umath',
    'pypdf',
    'docx',
]

st_datas = collect_data_files('sentence_transformers')

a = Analysis(
    ['src/app.py'],
    pathex=[],
    binaries=[],
    datas=st_datas,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='IntelligentDocumentFinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
