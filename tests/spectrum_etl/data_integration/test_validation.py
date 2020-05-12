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

def test_is_downstream_submission_valid():
    assert is_downstream_submission_valid("Storage Only", "CD45+", "SPECTRUM-OV-001") == True
    assert is_downstream_submission_valid("Storage Only", "CD45-", "SPECTRUM-OV-001") == True
    assert is_downstream_submission_valid("Storage Only", "Unsorted", "SPECTRUM-OV-001") == True

    assert is_downstream_submission_valid("Storage Only", "", "SPECTRUM-OV-001") == False
    assert is_downstream_submission_valid("Storage Only", "abc", "SPECTRUM-OV-001") == False
    assert is_downstream_submission_valid("Storage Only", "CD45+", "SPECTRUM-OV-001") == False

#def test_is_submitted_populations_valid(submitted_populations, patient_id):

def test_is_scrna_igo_id_valid():
    assert is_scrna_igo_id_valid("A") == True
    assert is_scrna_igo_id_valid("ZZ") == True

    assert is_scrna_igo_id_valid("AAA") == False
    assert is_scrna_igo_id_valid("1") == False
    assert is_scrna_igo_id_valid("12") == False
    assert is_scrna_igo_id_valid("123") == False

def test_is_scrna_igo_sub_id_valid():
    assert is_scrna_igo_sub_id_valid("IGO-123456") == True

    assert is_scrna_igo_sub_id_valid("IGO-1234567") == False
    assert is_scrna_igo_sub_id_valid("IGO-12345") == False
    assert is_scrna_igo_sub_id_valid("IGO-abcdef") == False
    assert is_scrna_igo_sub_id_valid("IGO-123abc") == False
    assert is_scrna_igo_sub_id_valid("1234567") == False
    assert is_scrna_igo_sub_id_valid("IGO1234567") == False

def test_is_scrna_rex_id_valid():
    assert is_scrna_rex_id_valid("001RA_CD45P") == True
    assert is_scrna_rex_id_valid("001-1RA_CD45P") == True
    assert is_scrna_rex_id_valid("001RA_CD45N") == True
    assert is_scrna_rex_id_valid("001-1RA_CD45N") == True

    assert is_scrna_rex_id_valid("001RA-CD45P") == False
    assert is_scrna_rex_id_valid("12RA_CD45P") == False
    assert is_scrna_rex_id_valid("001RA_CD45") == False
    assert is_scrna_rex_id_valid("001Omentum_CD45P") == False
    assert is_scrna_rex_id_valid("001RACD45P") == False

def test_is_qc_checks_valid():
    assert is_qc_checks_valid("001RA_CD45P", "Passed cDNA QC, Passed Library QC") == True
    assert is_qc_checks_valid("001RA_CD45P", "Failed cDNA QC") == True

    assert is_qc_checks_valid("001RA_CD45P", "Failed cDNA") == False
    assert is_qc_checks_valid("001RA_CD45P", "") == False

def test_is_dlp_rex_id_valid():
    assert is_dlp_rex_id_valid("001RA_DLP") == True
    assert is_dlp_rex_id_valid("001-1RA_DLP") == True

    assert is_dlp_rex_id_valid("001RA_CD45P") == False
    assert is_dlp_rex_id_valid("001RA_T") == False
    assert is_dlp_rex_id_valid("001RA-DLP") == False

def test_is_wgs_tissue_type_valid():
    assert is_wgs_tissue_type_valid("Frozen Tissue") == True

    assert is_wgs_tissue_type_valid("FFPE Block") == False
    assert is_wgs_tissue_type_valid("Single Cell Suspensions") == False

def test_is_ppbc_acc_num_valid():
    assert is_ppbc_acc_num_valid("S19-12345") == True

    assert is_ppbc_acc_num_valid("S19_12345") == False
    assert is_ppbc_acc_num_valid("S19-1234") == False
    assert is_ppbc_acc_num_valid("S19-123456") == False
    assert is_ppbc_acc_num_valid("s19-12345") == False

def test_is_ppbc_bank_num_valid():
    assert is_ppbc_bank_num_valid("TS-12345") == True

    assert is_ppbc_bank_num_valid("AC-12345") == False
    assert is_ppbc_bank_num_valid("TS-1234") == False
    assert is_ppbc_bank_num_valid("TS-123456") == False
    assert is_ppbc_bank_num_valid("ts-12345") == False
    assert is_ppbc_bank_num_valid("TS_12345") == False

def test_is_wgs_igo_id_valid():
    assert is_wgs_igo_id_valid("A") == True
    assert is_wgs_igo_id_valid("ZZ") == True

    assert is_wgs_igo_id_valid("AAA") == False
    assert is_wgs_igo_id_valid("1") == False
    assert is_wgs_igo_id_valid("12") == False
    assert is_wgs_igo_id_valid("123") == False

def test_is_wgs_igo_submission_id_valid():
    assert is_wgs_igo_submission_id_valid("IGO-123456") == True

    assert is_wgs_igo_submission_id_valid("IGO-1234567") == False
    assert is_wgs_igo_submission_id_valid("IGO-12345") == False
    assert is_wgs_igo_submission_id_valid("IGO-abcdef") == False
    assert is_wgs_igo_submission_id_valid("IGO-123abc") == False
    assert is_wgs_igo_submission_id_valid("1234567") == False
    assert is_wgs_igo_submission_id_valid("IGO1234567") == False

def test_is_wgs_rex_id_valid():
    assert is_wgs_rex_id_valid("001RA_T") == True
    assert is_wgs_rex_id_valid("001-1RA_T") == True

    assert is_wgs_rex_id_valid("001RA_CD45P") == False
    assert is_wgs_rex_id_valid("001RA_DLP") == False
    assert is_wgs_rex_id_valid("001RA-T") == False

def test_is_if_tissue_type_valid():
    assert is_if_tissue_type_valid("FFPE Block") == True

    assert is_if_tissue_type_valid("Frozen Tissue") == False
    assert is_if_tissue_type_valid("Single Cell Suspensions") == False