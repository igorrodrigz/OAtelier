# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['AtelierWindow.py'],  # Seu script principal
             pathex=['C:\\Users\\morei\\PycharmProjects\\OAtelier'],  # Caminho do seu projeto
             binaries=[],
             datas=[  # Incluindo arquivos adicionais
                 ('logo2.png', '.'),  # Adiciona o logo na mesma pasta do executável
                 ('BancoAtelier.db', '.'),  # Adiciona o banco de dados
                 ('pena.ico', '.'),  # Adiciona o ícone se necessário
                 ('styles.qss', '.'),  # Inclui o arquivo de estilos
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

# Removido o atributo a.zipped
pyz = PYZ(a.pure,
           cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='OAtelier',  # Nome do executável
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,  # False para não abrir console
          version='1.0.0',  # Versão do aplicativo
          description='Software de Gestão de Clientes - Atelier Recriar',  # Descrição do aplicativo
          company_name='MR Solutions',  # Nome da empresa
          copyright='Copyright (c) 2024 MR Solutions',  # Informação de copyright
          author='Igor Rodrigues'  # Nome do autor
          )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='OAtelier')
