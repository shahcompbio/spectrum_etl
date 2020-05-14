'''
Created on March 27, 2020

@author: limj@mskcc.org
'''
import sys
import re

import logging
logger = logging.getLogger()

validate_specimen_site = [
    'Ascites',
    'Bowel',
    'Infracolic Omentum',
    'Left Adnexa',
    'Left Upper Quadrant',
    'Other',
    'Pelvic Peritoneum',
    'Right Adnexa',
    'Right Upper Quadrant']

seq_info_headers = [
    'Sorting Method',
    'Flow Instrument',
    'Flow Data Summary',
    'Flow Data fcs files',
    'Submitted Populations',
    'Sequencing Technique',
    'scRNA Date of Submission',
    'scRNA Sequencing Location',
    'Initial Submission QC',
    '# of Cells Captured',
    'scRNA IGO ID',
    'scRNA IGO Submission ID',
    'scRNA REX Sample ID',
    'scRNA Sample Status',
    'scRNA iLab Submission Form',
    'scRNA REX Submission Form',
    'QC Checks']

validate_qc_check = [
    'Passed cDNA QC, Failed Library QC',
    'Passed cDNA QC, Passed Library QC',
    'Failed cDNA QC']

# validate patient id from elab data
def is_pt_id_valid(row):
    pattern = re.compile("^SPECTRUM-OV-\d{3}(-\d+)?$")

    if pattern.match(row["Patient ID"]):
        return True
    return False

# validate MRN from elab data
def is_mrn_valid(row):
    pattern = re.compile(r"^\d{8}$")

    if pattern.match(row["MRN"]):
        return True
    return False

# validate surgery ID number to match with patient ID
def is_surgery_id_valid(row):
    patternPre = re.compile(r"^SPECTRUM-OV-\d{3}$")
    patternPost = re.compile(r"^SPECTRUM-OV-\d{3}-\d+$")

    if patternPre.match(row["Patient ID"]):
        if row["Surgery ID"] == "0":
            return True
    elif patternPost.match(row["Patient ID"]):
        if row["Surgery ID"] == row["Patient ID"].split("-")[3]:
            return True
    return False

# validate excluded status, ensure exclusion details and diagnosis are valid, if necessary, from elab data
def is_patient_excluded(row):
    pattern = re.compile(r"^.*HGSC.*$")

    if row["Excluded"] == "No":
        if not pattern.match(row["Final Pathology"]):
            logger.error("Please ensure final pathology of %s is HGSC." % row["Patient ID"])
            return False
    else:
        if row["Final Pathology"] == "" or row["Reason for Exclusion"] == "":
            logger.error("Please input final pathology and/or reason for exclusion for %s." % row["Patient ID"])
            return False
        elif row["Final Pathology"] == "Other" and row["Specify Diagnosis"] == "":
            logger.error("Please input diagnosis for %s." % row["Patient ID"])
            return False
    return True

# validate specimen site, ensure site details are valid, if necessary, from elab data
def is_specimen_site_valid(row):

    if row["Specimen Site"] == "":
        logger.error("Please add a specimen site for %s." % row["Patient ID"])
        return False
    elif row["Specimen Site"] not in validate_specimen_site:
        logger.error("%s is not a site that was collected in our study." % row["Specimen Site"])
        return False
    elif row["Specimen Site"] == "Other" and row["Site Details"] == "":
        logger.error("Please input site details for %s." % row["Patient ID"])
        return False
    else:
        return True

# validate downstream submission field if sample is stored
def is_downstream_submission_valid(row):
    if row["Downstream Submission"] == "Storage Only":
        if row["Storage Populations"] == "CD45+" or row["Storage Populations"] == "CD45-" or row["Storage Populations"] == "Unsorted":
             return True
        else:
             logger.error("Please indicate storage populations as CD45+, CD45-, or Unsorted for %s." % row["Patient ID"])
             return False

# validate to ensure that all scRNA fields are blank for storage only samples
def is_seq_info_valid(row):
    if row["Downstream Submission"] == "Storage Only":
        for seq_info in seq_info_headers:
            if row[seq_info] != "":
                logger.error("Please remove all sorting and sequencing info from %s." % row["Patient ID"])
                return False
            return True
    return True

# validate submitted populations, initial submission QC and REX Sample ID
def is_submitted_populations_valid(row):
    pattern = re.compile(r"^.*CD45P$")
    pattern2 = re.compile(r"^.*CD45N$")

    if row["Submitted Populations"] == "CD45+":
        if row["Initial Submission QC"] == "Pass" and not pattern.match(row["scRNA REX Sample ID"]):
            logger.error("Please edit scRNA REX Sample ID (%s) to match submitted population (%s)." % (
                row["scRNA REX Sample ID"], row["Submitted Populations"]))
            return False
    elif row["Submitted Populations"] == "CD45-":
        if row["Initial Submission QC"] == "Pass" and not pattern2.match(row["scRNA REX Sample ID"]):
            logger.error("Please edit scRNA REX Sample ID (%s) to match submitted population (%s)." % (
                row["scRNA REX Sample ID"], row["Submitted Populations"]))
            return False
    else:
        logger.error("Please input submitted populations for %s." % row["Patient ID"])
        return False
    return True

# validate scRNA IGO ID
def is_scrna_igo_id_valid(row):
    pattern = re.compile(r"^[A-Z]{1,2}$")

    if pattern.match(row["scRNA IGO ID"]):
        return True
    return False

# validate scRNA IGO Submission ID
def is_scrna_igo_sub_id_valid(row):
    pattern = re.compile(r"^IGO-\d{6}$")

    if pattern.match(row["scRNA IGO Submission ID"]):
        return True
    return False

# validate scRNA REX ID
def is_scrna_rex_id_valid(row):
    pattern = re.compile(r"^\d{3}(-\d+)?[A-Z]{2,3}_CD45[P|N]$")

    if pattern.match(row["scRNA REX ID"]):
        return True
    return False

# validate QC Checks with scRNA REX ID
def is_qc_checks_valid(row):
    if (row["scRNA REX ID"] != "") and (row["QC Checks"] in validate_qc_check):
        return True
    return False

# validate DLP REX ID
def is_dlp_rex_id_valid(row):
    pattern = re.compile(r"^\d{3}(-\d+)?[A-Z]{2,3}_DLP$")

    if pattern.match(row["DLP REX ID"]):
        return True
    return False

# validate tissue type for WGS bulk tumour
def is_wgs_tissue_type_valid(row):
    if row["PPBC Downstream Submission"] == "WGS Bulk Tumour" and row["Tissue Type"] == "Frozen Tissue":
        return True
    return False

# validate PPBC accession # for frozen/FFPE
def is_ppbc_acc_num_valid(row):
    pattern = re.compile(r"^S\d{2}-\d{5}$")

    if pattern.match(row["PPBC Accession #"]):
        return True
    return False

# validate PPBC bank # for frozen/FFPE
def is_ppbc_bank_num_valid(row):
    pattern = re.compile(r"^TS-\d{5}$")

    if pattern.match(row["PPBC Bank Number"]):
        return True
    return False

# validate WGS IGO ID
def is_wgs_igo_id_valid(row):
    pattern = re.compile(r"^[A-Z]{1,2}$")

    if pattern.match(row["WGS IGO ID"]):
        return True
    return False

# validate WGS IGO Submission ID
def is_wgs_igo_submission_id_valid(row):
    pattern = re.compile(r"^IGO-\d{6}$")

    if pattern.match(row["WGS IGO Submission ID"]):
        return True
    return False

# validate WGS REX ID
def is_wgs_rex_id_valid(row):
    pattern = re.compile(r"^\d{3}(-\d+)?[A-Z]{2,3}_T$")

    if pattern.match(row["WGS REX ID"]):
        return True
    return False

# validate tissue type for IF
def is_if_tissue_type_valid(row):
    if row["PPBC Downstream Submission"] == "IF" and row["Tissue Type"] == "FFPE Block":
        return True
    return False