# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import ListBuildingMixin


class AorList(ListBuildingMixin, Lister):
    "List aor"

    _columns = ['endpoint', 'aor', 'mobile']

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('endpoint', help='Endpoint name')
        return parser

    def take_action(self, parsed_args):
        endpoint = self.app.client.action('PJSIPShowEndpoint', {'Endpoint': parsed_args.endpoint})

        aors = []
        for e in endpoint:
            if e.get('AOR'):
                aors.append(e.get('ID'))

        result = []
        for aor in aors:
            r = self.app.client.action('DBGet', {'Family': 'registrar/contact', 'Key': aor})
            is_mobile = 'mobile' in r[1]['Val']
            result.append({'endpoint': parsed_args.endpoint, 'aor': r[1]['Key'], 'mobile': is_mobile})

        if len(result) < 1:
            return (), ()

        headers = self.extract_column_headers(result[0])
        items = self.extract_items(headers, result)
        return headers, items


class AorDelete(Command):
    "Delete aor"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help="The aor to delete")
        return parser

    def take_action(self, parsed_args):
        aor = parsed_args.identifier
        self.app.LOG.debug('Deleting aor %s', aor)
        self.app.client.action('DBDel', {'Family': 'registrar/contact', 'Key': aor})
