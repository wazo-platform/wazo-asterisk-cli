# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import pprint

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import ListBuildingMixin


class ChannelsShow(ListBuildingMixin, Lister):
    "Show Channels"

    _columns = ['call_id', 'caller_id_num', 'caller_id_name', 'callee', 'channel', 'context', 'exten', 'application', 'state', 'duration']

    def take_action(self, parsed_args):
        channels = self.app.client.action('CoreShowChannels')

        if len(channels) < 1:
            return (), ()

        results = []
        for channel in channels:
            if channel.get('Event') == 'CoreShowChannel':
                exten = channel.get('ChanVariable').get('XIVO_BASE_EXTEN')

                results.append({
                    'call_id': channel['Uniqueid'],
                    'channel': channel['Channel'],
                    'caller_id_num': channel['CallerIDNum'],
                    'caller_id_name': channel['CallerIDName'],
                    'duration': channel['Duration'],
                    'state': channel['ChannelStateDesc'],
                    'context': channel['Context'],
                    'exten': channel['Exten'],
                    'callee': exten,
                    'application': channel['Application'],
                })
                
        headers = self.extract_column_headers(results[0])
        items = self.extract_items(headers, results)
        return headers, items
