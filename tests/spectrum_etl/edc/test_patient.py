#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 29, 2019

@author: pashaa@mskcc.org
'''
from openpyxl import load_workbook
import pytest

from spectrum_etl.edc.patient import Patient


class TestPatient(object):
    """Tests for `edc.patient` module."""
    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.tmpdir = tmpdir
        wb = load_workbook('tests/spectrum_etl/edc/data/patient_valid.xlsx')
        self.patient_sheet = wb['patients']


    def teardown_method(self, tmpdir):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        self.tmpdir = None

    def test_valid_patient(self):
        self.patient = Patient(self.patient_sheet)
        assert self.patient.get_mrn() == 12345
        assert self.patient.get_id() == 'SPECTRUM-OV-001'
