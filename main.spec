# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 我称呼打包后软件运行时会有一个临时文件夹称为虚拟路径，而本地磁盘的路径称为真实路径。你如果有生成视频的功能，那么需要和我一样copyFiles方法本地的拷贝到虚拟路径上，而不是映射进去，因为这里的datas不和docker一样是卷映射，也就是不是双向映射，所以还是建议拷贝到虚拟路径，虚拟路径生成以后如果以后还要看的，每次生成后保存到真实路径一份。
# 也就是说background.jpg不会有修改的我称之为固定资源，打好包以后就不修改了，像texts.json的内容作为数据库要修改的，就用copyFiles方法，再每次保存到磁盘上
a = Analysis(
    ['main.py'],
    pathex=['D:/Demos/social-auto-upload-main'],
    datas=[
        ('douyin_uploader/', 'douyin_uploader/'),  # Ensure JSON file is included
        ('bilibili_uploader/', 'bilibili_uploader/'),    # Ensure audio file is included
        ('tencent_uploader/', 'tencent_uploader/'),    # Ensure audio file is included
        ('utils', 'utils'),  # Ensure the video files directory is included
        ('staticSource/', 'staticSource/'),  # Ensure the video files directory is included
    ],
    hiddenimports=[
        'babel.numbers',
        'tkcalendar'
    ],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    cipher=block_cipher,
    noarchive=False
)
