#!/usr/bin/env python3
# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages


setup(
    name='wazo-asterisk-cli',
    version='1.0',
    author='Wazo Authors',
    author_email='dev@wazo.io',
    url='http://wazo.io',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['wazo-asterisk-cli = wazo_asterisk_cli.main:main'],
        'wazo_asterisk_cli.commands': [
            'aor_list = wazo_asterisk_cli.commands.aor:AorList',
            'aor_delete = wazo_asterisk_cli.commands.aor:AorDelete',
            'channels_show = wazo_asterisk_cli.commands.channels:ChannelsShow',
            'endpoints_list = wazo_asterisk_cli.commands.endpoints:EndpointsList',
            'endpoint_show = wazo_asterisk_cli.commands.endpoints:EndpointShow',
        ],
    },
)
