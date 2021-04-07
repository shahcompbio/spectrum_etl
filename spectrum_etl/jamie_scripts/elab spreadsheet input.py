import os
import pandas as pd
import datetime
import numpy as np

def import_OR_record_sheet(OR_fname, output_OR_fname):
    full_path = os.path.expanduser(OR_fname)
    OR_file = pd.read_excel(full_path)

    OR_file['Spectrum-OV'] = 'SPECTRUM-OV-' + OR_file['Spectrum-OV'].astype(str)
    OR_file['Surgery Date'] = OR_file['Surgery Date'].apply(
        lambda x: x.date() if isinstance(x, datetime.datetime) else x)

    OR_file = OR_file[["Notes", "Spectrum-OV", "MRN", "Surgery Type", "Surgery Date", "Attending", "Surgery Location", "Room", "Study Protocol", "Excluded", "Final Path"]]

    OR_file.to_excel(output_OR_fname)


def import_IGO_storage_sheet(IGO_fname, elab_fname, output_fname):
    IGO_path = os.path.expanduser(IGO_fname)
    elab_path = os.path.expanduser(elab_fname)
    IGO_file = pd.read_excel(IGO_path, usecols=["IGO ID", "Sample ID"])
    elab_file = pd.read_excel(elab_path)

    IGO_file.dropna(subset=["Sample ID"], inplace=True)

    IGO_file.set_index("Sample ID")
    elab_file.set_index("scRNA REX Sample ID")

    all_data = pd.merge(IGO_file, elab_file, how='left', left_on="Sample ID", right_on="scRNA REX Sample ID")

    all_data["Storage Facility"] = "IGO"
    all_data = all_data[
        ["Patient ID", "MRN", "Surgery Type", "Surgery Date", "Surgeon", "Surgery Location", "Room", "Study Protocol",
         "Excluded", "Final Pathology", "Processing Date", "Specimen Site", "Site Details", "Primary Site",
         "Tissue Type", "Preservation Method", "Downstream Submission", "Submitted Populations", "Storage Facility", "IGO ID", "Sample ID"]].sort_values(by='Sample ID')

    all_data.to_excel(output_fname)

#import_OR_record_sheet("~/Desktop/MSKCC/SPECTRUM/Sample Collection/Spectrum Patient OR Collection Record.xlsx", "elab SPECTRUM Patient OR Collection Record.xlsx")
import_IGO_storage_sheet("~/Desktop/MSKCC/SPECTRUM/Sample Collection/Sample Processing & Storage/IGO 121620 - Spectrum Remainder Aliquots Post-10X.xlsx", "~/Desktop/MSKCC/SPECTRUM/Database Management/ELAB PULL/elabpull wMRN 121620.xlsx", 'elab IGO Storage Aliquots.xlsx')