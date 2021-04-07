import pandas as pd
import os
from elab_queries import import_elab_pull

# sort columns in elab queries for PPBC blocks/frozens or DLP (edit line 9 & 11)
# edit sorted_filename - eLab_<storage/PPBC>_samples.csv
def sort_columns_PPBC(pull_filename, sorted_filename):

    elab_pull = import_elab_pull(pull_filename)
    #DLP elab_pull = elab_pull.loc[elab_pull['Excluded'] == "No"]
    elab_pull = elab_pull.loc[elab_pull['Tissue Type'] == "FFPE Block"]
    #DLP elab_pull = elab_pull.loc[elab_pull['Downstream Submission'] == "Storage Only"]
    elab_pull = elab_pull[["Project", "Patient ID", "MRN", "Surgery #", "Surgery Type", "Surgery Date", "Surgeon", "Surgery Location", "Room", "Study Protocol", "Excluded", "Final Pathology", "Processing Date", "Specimen Site", "Primary Site", "Tissue Type", "PPBC Bank #", "PPBC Aliquot #", "PPBC Accession #"]]
    #DLP elab_pull = elab_pull[
    #     ["Project", "Patient ID", "MRN", "Surgery Type", "Surgery Date", "Surgeon", "Surgery Location", "Room",
    #      "Study Protocol", "Excluded", "Final Pathology", "Processing Date", "Specimen Site", "Site Details",
    #      "Primary Site", "Tissue Type", "Preservation Method", "Total Cell Count (cells/ml)", "Live Cell Count (cells/ml)",
    #      "Total Volume (ml)", "Viability (%)", "Downstream Submission",	"Storage Populations",	"Storage Facility",
    #      "IGO Storage ID",	"IGO Sample ID"]]

    #print(elab_pull)
    elab_pull.to_csv(sorted_filename, index=False)

# compare sorted columns sheet to submitted FFPE samples for mpIF/IF and WGS-T (PPBC) and DLP
# submitted spreadsheet format (Patient ID, Specimen Site, Nomenclature)
def compare_sorted_to_submitted_PPBC(sorted_filename, submitted_filename, saved_filename):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    submitted_doc = os.path.join(fileDir, "/Volumes/GynLab/Weigelt Lab/Jamie/wet_lab/SPECTRUM/" + submitted_filename)

    sorted_file = pd.read_csv(sorted_filename)
    submitted_file = pd.read_excel(submitted_doc)

    merged_files = pd.merge(submitted_file, sorted_file,
                                on=['Patient ID', 'Specimen Site'], how='left')

    merged_files = merged_files[["Project", "Patient ID", "MRN", "Surgery Type", "Surgery Date", "Surgeon", "Surgery Location", "Room", "Study Protocol", "Excluded", "Final Pathology", "Processing Date", "Specimen Site", "Site Details", "Primary Site", "Tissue Type", "PPBC Bank #", "PPBC Aliquot #", "PPBC Accession #", "Nomenclature"]]

    #DLP merged_files = merged_files[
    #     ["Patient ID", "MRN", "Surgery Type", "Surgery Date", "Surgeon", "Surgery Location", "Room",
    #      "Study Protocol", "Excluded", "Final Pathology", "Processing Date", "Specimen Site", "Site Details",
    #      "Primary Site", "Tissue Type", "Preservation Method", "Total Cell Count (cells/ml)",
    #      "Live Cell Count (cells/ml)", "Total Volume (ml)", "Viability (%)", "Downstream Submission",
    #      "Storage Facility", "IGO Storage ID", "IGO Sample ID"]]

    merged_files = merged_files.drop_duplicates()
    #print(merged_files)
    saved_file = os.path.join(fileDir, "/Volumes/GynLab/Weigelt Lab/Jamie/wet_lab/SPECTRUM/Sample Submissions and Data/mpIF-IF/" + saved_filename)
    merged_files.to_csv(saved_file, index=False)

# compare sorted columns sheet to submitted FFPE samples for mpIF/IF (Diagnostic)
# 1. pull reference_file query from elab (Excluded=No)
# 2. remove duplicates from reference_file (Col U, AD), save as xlsx
def compare_sorted_to_submitted_diag(reference_filename, submitted_filename, saved_filename):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    submitted_doc = os.path.join(fileDir, "/Volumes/GynLab/Weigelt Lab/Jamie/wet_lab/SPECTRUM/" + submitted_filename)

    reference_file = pd.read_excel(reference_filename)
    submitted_file = pd.read_excel(submitted_doc)

    reference_file = reference_file.loc[reference_file['Excluded'] == "No"]
    reference_file = reference_file.loc[reference_file['Tissue Type'] == "Single Cell Suspension"]

    reference_file = reference_file[
        ["Project", "Patient ID", "MRN", "Surgery Type", "Surgery Date", "Surgeon", "Surgery Location", "Room",
         "Study Protocol", "Excluded", "Final Pathology", "Processing Date", "Specimen Site", "Primary Site",
         "Tissue Type", "PPBC Bank #", "PPBC Aliquot #", "PPBC Accession #"]]

    merged_files = pd.merge(submitted_file, reference_file,
                                on=['Patient ID', "Specimen Site"], how='left')

    merged_files = merged_files[["Project", "Patient ID", "MRN", "Surgery Type", "Surgery Date", "Surgeon", "Surgery Location", "Room", "Study Protocol", "Excluded", "Final Pathology", "Processing Date", "Specimen Site", "Site Details", "Primary Site", "Tissue Type", "PPBC Bank #", "PPBC Aliquot #", "PPBC Accession #", "Case Accession #", "Block ID", "Matched Site", "Nomenclature"]]

    merged_files_nodup = merged_files.drop_duplicates()
    #print(merged_files)
    saved_file = os.path.join(fileDir,
                              "/Volumes/GynLab/Weigelt Lab/Jamie/wet_lab/SPECTRUM/Sample Submissions and Data/mpIF-IF/" + saved_filename)
    merged_files_nodup.to_csv(saved_file, index=False)

sort_columns_PPBC("~/Desktop/MSKCC/ARCHIVE_SPECTRUM/Database Management/ELAB PULL/elabpull wMRN_031021.xlsx", "eLab_storage_samples.csv")
#compare_sorted_to_submitted_PPBC("eLab_storage_samples.csv", "Sample Submissions and Data/mpIF-IF/SPECTRUM_Slides_mpIF_Feb2021.xlsx", "SPECTRUM_Slides_mpIF_Feb2021_GYN_eLab.csv")
compare_sorted_to_submitted_diag("~/Desktop/MSKCC/ARCHIVE_SPECTRUM/Database Management/ELAB PULL/elabpull wMRN_031021.xlsx", "Sample Submissions and Data/mpIF-IF/SPECTRUM_Slides_mpIF_Feb2021.xlsx", "SPECTRUM_Slides_mpIF_Feb2021_diag_eLab.csv")