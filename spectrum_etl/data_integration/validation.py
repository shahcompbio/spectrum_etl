'''
Created on March 27, 2020

@author: limj@mskcc.org
'''

pt_id = ['SPECTRUM-OV-001',
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

sites = ['Ascites',
         'Bowel',
         'Infracolic Omentum',
         'Left Adnexa',
         'Left Upper Quadrant',
         'Other',
         'Pelvic Peritoneum',
         'Right Adnexa',
         'Right Upper Quadrant']

class is_pt_id_valid():
    if pt_id is None: return False

    for id in range(len(pt_id)):
        if pt_id[id] == pt_id:
            return True

    return False

class is_specimen_site_valid():
    if specimen_site is None: return False

    for site in range(len(specimen_site)):
        if specimen_site[site] == specimen_site:
            return True

    return False


