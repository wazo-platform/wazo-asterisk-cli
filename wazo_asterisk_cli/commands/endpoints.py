# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import pprint

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import ListBuildingMixin


class EndpointsList(ListBuildingMixin, Lister):
    "List endpoints"

    _columns = ['endpoint']

    def take_action(self, parsed_args):
        endpoints = self.app.client.action('PJSIPShowEndpoints')

        if len(endpoints) < 1:
            return (), ()

        results = []
        for endpoint in endpoints:
            if endpoint.get('Event') == 'EndpointList':
                results.append(
                    {
                        'endpoint': endpoint['ObjectName'],
                        'transport': endpoint['Transport'],
                        'aor': endpoint['Aor'],
                        'contacts': endpoint['Contacts'],
                        'state': endpoint['DeviceState'],
                    }
                )

        headers = self.extract_column_headers(results[0])
        items = self.extract_items(headers, results)
        return headers, items


class EndpointShow(Command):
    "Show endpoint"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help="The aor to delete")
        return parser

    def take_action(self, parsed_args):
        endpoint = parsed_args.identifier
        self.app.LOG.debug('Show endpoint %s', endpoint)
        endpoint = self.app.client.action('PJSIPShowEndpoint', {'Endpoint': endpoint})

        if len(endpoint) < 1:
            return (), ()

        endpoint.pop(0)
        endpoint.pop(-1)

        pprint.pprint(endpoint)
