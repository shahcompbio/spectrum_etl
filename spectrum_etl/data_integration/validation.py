'''
Created on March 27, 2020

@author: limj@mskcc.org
'''
import sys
import re

import logging
logger = logging.getLogger()

validate_specimen_sites = ['Ascites',
         'Bowel',
         'Infracolic Omentum',
         'Left Adnexa',
         'Left Upper Quadrant',
         'Other',
         'Pelvic Peritoneum',
         'Right Adnexa',
         'Right Upper Quadrant']

validate_sequencing_info = ['Sorting Method',
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

# validate patient id from elab data
def is_pt_id_valid(patient_id):
    pattern = re.compile("^SPECTRUM-OV-\d{3}(-\d+)?$")

    if pattern.match(patient_id):
        return True
    return False

# validate MRN from elab data
def is_mrn_valid(mrn):
    pattern = re.compile(r"^\d{8}$")

    if pattern.match(mrn):
        return True
    return False

# validate surgery ID number to match with patient ID
def is_surgery_id_valid(surgery_id, patient_id):
    pattern = re.compile(r"^SPECTRUM-OV-\d{3}-\d+$")
    pattern2 = re.compile(r"^SPECTRUM-OV-\d{3}$")

    returnVal = True
    if pattern.match(patient_id):
        if surgery_id != patient_id.split("-")[3]:
            returnVal = False
    elif pattern2.match(patient_id):
        if surgery_id != "0":
            returnVal = False
    else:
        returnVal = False

    if returnVal is True:
        return True
    return False

# validate excluded status, ensure exclusion details and diagnosis are valid, if necessary, from elab data
def is_patient_excluded(excluded, final_pathology, specify_diagnosis, reason_for_exclusion, patient_id):
    pattern = re.compile(r"HGSC")

    returnVal = True
    if excluded == "No":
        if not pattern.match(final_pathology):
            returnVal = False
            if returnVal is False:
                logger.error("Please ensure final pathology of %s is HGSC." % patient_id)
    else:
        if final_pathology == "" or reason_for_exclusion == "":
            returnVal = False
            if returnVal is False:
                logger.error("Please input final pathology and/or reason for exclusion for %s." % patient_id)
        elif final_pathology == "Other" and specify_diagnosis == "":
            returnVal = False
            if returnVal is False:
                logger.error("Please input diagnosis for %s." % patient_id)

    if returnVal is True:
        return True
    return False

# validate specimen site, ensure site details are valid, if necessary, from elab data
def is_specimen_site_valid(specimen_site, patient_id, site_details):

    returnVal = True
    if specimen_site == "":
        returnVal = False
        logger.error("Please add a specimen site for %s." % patient_id)
    elif specimen_site not in validate_specimen_sites:
        returnVal = False
        logger.error("%s is not a site that was collected in our study." % specimen_site)
    elif specimen_site == "Other" and site_details == "":
        returnVal = False
        logger.error("Please input site details for %s." % patient_id)
    else:
        pass

    if returnVal is True:
        return True
    return False

# validate downstream submission field if sample is stored
def is_downstream_submission_valid(downstream_submission, patient_id):
    if downstream_submission == "Storage Only":
        for seq_info in validate_sequencing_info:
            if seq_info != "":
                print("Please remove all sorting and sequencing info from %s." % patient_id)
        # if storage_populations == "":
        #     print("Please indicate storage populations as CD45+, CD45-, or unsorted for %s." % patient_id)
            sys.exit(1)

# validate submitted populations, initial submission QC and REX Sample ID
def is_submitted_populations_valid(submitted_populations, patient_id):
    if submitted_populations != "CD45+" and submitted_populations != "CD45-":
        print("Please input submitted populations for %s." % patient_id)
    else:
        # if initial_submission_QC == "Pass" and submitted_populations == "CD45+":
        #     if scRNA_rex_sample_id != re.compile(r"CD45P"):
        #         print("Please edit scRNA REX Sample ID (%s) to match submitted population." % scrna_rex_sample_id)
        # elif initial_submission_QC == "Pass" and submitted_populations == "CD45-":
        #     if scRNA_rex_sample_id != re.compile(r"CD45N"):
        #         print("Please edit scRNA REX Sample ID (%s) to match submitted population." % scRNA_rex_sample_id)
                sys.exit(1)

# validate scRNA IGO ID
def is_scrna_igo_id_valid(scrna_igo_id):
    pattern = re.compile(r"^[A-Z]{1,2}$")

    if pattern.match(scrna_igo_id):
        return True
    return False

# validate scRNA IGO Submission ID
def is_scrna_igo_sub_id_valid(scrna_igo_sub_id):
    pattern = re.compile(r"^IGO-\d{6}$")

    if pattern.match(scrna_igo_sub_id):
        return True
    return False
        #print("Please ensure scRNA IGO Submission ID is in proper format for %s." % patient_id)
        #sys.exit(1)

# validate scRNA REX ID
def is_scRNA_REX_ID_valid(scrna_rex_id, patient_id, qc_checks):
    pattern = re.compile(r"^\d{3}(-\d+)?[A-Z]{2,3}_CD45[P|N]$")

    if pattern.match(scrna_rex_id):
        return True
    return False
        #print("Please ensure scRNA REX ID is in proper format for %s." % patient_id)
        #sys.exit(1)

# validate QC Checks with scRNA REX ID
def is_QC_checks_valid(qc_checks):
    if scrna_rex_id != None and qc_checks == None:
        return False
    return True
        #print("Please ensure input for QC Checks are valid for %s." % patient_id)
        #sys.exit(1)

# validate DLP REX ID
def is_DLP_REX_ID(dlp_rex_id, patient_id):
    pattern = re.compile(r"^\d{3}[A-Z]{2,3}_DLP$")

    if pattern.match(dlp_rex_id):
        return True
    return False
        #print("Please ensure DLP REX ID is in proper format for %s." % patient_id)
        #sys.exit(1)

# validate tissue type for WGS bulk tumour
def is_WGS_tissue_type_valid(tissue_type, patient_id):
    if tissue_type == "Frozen Tissue":
        return True
    return False
        #print("Please ensure WGS bulk tumour tissue type is accurate for %s." % patient_id)
        #sys.exit(1)

# validate PPBC accession # for frozen/FFPE
def is_PPBC_acc_num_valid(ppbc_acc_num, patient_id):
    pattern = re.compile(r"^S\d{2}-\d{5}$")

    if pattern.match(ppbc_acc_num):
        return True
    return False
        #print("Please ensure PPBC accession number is in proper format for %s." % patient_id)
        #sys.exit(1)

# validate PPBC bank # for frozen/FFPE
def is_ppbc_bank_num_valid(ppbc_bank_num, patient_id):
    pattern = re.compile(r"^TS-\d{5}$")

    if pattern.match(ppbc_bank_num):
        return True
    return False
        #print("Please ensure PPBC bank number is in proper format for %s." % patient_id)
        #sys.exit(1)

# validate WGS IGO ID
def is_WGS_IGO_ID_valid(wgs_igo_id, patient_id):
    pattern = re.compile(r"^[A-Z]{1,2}$")

    if pattern.match(wgs_igo_id):
        return True
    return False
        #print("Please ensure WGS IGO ID is in proper format for %s." % patient_id)
        #sys.exit(1)

# validate WGS IGO Submission ID
def is_WGS_IGO_Submission_ID_valid(wgs_igo_sub_id, patient_id):
    pattern = re.compile(r"^IGO-\d{6}$")

    if pattern.match(wgs_igo_sub_id):
        return True
    return False
        #print("Please ensure WGS IGO Submission ID is in proper format for %s." % patient_id)
        #sys.exit(1)

# validate WGS REX ID
def is_WGS_REX_ID(wgs_rex_id, patient_id):
    pattern = re.compile(r"^\d{3}[A-Z]{2,3}_T$")

    if pattern.match(wgs_rex_id):
        return True
    return False
        #print("Please ensure WGS REX ID is in proper format for %s." % patient_id)
        #sys.exit(1)

# validate tissue type for IF
def is_IF_tissue_type_valid(tissue_type, patient_id):
    if tissue_type == "FFPE Block":
        return True
    return False
        #print("Please ensure IF tissue type is accurate for %s." % patient_id)
        #sys.exit(1)