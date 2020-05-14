#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 07, 2020

@author: pashaa@mskcc.org
'''

import pytest

from spectrum_etl.data_integration.validation import *

def test_is_pt_id_valid():

    assert is_pt_id_valid({"Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_pt_id_valid({"Patient ID":"SPECTRUM-OV-999"}) == True
    assert is_pt_id_valid({"Patient ID":"SPECTRUM-OV-999"}) == True
    assert is_pt_id_valid({"Patient ID":"SPECTRUM-OV-001-1"}) == True
    assert is_pt_id_valid({"Patient ID":"SPECTRUM-OV-001-11"}) == True
    assert is_pt_id_valid({"Patient ID":"SPECTRUM-OV-999-99"}) == True

    assert is_pt_id_valid({"Patient ID":"SPECTRUM_OV_001"}) == False
    assert is_pt_id_valid({"Patient ID":"SPECTRUM-001"}) == False
    assert is_pt_id_valid({"Patient ID":"SPECTRUM-OV-01"}) == False
    assert is_pt_id_valid({"Patient ID":"SPECTRUM-OV-0001"}) == False

def test_is_mrn_valid():
    assert is_mrn_valid({"MRN":"12345678"}) == True
    assert is_mrn_valid({"MRN":"29385433"}) == True

    assert is_mrn_valid({"MRN":""}) == False
    assert is_mrn_valid({"MRN":"a1234567"}) == False
    assert is_mrn_valid({"MRN":"1234567"}) == False
    assert is_mrn_valid({"MRN":"abcdefgh"}) == False

def test_is_surgery_id_valid():
    assert is_surgery_id_valid({"Patient ID":"SPECTRUM-OV-001", "Surgery ID":"0", }) == True
    assert is_surgery_id_valid({"Patient ID":"SPECTRUM-OV-001-1", "Surgery ID":"1",}) == True
    assert is_surgery_id_valid({"Patient ID":"SPECTRUM-OV-001-99", "Surgery ID":"99"}) == True
    assert is_surgery_id_valid({"Patient ID":"SPECTRUM-OV-001-123", "Surgery ID":"123"}) == True

    assert is_surgery_id_valid({"Patient ID":"SPECTRUM-OV-001-1", "Surgery ID":"0"}) == False
    assert is_surgery_id_valid({"Patient ID":"SPECTRUM-OV-001-123", "Surgery ID":"1"}) == False
    assert is_surgery_id_valid({"Patient ID":"SPECTRUM-OV-001", "Surgery ID":"1"}) == False

def test_is_patient_excluded():
    assert is_patient_excluded({"Excluded":"No", "Final Pathology":"HGSC", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_patient_excluded({"Excluded":"No", "Final Pathology":"HGSC/G3 Endometrioid", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_patient_excluded({"Excluded":"Yes", "Final Pathology":"Clear Cell Carcinoma", "Reason for Exclusion":"Diagnosis", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_patient_excluded({"Excluded":"Yes", "Final Pathology":"Other", "Specify Diagnosis":"Low Grade Serous", "Reason for Exclusion":"Diagnosis", "Patient ID":"SPECTRUM-OV-001"}) == True

    assert is_patient_excluded({"Excluded":"No", "Final Pathology":"Clear Cell Carcinoma", "Patient ID":"SPECTRUM-OV-001"}) == False
    assert is_patient_excluded({"Excluded":"Yes", "Final Pathology":"", "Reason for Exclusion":"Diagnosis", "Patient ID":"SPECTRUM-OV-001"}) == False
    assert is_patient_excluded({"Excluded":"Yes", "Final Pathology":"Clear Cell Carcinoma", "Reason for Exclusion":"", "Patient ID":"SPECTRUM-OV-001"}) == False
    assert is_patient_excluded({"Excluded":"Yes", "Final Pathology":"", "Patient ID":"SPECTRUM-OV-001"}) == False
    assert is_patient_excluded({"Excluded":"Yes", "Final Pathology":"Other", "Specify Diagnosis":"", "Reason for Exclusion":"Diagnosis", "Patient ID":"SPECTRUM-OV-001"}) == False

def test_is_specimen_site_valid():
    assert is_specimen_site_valid({"Specimen Site":"Infracolic Omentum", "Site Details":"", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_specimen_site_valid({"Specimen Site":"Right Adnexa", "Site Details":"Right Ovary", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_specimen_site_valid({"Specimen Site":"Other", "Site Details":"Liver", "Patient ID":"SPECTRUM-OV-001"}) == True

    assert is_specimen_site_valid({"Specimen Site":"", "Site Details":"", "Patient ID":"SPECTRUM-OV-001"}) == False
    assert is_specimen_site_valid({"Specimen Site":"Cervix", "Site Details":"", "Patient ID":"SPECTRUM-OV-001"}) == False
    assert is_specimen_site_valid({"Specimen Site":"Other", "Site Details":"", "Patient ID":"SPECTRUM-OV-001"}) == False

def test_is_downstream_submission_valid():
    assert is_downstream_submission_valid({"Downstream Submission":"Storage Only", "Storage Populations":"CD45+", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_downstream_submission_valid({"Downstream Submission":"Storage Only", "Storage Populations":"CD45-", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_downstream_submission_valid({"Downstream Submission":"Storage Only", "Storage Populations":"Unsorted", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_downstream_submission_valid({"Downstream Submission":"Storage Only", "Storage Populations":"CD45+", "Patient ID":"SPECTRUM-OV-001-1"}) == True

    assert is_downstream_submission_valid({"Downstream Submission":"Storage Only", "Storage Populations":"", "Patient ID":"SPECTRUM-OV-001"}) == False
    assert is_downstream_submission_valid({"Downstream Submission":"Storage Only", "Storage Populations":"abc", "Patient ID":"SPECTRUM-OV-001"}) == False
    assert is_downstream_submission_valid({"Downstream Submission":"Storage Only", "Storage Populations":"CD45P", "Patient ID":"SPECTRUM-OV-001"}) == False

def test_is_seq_info_valid():
    assert is_seq_info_valid({'Downstream Submission':"Sorted Single Cell Sequencing", "Patient ID":"SPECTRUM-OV-001"}) == True
    assert is_seq_info_valid({
    'Downstream Submission':"Storage Only",
    'Sorting Method':"",
    'Flow Instrument':"",
    'Flow Data Summary':"",
    'Flow Data fcs files':"",
    'Submitted Populations':"",
    'Sequencing Technique':"",
    'scRNA Date of Submission':"",
    'scRNA Sequencing Location':"",
    'Initial Submission QC':"",
    '# of Cells Captured':"",
    'scRNA IGO ID':"",
    'scRNA IGO Submission ID':"",
    'scRNA REX Sample ID':"",
    'scRNA Sample Status':"",
    'scRNA iLab Submission Form':"",
    'scRNA REX Submission Form':"",
    'QC Checks':"",
    'Patient ID': "SPECTRUM-OV-001"}) == True

    assert is_seq_info_valid({
        'Downstream Submission': "Storage Only",
        'Sorting Method': "Flow Sorting",
        'Flow Instrument': "",
        'Flow Data Summary': "",
        'Flow Data fcs files': "",
        'Submitted Populations': "",
        'Sequencing Technique': "",
        'scRNA Date of Submission': "",
        'scRNA Sequencing Location': "",
        'Initial Submission QC': "",
        '# of Cells Captured': "",
        'scRNA IGO ID': "",
        'scRNA IGO Submission ID': "",
        'scRNA REX Sample ID': "",
        'scRNA Sample Status': "",
        'scRNA iLab Submission Form': "",
        'scRNA REX Submission Form': "",
        'QC Checks': "",
        'Patient ID': "SPECTRUM-OV-001"}) == False

def test_is_submitted_populations_valid():
    assert is_submitted_populations_valid({"Submitted Populations": "CD45+", "Initial Submission QC":"Pass", "scRNA REX Sample ID":"001RA_CD45P", "Patient ID": "SPECTRUM-OV-001"}) == True
    assert is_submitted_populations_valid({"Submitted Populations": "CD45-", "Initial Submission QC":"Pass", "scRNA REX Sample ID":"001RA_CD45N", "Patient ID": "SPECTRUM-OV-001"}) == True

    assert is_submitted_populations_valid({"Submitted Populations": "CD45", "Patient ID": "SPECTRUM-OV-001"}) == False
    assert is_submitted_populations_valid({"Submitted Populations": "CD45+", "Initial Submission QC":"Pass", "scRNA REX Sample ID":"001RA_CD45N", "Patient ID": "SPECTRUM-OV-001"}) == False
    assert is_submitted_populations_valid({"Submitted Populations": "CD45-", "Initial Submission QC":"Pass", "scRNA REX Sample ID":"001RA_CD45P", "Patient ID": "SPECTRUM-OV-001"}) == False

def test_is_scrna_igo_id_valid():
    assert is_scrna_igo_id_valid({"scRNA IGO ID":"A"}) == True
    assert is_scrna_igo_id_valid({"scRNA IGO ID":"ZZ"}) == True

    assert is_scrna_igo_id_valid({"scRNA IGO ID":"AAA"}) == False
    assert is_scrna_igo_id_valid({"scRNA IGO ID":"1"}) == False
    assert is_scrna_igo_id_valid({"scRNA IGO ID":"12"}) == False
    assert is_scrna_igo_id_valid({"scRNA IGO ID":"123"}) == False

def test_is_scrna_igo_sub_id_valid():
    assert is_scrna_igo_sub_id_valid({"scRNA IGO Submission ID":"IGO-123456"}) == True

    assert is_scrna_igo_sub_id_valid({"scRNA IGO Submission ID":"IGO-1234567"}) == False
    assert is_scrna_igo_sub_id_valid({"scRNA IGO Submission ID":"IGO-12345"}) == False
    assert is_scrna_igo_sub_id_valid({"scRNA IGO Submission ID":"IGO-abcdef"}) == False
    assert is_scrna_igo_sub_id_valid({"scRNA IGO Submission ID":"IGO-123abc"}) == False
    assert is_scrna_igo_sub_id_valid({"scRNA IGO Submission ID":"1234567"}) == False
    assert is_scrna_igo_sub_id_valid({"scRNA IGO Submission ID":"IGO1234567"}) == False

def test_is_scrna_rex_id_valid():
    assert is_scrna_rex_id_valid({"scRNA REX ID":"001RA_CD45P"}) == True
    assert is_scrna_rex_id_valid({"scRNA REX ID":"001-1RA_CD45P"}) == True
    assert is_scrna_rex_id_valid({"scRNA REX ID":"001RA_CD45N"}) == True
    assert is_scrna_rex_id_valid({"scRNA REX ID":"001-1RA_CD45N"}) == True

    assert is_scrna_rex_id_valid({"scRNA REX ID":"001RA-CD45P"}) == False
    assert is_scrna_rex_id_valid({"scRNA REX ID":"12RA_CD45P"}) == False
    assert is_scrna_rex_id_valid({"scRNA REX ID":"001RA_CD45"}) == False
    assert is_scrna_rex_id_valid({"scRNA REX ID":"001Omentum_CD45P"}) == False
    assert is_scrna_rex_id_valid({"scRNA REX ID":"001RACD45P"}) == False

def test_is_qc_checks_valid():
    assert is_qc_checks_valid({"scRNA REX ID":"001RA_CD45P", "QC Checks":"Passed cDNA QC, Passed Library QC"}) == True
    assert is_qc_checks_valid({"scRNA REX ID":"001RA_CD45P", "QC Checks":"Failed cDNA QC"}) == True

    assert is_qc_checks_valid({"scRNA REX ID":"001RA_CD45P", "QC Checks":"Failed cDNA"}) == False
    assert is_qc_checks_valid({"scRNA REX ID":"001RA_CD45P", "QC Checks":""}) == False

def test_is_dlp_rex_id_valid():
    assert is_dlp_rex_id_valid({"DLP REX ID":"001RA_DLP"}) == True
    assert is_dlp_rex_id_valid({"DLP REX ID":"001-1RA_DLP"}) == True

    assert is_dlp_rex_id_valid({"DLP REX ID":"001RA_CD45P"}) == False
    assert is_dlp_rex_id_valid({"DLP REX ID":"001RA_T"}) == False
    assert is_dlp_rex_id_valid({"DLP REX ID":"001RA-DLP"}) == False

def test_is_wgs_tissue_type_valid():
    assert is_wgs_tissue_type_valid({"PPBC Downstream Submission":"WGS Bulk Tumour", "Tissue Type":"Frozen Tissue"}) == True

    assert is_wgs_tissue_type_valid({"PPBC Downstream Submission":"WGS Bulk Tumour", "Tissue Type":"FFPE Block"}) == False
    assert is_wgs_tissue_type_valid({"PPBC Downstream Submission":"WGS Bulk Tumour", "Tissue Type":"Single Cell Suspensions"}) == False

def test_is_ppbc_acc_num_valid():
    assert is_ppbc_acc_num_valid({"PPBC Accession #":"S19-12345"}) == True

    assert is_ppbc_acc_num_valid({"PPBC Accession #":"S19_12345"}) == False
    assert is_ppbc_acc_num_valid({"PPBC Accession #":"S19-1234"}) == False
    assert is_ppbc_acc_num_valid({"PPBC Accession #":"S19-123456"}) == False
    assert is_ppbc_acc_num_valid({"PPBC Accession #":"s19-12345"}) == False

def test_is_ppbc_bank_num_valid():
    assert is_ppbc_bank_num_valid({"PPBC Bank Number":"TS-12345"}) == True

    assert is_ppbc_bank_num_valid({"PPBC Bank Number":"AC-12345"}) == False
    assert is_ppbc_bank_num_valid({"PPBC Bank Number":"TS-1234"}) == False
    assert is_ppbc_bank_num_valid({"PPBC Bank Number":"TS-123456"}) == False
    assert is_ppbc_bank_num_valid({"PPBC Bank Number":"ts-12345"}) == False
    assert is_ppbc_bank_num_valid({"PPBC Bank Number":"TS_12345"}) == False

def test_is_wgs_igo_id_valid():
    assert is_wgs_igo_id_valid({"WGS IGO ID":"A"}) == True
    assert is_wgs_igo_id_valid({"WGS IGO ID":"ZZ"}) == True

    assert is_wgs_igo_id_valid({"WGS IGO ID":"AAA"}) == False
    assert is_wgs_igo_id_valid({"WGS IGO ID":"1"}) == False
    assert is_wgs_igo_id_valid({"WGS IGO ID":"12"}) == False
    assert is_wgs_igo_id_valid({"WGS IGO ID":"123"}) == False

def test_is_wgs_igo_submission_id_valid():
    assert is_wgs_igo_submission_id_valid({"WGS IGO Submission ID":"IGO-123456"}) == True

    assert is_wgs_igo_submission_id_valid({"WGS IGO Submission ID":"IGO-1234567"}) == False
    assert is_wgs_igo_submission_id_valid({"WGS IGO Submission ID":"IGO-12345"}) == False
    assert is_wgs_igo_submission_id_valid({"WGS IGO Submission ID":"IGO-abcdef"}) == False
    assert is_wgs_igo_submission_id_valid({"WGS IGO Submission ID":"IGO-123abc"}) == False
    assert is_wgs_igo_submission_id_valid({"WGS IGO Submission ID":"1234567"}) == False
    assert is_wgs_igo_submission_id_valid({"WGS IGO Submission ID":"IGO1234567"}) == False

def test_is_wgs_rex_id_valid():
    assert is_wgs_rex_id_valid({"WGS REX ID":"001RA_T"}) == True
    assert is_wgs_rex_id_valid({"WGS REX ID":"001-1RA_T"}) == True

    assert is_wgs_rex_id_valid({"WGS REX ID":"001RA_CD45P"}) == False
    assert is_wgs_rex_id_valid({"WGS REX ID":"001RA_DLP"}) == False
    assert is_wgs_rex_id_valid({"WGS REX ID":"001RA-T"}) == False

def test_is_if_tissue_type_valid():
    assert is_if_tissue_type_valid({"PPBC Downstream Submission":"IF", "Tissue Type":"FFPE Block"}) == True

    assert is_if_tissue_type_valid({"PPBC Downstream Submission":"IF", "Tissue Type":"Frozen Tissue"}) == False
    assert is_if_tissue_type_valid({"PPBC Downstream Submission":"IF", "Tissue Type":"Single Cell Suspensions"}) == False