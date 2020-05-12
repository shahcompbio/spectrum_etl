#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 07, 2020

@author: pashaa@mskcc.org
'''

import pytest

from spectrum_etl.data_integration.validation import *

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

def test_is_mrn_valid():
    assert is_mrn_valid("12345678") == True
    assert is_mrn_valid("29385433") == True

    assert is_mrn_valid("") == False
    assert is_mrn_valid("a1234567") == False
    assert is_mrn_valid("1234567") == False
    assert is_mrn_valid("abcdefgh") == False

def test_is_surgery_id_valid():
    assert is_surgery_id_valid("0", "SPECTRUM-OV-001") == True
    assert is_surgery_id_valid("1", "SPECTRUM-OV-001-1") == True
    assert is_surgery_id_valid("99", "SPECTRUM-OV-001-99") == True
    assert is_surgery_id_valid("123", "SPECTRUM-OV-001-123") == True

    assert is_surgery_id_valid("0", "SPECTRUM-OV-001-1") == False
    assert is_surgery_id_valid("1", "SPECTRUM-OV-001-123") == False
    assert is_surgery_id_valid("1", "SPECTRUM-OV-001") == False

def test_is_patient_excluded():
    assert is_patient_excluded("No", "HGSC", "", "", "SPECTRUM-OV-001") == True
    assert is_patient_excluded("No", "HGSC/G3 Endometrioid", "", "", "SPECTRUM-OV-001") == True
    assert is_patient_excluded("Yes", "Clear Cell Carcinoma", "", "Diagnosis", "SPECTRUM-OV-001") == True
    assert is_patient_excluded("Yes", "Other", "Low Grade Serous", "Diagnosis", "SPECTRUM-OV-001") == True

    assert is_patient_excluded("No", "Clear Cell Carcinoma", "", "", "SPECTRUM-OV-001") == False
    assert is_patient_excluded("Yes", "", "", "Diagnosis", "SPECTRUM-OV-001") == False
    assert is_patient_excluded("Yes", "Clear Cell Carcinoma", "", "", "SPECTRUM-OV-001") == False
    assert is_patient_excluded("Yes", "", "", "", "SPECTRUM-OV-001") == False
    assert is_patient_excluded("Yes", "Other", "", "", "SPECTRUM-OV-001") == False

def test_is_specimen_site_valid():
    assert is_specimen_site_valid("Infracolic Omentum", "SPECTRUM-OV-001", "") == True
    assert is_specimen_site_valid("Right Adnexa", "SPECTRUM-OV-001", "Right Ovary") == True
    assert is_specimen_site_valid("Other", "SPECTRUM-OV-001", "Liver") == True

    assert is_specimen_site_valid("", "SPECTRUM-OV-001", "") == False
    assert is_specimen_site_valid("Cervix", "SPECTRUM-OV-001", "") == False
    assert is_specimen_site_valid("Other", "SPECTRUM-OV-001", "") == False

