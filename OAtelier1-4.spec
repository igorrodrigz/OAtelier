# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['AtelierWindow.py'],
             pathex=['D:\\PycharmProjects\\OAtelier-MR'],
             binaries=[],
             datas=[
                 ('logoMR.png', '.'),
                 ('BancoAtelier.db', '.'),
                 ('pena.ico', '.'),
                 ('styles.qss', '.'),
             ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure,
           cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OAtelier',
    icon='D:\\PycharmProjects\\OAtelier-MR\\pena.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    description='Software de Gestão de Clientes - MR Solutions',
    company_name='MR Solutions',
    copyright='Copyright (c) 2024 MR Solutions',
    author='Igor Rodrigues'
)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='OAtelier')
