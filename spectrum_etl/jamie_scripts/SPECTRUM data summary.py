import os
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

def import_scrna_from_github(scrna_fname):
    full_path = os.path.expanduser(scrna_fname)
    scrna_file = pd.read_csv(full_path, sep ='\t')

    # format imported spreadsheet
    scrna_file[['Patient ID', 'Surgery ID', 'Specimen Site']] = scrna_file['sample_id'].str.split('_', n=2, expand=True)
    scrna_file['Specimen Site'] = scrna_file['Specimen Site'].str.title().str.replace('_', " ")

    # ammend pt id to include post-tx ids
    scrna_file.loc[scrna_file['Surgery ID'] == 'S2', 'Patient ID'] = scrna_file['Patient ID'] + "-1"
    scrna_file.loc[scrna_file['Surgery ID'] == 'S3', 'Patient ID'] = scrna_file['Patient ID'] + "-3"
    scrna_file['Platform'] = "scRNA"
    scrna_final = scrna_file[['Platform', 'Patient ID', 'Specimen Site']]

    scrna_final.to_excel("Output Data files/scRNA_wdata.xlsx")
    return scrna_final

def import_dlp_from_github(dlp_fname):
    full_path = os.path.expanduser(dlp_fname)
    dlp_file = pd.read_csv(full_path, sep='\t')

    # format imported spreadsheet
    dlp_file[['Patient ID', 'Surgery ID', 'Populations', 'Specimen Site']] = dlp_file['isabl_id'].str.split('_', n=3, expand=True)
    dlp_file['Specimen Site'] = dlp_file['Specimen Site'].str.title().str.replace('_', " ")

    # ammend pt id to include post-tx ids
    dlp_file = dlp_file[dlp_file['Patient ID'] != "SPECTRUM-OV-001"]
    dlp_file.loc[dlp_file['Surgery ID'] == 'S2', 'Patient ID'] = dlp_file['Patient ID'] + "-1"
    dlp_file.loc[dlp_file['Surgery ID'] == 'S3', 'Patient ID'] = dlp_file['Patient ID'] + "-3"
    dlp_file['Platform'] = "DLP"
    dlp_final = dlp_file[['Platform', 'Patient ID', 'Specimen Site']]

    dlp_final.to_excel("Output Data files/dlp_wdata.xlsx")
    return dlp_final

def import_ifmpif_from_github(ifmpif_fname):
    full_path = os.path.expanduser(ifmpif_fname)
    ifmpif_file = pd.read_csv(full_path, sep=',')

    # format imported spreadsheet
    ifmpif_file[['Patient ID', 'Surgery ID', 'Specimen Site']] = ifmpif_file['isabl_id'].str.split('_', n=2, expand=True)
    ifmpif_file['Specimen Site'] = ifmpif_file['Specimen Site'].str.title().str.replace('_', " ")

    # ammend pt id to include post-tx ids
    ifmpif_file.loc[ifmpif_file['Surgery ID'] == 'S2', 'Patient ID'] = ifmpif_file['Patient ID'] + "-1"
    ifmpif_file.loc[ifmpif_file['Surgery ID'] == 'S3', 'Patient ID'] = ifmpif_file['Patient ID'] + "-3"
    ifmpif_file['Platform'] = "IF/mpIF"
    ifmpif_final = ifmpif_file[['Platform', 'Patient ID', 'Specimen Site']]

    ifmpif_final.to_excel("Output Data files/ifmpif_wdata.xlsx")
    return ifmpif_final

def import_wgs_from_github(wgs_fname):
    full_path = os.path.expanduser(wgs_fname)
    wgs_file = pd.read_csv(full_path, sep='\t')

    # format imported spreadsheet
    wgs_file[['Patient ID', 'Surgery ID', 'Specimen Site']] = wgs_file['isabl_id'].str.split('_', n=2, expand=True)
    wgs_file['Specimen Site'] = wgs_file['Specimen Site'].str.title().str.replace('_', " ")

    # ammend pt id to include post-tx ids
    wgs_file['Platform'] = "WGS"
    wgs_file.loc[wgs_file['Surgery ID'] == 'S2', 'Patient ID'] = wgs_file['Patient ID'] + "-1"
    wgs_file.loc[wgs_file['Surgery ID'] == 'S3', 'Patient ID'] = wgs_file['Patient ID'] + "-3"
    wgs_file.loc[wgs_file['Surgery ID'] == 'BC1', ['Platform', 'Specimen Site']] = ["WGS-Normal", 'Buffy Coat']
    wgs_final = wgs_file[['Platform', 'Patient ID', 'Specimen Site']]

    wgs_final.to_excel("Output Data files/wgs_wdata.xlsx")
    return wgs_final

def data_summary_vis(scrna_fname, dlp_fname, ifmpif_fname, wgs_fname, storage_filename, plot_file_name):
    scrna_file = import_scrna_from_github(scrna_fname)
    dlp_file = import_dlp_from_github(dlp_fname)
    if_file = import_ifmpif_from_github(ifmpif_fname)
    wgs_file = import_wgs_from_github(wgs_fname)

    # import elab pull and filter for storage aliquots from patients included in study
    storage_aliquots = pd.read_excel(storage_filename)
    filtered_aliquots = storage_aliquots.loc[(storage_aliquots['Excluded'] == "No") & (storage_aliquots['Downstream Submission'] == "Storage Only")]
    pt_id_aliquots = filtered_aliquots["Patient ID"].drop_duplicates()
    patients = pt_id_aliquots.tolist()

    all_data_files = pd.concat([scrna_file, dlp_file, if_file, wgs_file], axis=0, sort=True)
    all_data_files = all_data_files[["Platform", "Patient ID"]]

    data_dict = {}
    for i in all_data_files["Platform"].tolist():
        data_dict[i] = all_data_files[all_data_files["Platform"] == i]["Patient ID"].tolist()

    platforms = []
    matrix = []

    #identify matrix size (x and y length)
    for key, value in sorted(data_dict.items()):
        platforms.append(key)
        for patient in value:
            if patient not in patients:
                patients.append(patient)
    patients.sort()

    #create matrix from key value pairs
    currentPlatform = 0
    for key, value in sorted(data_dict.items()):
        matrix.append([])
        # initialize each matrix row to 0
        matrix[currentPlatform] = [0] * len(patients)
        for patient in value:
            patientIndex = patients.index(patient)
            matrix[currentPlatform][patientIndex] = 1
        currentPlatform += 1

    patients = [patient.lstrip("SPECTRUM-") for patient in patients]
    print(patients)

    # plot matrix
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.matshow(matrix, cmap=plt.cm.Blues)

    plt.title('SPECTRUM Data Summary', weight='bold', fontsize=8)
    plt.xlabel('Patients wtih scs Stored', fontsize=4, weight='bold')
    plt.ylabel('Platforms', rotation='vertical', fontsize=4, weight='bold')

    ax.set_xticklabels([''] + patients, rotation='vertical', fontsize=3, ha="center")
    ax.set_yticklabels([''] + platforms, fontsize=3)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().xaxis.tick_bottom()

    ax.set_xticks(np.arange(-.5, len(patients)), minor=True)
    ax.set_yticks(np.arange(-.5, len(platforms)), minor=True)
    ax.grid(which="minor", linewidth=0.5, alpha=0.5)

    plt.tight_layout()
    plt.savefig(fname=plot_file_name, dpi=300)

# count number of patients and sites w/data for each platform
def count_samples_wdata(scrna_fname, dlp_fname, ifmpif_fname, wgs_fname):
    scrna_file = import_scrna_from_github(scrna_fname)
    dlp_file = import_dlp_from_github(dlp_fname)
    if_file = import_ifmpif_from_github(ifmpif_fname)
    wgs_file = import_wgs_from_github(wgs_fname)

    all_data_files = pd.concat([scrna_file, dlp_file, if_file, wgs_file], axis=0, sort=True)
    all_data_files = all_data_files[["Platform", "Patient ID"]]

    data_counts = all_data_files['Platform'].value_counts().reset_index()
    data_counts.columns = ['Platform', 'Sites with Data']

    patients = all_data_files.drop_duplicates(subset=['Platform', 'Patient ID'])
    pt_counts = patients['Platform'].value_counts().reset_index()
    pt_counts.columns = ['Platform', 'Cases with Data']
    total_counts = pd.merge(data_counts, pt_counts, on="Platform", sort=True)
    print(total_counts[['Platform', 'Cases with Data', 'Sites with Data']])

# data_summary_vis("~/dev/metadata/metadata/spectrum/tsvs/scrna_samples.tsv", "~/dev/metadata/metadata/spectrum/tsvs/dlp_samples.tsv",
#                  "~/dev/metadata/metadata/spectrum/tsvs/mpif_samples.tsv", "~/dev/metadata/metadata/spectrum/tsvs/wgs_samples.tsv",
#                  "../ELAB PULL/elabpull wMRN_031021.xlsx", "SPECTRUM data summary")

count_samples_wdata("~/dev/metadata/metadata/spectrum/tsvs/scrna_samples.tsv", "~/dev/metadata/metadata/spectrum/tsvs/dlp_samples.tsv",
                    "~/dev/metadata/metadata/spectrum/tsvs/mpif_samples.tsv", "~/dev/metadata/metadata/spectrum/tsvs/wgs_samples.tsv")