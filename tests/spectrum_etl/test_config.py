#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on October 17, 2019

@author: pashaa@mskcc.org
'''

import pytest


def test_get_redcap_config():
    from spectrum_etl.config import Config

    config = Config(config_file='tests/spectrum_etl/test_config.yaml')
    assert config.get_redcap_token(instance_name='test') == 'test_redcap_token_1234'
    assert config.get_redcap_api_url() == 'https://test.url/api/'


def test_get_elab_config():
    from spectrum_etl.config import Config

    config = Config(config_file='tests/spectrum_etl/test_config.yaml')
    assert config.get_elab_api_token() == 'test_elab_token_1234'


