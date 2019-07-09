#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 30, 2019

@author: pashaa@mskcc.org
'''

from openpyxl import load_workbook
import pytest
from openpyxl.styles import Protection
from spectrum_etl.edc.Surgeries import Surgeries

from spectrum_etl.edc.patient import Patient
from spectrum_etl.edc.patient import MRN_CELL
from spectrum_etl.edc.patient import ID_CELL
from spectrum_etl.edc.constants import COLOR_PROCESSED


class TestSurgeries(object):
    """Tests for `edc.patient` module."""
    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.tmpdir = tmpdir



    def teardown_method(self, tmpdir):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        self.tmpdir = None

    def test_valid_surgeries(self):
        wb = load_workbook('tests/spectrum_etl/edc/data/surgeries_valid.xlsx')
        surgeries_sheet = wb['surgeries']

        surgeries = Surgeries(surgeries_sheet)
        #assert patient.get_mrn() == 12345
        #assert patient.get_id() == 'SPECTRUM-OV-001'

    def test_invalid_type(self):
        pass

    def test_invalid_count_non_int(self):
        pass

    def test_missing_type(self):
        pass

    def test_missing_count(self):
        pass

