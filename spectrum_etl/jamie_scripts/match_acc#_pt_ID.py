import pandas as pd
import os

# matches accession numbers to Spectrum Patient ID
def match_acc_num_pt_id(file_name, file_name2, saved_filename):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    file_spec_id = os.path.join(fileDir, "Sample Collection/PPBC requests/Pathology request"+file_name)
    file_OR_collection = os.path.join(fileDir, "Sample Collection/"+file_name2)

    spec_id = pd.read_excel(file_spec_id)

    OR_record = pd.read_excel(file_OR_collection, usecols=["MRN", "Spectrum-OV", "Excluded", "Accession #"])

    OR_record['Spectrum-OV'] = 'SPECTRUM-OV-' + OR_record['Spectrum-OV'].astype(str)

    spec_id_with_acc = pd.merge(spec_id, OR_record,
                                     on=['Spectrum-OV'], how='left')

    spec_id_with_acc = spec_id_with_acc[["Spectrum-OV", "Accession #", "Site", "MRN", "Excluded"]]

    print(spec_id_with_acc)
    spec_id_with_acc.to_csv('Sample Collection/PPBC requests/Pathology request'+saved_filename, index=False)

match_acc_num_pt_id('Diag_FFPE_request_Jul29.xlsx', 'Spectrum Patient OR Collection Record.xlsx', 'Diag_FFPE_request_Jul29.csv')