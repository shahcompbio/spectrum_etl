'''
Created on March 27, 2020

@author: limj@mskcc.org
'''
import sys

validate_pt_id = ['SPECTRUM-OV-001',
         'SPECTRUM-OV-002',
         'SPECTRUM-OV-003',
         'SPECTRUM-OV-004',
         'SPECTRUM-OV-005',
         'SPECTRUM-OV-006',
         'SPECTRUM-OV-007',
         'SPECTRUM-OV-008',
         'SPECTRUM-OV-009',
         'SPECTRUM-OV-010',
         'SPECTRUM-OV-011',
         'SPECTRUM-OV-012',
         'SPECTRUM-OV-013',
         'SPECTRUM-OV-014',
         'SPECTRUM-OV-015',
         'SPECTRUM-OV-016',
         'SPECTRUM-OV-017',
         'SPECTRUM-OV-018',
         'SPECTRUM-OV-019',
         'SPECTRUM-OV-020',]

validate_specimen_sites = ['Ascites',
         'Bowel',
         'Infracolic Omentum',
         'Left Adnexa',
         'Left Upper Quadrant',
         'Other',
         'Pelvic Peritoneum',
         'Right Adnexa',
         'Right Upper Quadrant']

# validate patient id from elab data frame
def is_pt_id_valid(patient_id):
    if patient_id not in validate_pt_id:
        print("There is no metadata available for %s." % patient_id)
        sys.exit(1)

# validate specimen site from elab data frame
def is_specimen_site_valid(specimen_site):
    if specimen_site not in validate_specimen_sites:
        print("%s is not a site that was collected in our study." % specimen_site)
        sys.exit(1)