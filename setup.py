#!/usr/bin/env python

from setuptools import setup

setup(name='ItChatSh',
      version='1.0.6',
      description='Shell on WeChat based on ItChat',
      author='LI ZEYAN',
      url="https://github.com/lizeyan/itchatsh",
      author_email='zy-li14@hotmail.com',
      packages=['itchatsh'],
      license="MIT",
      install_requires=['requests', 'pyqrcode', 'itchat'],
      )

