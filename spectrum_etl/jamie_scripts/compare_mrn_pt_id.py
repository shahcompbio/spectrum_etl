import pandas as pd
import os
import xlrd
import datetime
import math
import numpy as np

# match PPBC (FFPE/Frozen) reports to Spectrum Patient ID, using OR collection record, and prints in elab spreadsheet entry column format
def match_ppbc_mrn_to_pt_id(file_name, file_name2, saved_filename):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    file_ppbc = os.path.join(fileDir, "PPBC/"+file_name)
    file_mrn = os.path.join(fileDir, "/Volumes/GynLab/Weigelt Lab/Jamie/wet_lab/SPECTRUM/"+file_name2)

    ppbc_collection = pd.read_excel(file_ppbc)
    OR_record = pd.read_excel(file_mrn, usecols=["Project", "MRN", "Patient ID", "Surgery Date", "Surgery Type", "Attending", "Surgery Location", "Room", "Final Path", "Study Protocol", "Excluded"])

    OR_record['Patient ID'] = 'SPECTRUM-OV-' + OR_record['Patient ID'].astype(str)
    ppbc_collection.rename(columns={'OR Date':'Surgery Date'}, inplace=True)

    ppbc_collection['Surgery Date'] = ppbc_collection['Surgery Date'].dt.date
    OR_record['Surgery Date'] = OR_record['Surgery Date'].apply(lambda x: x.date() if isinstance(x, datetime.datetime) else x)

    ppbc_collection["PPBC Aliquot Number"] = ppbc_collection["Aliquot Number"].apply(lambda x: str(int(x)) if not math.isnan(x) else x) + ppbc_collection["Specimen Category"]

    ppbc_collected = pd.merge(ppbc_collection, OR_record,
                                     on=['MRN', 'Surgery Date'], how='left')

    ppbc_collected.drop(['Patient Name', 'Part - Sub Part', 'Time Lapse'], axis=1, inplace=True)
    ppbc_collected['Specimen Unit'] = ppbc_collected['Specimen Unit'].replace(['Nunc (Cryovial)'], 'Frozen Tissue')
    ppbc_collected['Specimen Unit'] = ppbc_collected['Specimen Unit'].replace(['Cryomold'], 'Frozen Tissue')
    ppbc_collected['Specimen Unit'] = ppbc_collected['Specimen Unit'].replace(['Paraffin Block'], 'FFPE Block')

    ppbc_collected["PPBC Downstream Submission"] = "Storage Only"
    ppbc_collected["Specify Diagnosis"] = ""

    path_list = ['Benign',
                 'Carcinosarcoma',
                 'Clear Cell Carcinoma',
                 'HGSC',
                 'HGSC/G3 Endometrioid',
                 'LGSC',
                 'Mucinous Adenocarcinoma',
                 'Mucinous Carcinoma',
                 'SCCOHT']

    for index, row in ppbc_collected.iterrows():
        temp = row['Final Path']
        if temp not in path_list:
            ppbc_collected.at[index, 'Specify Diagnosis'] = row['Final Path']
            ppbc_collected.at[index, "Final Path"] = "Other"

    ppbc_collected = ppbc_collected[["Project", "Patient ID", "MRN", "Surgery Type", "Surgery Date", "Attending", "Surgery Location", "Room", "Study Protocol", "Excluded", "Final Path", "Specify Diagnosis", "Specimen Unit", "Bank Number", "PPBC Aliquot Number", "Accession Number", "PPBC Downstream Submission", "Site and Laterality", "Specimen Category", "Aliquot Number"]]

    ppbc_collected.to_csv("PPBC/"+saved_filename, index=False)

# matches IMF blood spreadsheet to Spectrum Patient ID and prints in elab spreadsheet entry column format
# 1. sort IMF spreadsheet by date, drag tab 3 so that it becomes tab 1 in excel. remove spaces from (x106) header
def match_IMF_mrn_to_pt_id(file_name, file_name2, saved_filename):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    file_imf = os.path.join(fileDir, "./Sample Collection/IMF/"+file_name)
    file_mrn = os.path.join(fileDir, "/Volumes/GynLab/Weigelt Lab/Jamie/wet_lab/SPECTRUM/"+file_name2)

    imf_collection = pd.read_excel(file_imf)
    #imf_collection["MRN"] = imf_collection["MRN"].convert_objects(convert_numeric=True)

    OR_record = pd.read_excel(file_mrn, usecols=["MRN", "Spectrum-OV", "Study Protocol", "Excluded"])

    OR_record['Spectrum-OV'] = 'SPECTRUM-OV-' + OR_record['Spectrum-OV'].astype(str)

    imf_collected = pd.merge(imf_collection, OR_record,
                                     on=['MRN'], how='left')

    imf_collected.rename(columns={'Current # of vials':'vials'}, inplace=True)
    imf_collected['# of vials stored'] = imf_collected.vials.str.split(' ').str[0]
    imf_collected.drop(['Patient Initials', '#Cells/ Vial (x 106)', 'Box ID in LN2-1', 'Position in Box'], axis=1, inplace=True)

    imf_collected = imf_collected[["Spectrum-OV", "MRN", "Study Protocol", "Excluded", "IMF Clinical Trial Sample ID", "Freeze date", "# of vials stored"]]

    imf_collected.to_csv('Sample Collection/IMF/'+saved_filename, index=False)

match_ppbc_mrn_to_pt_id('15-200 Samples Collected until 1-26-21 with OCT Aliq.xlsx', 'Spectrum Patient OR Collection Record.xlsx', 'PPBC Collection_frozen_Jan2021.csv')
#match_IMF_mrn_to_pt_id('15-200 Study Samples - 20210127.xlsx', 'Spectrum Patient OR Collection Record.xlsx', 'IMF 15-200 Samples collected - toJan25.csv')
