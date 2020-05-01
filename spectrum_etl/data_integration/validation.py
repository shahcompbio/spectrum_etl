'''
Created on March 27, 2020

@author: limj@mskcc.org
'''
import sys
import re

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
    if patient_id != re.compile(r"\b\d{3}[A-Z]{2,3}_CD45[P|N]\b"):
        print("Please ensure patient ID (%s) is in proper format." % patient_id)
        sys.exit(1)

# validate MRN from elab data
def is_mrn_valid(mrn, patient_id):
    if mrn == NULL or mrn != re.compile(r"\b\d{8}\b"):
        print("Please add/edit the MRN for %s." % patient_id)
        sys.exit(1)

# validate excluded status, ensure exclusion details and diagnosis are valid, if necessary, from elab data
def is_patient_excluded(excluded, patient_id, final_pathology, specify_diagnosis, reason_for_exclusion):
    if excluded == "No":
        if final_pathology != re.compile(r"HGSC"):
        print("Please ensure final pathology of %s is HGSC." % patient_id)
    else:
        if final_pathology == "NULL" or reason_for_exclusion == "NULL":
            print("Please input final pathology and/or reason for exclusion for %s." % patient_id)
            sys.exit(1)

    if final_pathology == "Other":
        if specify_diagnosis == NULL:
            print("Please input diagnosis for %s." % patient_id)
            sys.exit(1)

# validate specimen site, ensure site details are valid, if necessary, from elab data
def is_specimen_site_valid(specimen_site, patient_id, site_details):
    if specimen_site == NULL:
        print("Please add a specimen site for %s." % patient_id)
    else:
        if specimen_site not in validate_specimen_sites:
            print("%s is not a site that was collected in our study." % specimen_site)
            sys.exit(1)

    if specimen_site == "Other":
        if site_details == NULL:
            print("Please input site details for %s." % patient_id)
            sys.exit(1)

# validate downstream submission field if sample is stored
def is_downstream_submission_valid(downstream_submission, patient_id):
    if downstream_submission == "Storage Only":
        for seq_info in validate_sequencing_info:
            if seq_info != "NULL":
                print("Please remove all sorting and sequencing info from %s." % patient_id)
        if storage_populations == "NULL":
            print("Please indicate storage populations as CD45+, CD45-, or unsorted for %s." % patient_id)
            sys.exit(1)

# validate submitted populations, initial submission QC and REX Sample ID
def is_submitted_populations_valid(submitted_populations, patient_id):
    if submitted_populations != "CD45+" and submitted_populations != "CD45-":
        print("Please input submitted populations for %s." % patient_id)
    else:
        if initial_submission_QC == "Pass" and submitted_populations == "CD45+":
            if scRNA_rex_sample_id != re.compile(r"CD45P"):
                print("Please edit scRNA REX Sample ID (%s) to match submitted population." % scrna_rex_sample_id)
        elif initial_submission_QC == "Pass" and submitted_populations == "CD45-":
            if scRNA_rex_sample_id != re.compile(r"CD45N"):
                print("Please edit scRNA REX Sample ID (%s) to match submitted population." % scRNA_rex_sample_id)
                sys.exit(1)

# validate scRNA IGO ID
def is_scRNA_IGO_ID_valid(scrna_igo_id, patient_id):
    if scrna_igo_id != re.compile(r"\b[A-Z]{1,2}\b"):
        print("Please ensure scRNA IGO ID is in proper format for %s." % patient_id)
        sys.exit(1)

# validate scRNA IGO Submission ID
def is_scRNA_IGO_Submission_ID_valid(scrna_igo_sub_id, patient_id):
    if scrna_igo_sub_id != re.compile(r"\bIGO-\d{6}\b"):
        print("Please ensure scRNA IGO Submission ID is in proper format for %s." % patient_id)
        sys.exit(1)

# validate scRNA REX ID
def is_scRNA_REX_ID(scrna_rex_id, patient_id, qc_checks):
    if scrna_rex_id != re.compile(r"\b\d{3}[A-Z]{2,3}_CD45[P|N]\b"):
        print("Please ensure scRNA REX ID is in proper format for %s." % patient_id)
        sys.exit(1)

    if scrna_rex_id != "NULL" and qc_checks == "NULL":
        print("Please ensure input for QC Checks are valid for %s." % patient_id)
        sys.exit(1)