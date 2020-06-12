# wazo-asterisk-cli
A command line interface for the wazo asterisk service

## Configuration

Configuration file can be added at the following locations:

```
~/.config/wazo-asterisk-cli/*.yml
/etc/wazo-asterisk-cli/conf.d/*.yml
/etc/wazo-asterisk-cli/config.yml
```

The `/etc/wazo-asterisk-cli/config.yml` is the default configuration file shipped with the debian package. This file should not be modified but can be used as a reference.

The `/etc/wazo-asterisk-cli/conf.d/*.yml` files will be used to override the default configuration file. System-wide configurations should be dropped in this directory.

The `~/.config/wazo-asterisk-cli/*.yml` files will be used to override the global configuration files for a given user. This directory will generally include files containing credentials.

The user's configuration file directory are not read automatically at the moment. wazo-asterisk-cli can be launched using the --config option to read this directory.

```sh
wazo-asterisk-cli --config ~/.config/wazo-asterisk-cli
```

The `WAZO_ASTERISK_CLI_CONFIG` environment variable can also be used to avoid having to use the `--config` option.

```sh
export WAZO_ASTERISK_CLI_CONFIG=~/.config/wazo-asterisk-cli
```

This line can also be added to the user's `~/.bashrc` to avoid typing it at each session

A credential files should be created for the root user when wazo-auth is installed

```sh
# cat ~/.config/wazo-asterisk-cli/050-credentials.yml
auth:
  username: wazo-asterisk-cli
  password: uwt1V5GILaJ6tFEZZzFM
  backend: wazo_user
```

## Commands

To specify which user, password, backend or hostname you can use config file or command line like

```sh
wazo-asterisk-cli --hostname mywazo --insecure --auth-username test --auth-password test --backend wazo_user <command> <args>
```

### Completion

```sh
wazo-asterisk-cli complete > /etc/bash_completion.d/wazo-asterisk-cli
```

### Aor

List Aor for specific endpoint

```sh
wazo-asterisk-cli aor list 1234
```

Delete Aor

```sh
wazo-asterisk-cli aor delete '39x6d34a;@1bca81459e7dd00675452bee7ec97c32'
```

### Other commands

```sh
wazo-asterisk-cli --help
```
