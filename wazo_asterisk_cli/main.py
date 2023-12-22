# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import os.path
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from wazo_amid_client import Client as Amid
from wazo_auth_client import Client as Auth

from . import config

logging.getLogger('requests').setLevel(logging.ERROR)


class WazoAsteriskCLI(App):
    DEFAULT_VERBOSE_LEVEL = 0

    def __init__(self):
        super().__init__(
            description='A CLI for the asterisk service',
            command_manager=CommandManager('wazo_asterisk_cli.commands'),
            version='0.0.1',
        )
        self._current_token = None
        self._remove_token = False
        self._auth_client = None
        self._client = None
        self._backend = None

    def build_option_parser(self, *args, **kwargs):
        parser = super().build_option_parser(*args, **kwargs)
        config_path_from_env = os.getenv('WAZO_ASTERISK_CLI_CONFIG', None)
        config_path_default = os.path.expanduser(
            os.path.join('~', '.config', 'wazo-asterisk-cli')
        )
        parser.add_argument(
            '--config',
            default=(config_path_from_env or config_path_default),
            help='Extra configuration directory to override the system configuration',
        )
        parser.add_argument('--hostname', help='The wazo-auth hostname')
        parser.add_argument('--port', help='The wazo-auth port')

        https_verification = parser.add_mutually_exclusive_group()
        https_verification.add_argument('--ssl', help="Use ssl")
        https_verification.add_argument('--no-ssl', help="Don't use ssl")
        https_verification.add_argument(
            '--verify', action='store_true', help='Verify the HTTPS certificate or not'
        )
        https_verification.add_argument(
            '--insecure', action='store_true', help='Bypass certificate verification'
        )
        https_verification.add_argument('--cacert', help='Specify the ca bundle file')

        auth_or_token = parser.add_mutually_exclusive_group()
        auth_or_token.add_argument('--token', help='The wazo-auth token to use')

        username_password = auth_or_token.add_argument_group()
        username_password.add_argument(
            '--auth-username',
            metavar='auth_username',
            help='The username to use to retrieve a token',
        )
        username_password.add_argument(
            '--auth-password',
            metavar='auth_password',
            help='The password to use to retrieve a token',
        )
        username_password.add_argument(
            '--backend', help='The backend to use when authenticating'
        )

        return parser

    @property
    def client(self):
        if not self._auth_client:
            self._auth_client = Auth(**self._auth_config)

        if not self._current_token:
            self._backend = self._auth_config.pop('backend', None) or self._backend
            self._auth_client = Auth(**self._auth_config)
            args = {'expiration': 3600}
            if self._backend:
                args['backend'] = self._backend
            token_data = self._auth_client.token.new(**args)
            self._current_token = token_data['token']

        self._auth_client.set_token(self._current_token)

        self._client = Amid(**self._amid_config)
        self._client.set_token(self._current_token)

        return self._client

    @property
    def client_without_token(self):
        if not self._client:
            self._client = Auth(**self._auth_config)
        return self._client

    def initialize_app(self, argv):
        self.LOG.debug('Wazo Asterisk CLI')
        self.LOG.debug('options=%s', self.options)
        conf = config.build(self.options)
        self.LOG.debug('Starting with config: %s', conf)
        self._current_token = self.options.token

        self.LOG.debug('client args: %s', conf['auth'])
        self._auth_config = dict(conf['auth'])
        self._amid_config = dict(conf['amid'])

    def clean_up(self, cmd, result, err):
        if err:
            self.LOG.debug('got an error: %s', err)

        if self._remove_token:
            self._auth_client.token.revoke(self._current_token)
            self._remove_token = False


def main(argv=sys.argv[1:]):
    app = WazoAsteriskCLI()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
