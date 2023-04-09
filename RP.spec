# -*- mode: python ; coding: utf-8 -*-

import os
import glob

def collect_data_files(src_folder):
    data_files = []
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith('.txt'):
                source_file = os.path.join(root, file)
                dest_folder = os.path.join('data_files', os.path.relpath(root, src_folder))
                data_files.append((source_file, dest_folder))
    return data_files


txt_files = collect_data_files('./data_files')

block_cipher = None


a = Analysis(
    ['RP.py'],
    pathex=[r"C:\Users\Gabi\Desktop\RP_executable"],
    binaries=[],
    datas=txt_files,
    hiddenimports=[],
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
upx=False
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RP executable',
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
