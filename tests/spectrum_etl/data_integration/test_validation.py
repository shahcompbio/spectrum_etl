#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 07, 2020

@author: pashaa@mskcc.org
'''

import pytest

from spectrum_etl.data_integration.validation import is_pt_id_valid


def test_is_pt_id_valid():
    assert is_pt_id_valid("SPECTRUM-OV-001") == True
    assert is_pt_id_valid("SPECTRUM-OV-999") == True
    assert is_pt_id_valid("SPECTRUM-OV-001-1") == True
    assert is_pt_id_valid("SPECTRUM-OV-001-11") == True
    assert is_pt_id_valid("SPECTRUM-OV-999-99") == True

    assert is_pt_id_valid("SPECTRUM_OV_001") == False
    assert is_pt_id_valid("SPECTRUM-001") == False
    assert is_pt_id_valid("SPECTRUM-OV-01") == False
    assert is_pt_id_valid("SPECTRUM-OV-0001") == False

