# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Module for dealing with the hekit configuration file"""

from os import path
from typing import NamedTuple
from toml import load


class Config(NamedTuple):
    """Represents a config"""

    config_filename: str
    repo_location: str


class ConfigFileError(Exception):
    """Error for when config file """


def config_required(func):
    """Decorator that loads the config file before running the actual function"""

    def inner(args):
        try:
            # replace the filename with the actual config
            args.config = load_config(args.config)
            return func(args)
        except KeyError as e:
            raise ConfigFileError("Error while parsing config file\n", f"  {e!r}")

    return inner


def load_config(filename: str) -> Config:
    """Load a config file in TOML format"""
    expand = path.expanduser  # alias
    expanded_filename = expand(filename)
    toml_dict = load(expanded_filename)
    toml_dict = {k: expand(v) for k, v in toml_dict.items()}
    # deref kwargs this way, get exceptions unknown key for free
    return Config(expanded_filename, **toml_dict)
