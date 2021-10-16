# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None


a = Analysis(['run.py'],
             pathex=['C:\\Users\\willw\\Documents\\GitHub\\Personal\\desktop-pet'],
             binaries=[],
             datas=[
                 ('README.md', '.'),
                 ('config.xml', '.'),
                 ('icon.ico', '.'),
                 ('src/sprites', 'src/sprites'),
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
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='DesktopPet',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='DesktopPet')


if sys.platform == 'darwin':
    app = BUNDLE(exe, 
            name="DesktopPet",
            icon=None)