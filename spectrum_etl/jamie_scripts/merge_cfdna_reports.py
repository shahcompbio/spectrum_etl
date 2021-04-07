import pandas as pd
import os

# merges all previously received cfDNA reports from Lab Medicine and converts to elab spreadsheet entry format
def merge_cfdna_reports(file1, file2, file3, file4, file5, file6, file7, file8, file9, file10, file11, file12, file13, file_name, saved_filename):
    mar19 = pd.read_excel(file1)
    apr19 = pd.read_excel(file2)
    may19 = pd.read_excel(file3)
    jun19 = pd.read_excel(file4)
    jul19 = pd.read_excel(file5)
    aug19 = pd.read_excel(file6)
    sep19 = pd.read_excel(file7)
    oct19 = pd.read_excel(file8)
    nov19 = pd.read_excel(file9)
    dec19 = pd.read_excel(file10)
    jan20 = pd.read_excel(file11)
    feb20 = pd.read_excel(file12)
    marapr20 = pd.read_excel(file13)
    mrn_record = pd.read_excel(file_name, converters={'Spectrum-OV': str})
    mrn_record['Spectrum-OV'] = 'SPECTRUM-OV-' + mrn_record['Spectrum-OV'].astype(str)

    merged_sheets = pd.concat([mar19, apr19, may19, jun19, jul19, aug19, sep19, oct19, nov19, dec19, jan20, feb20, marapr20])

    merged_sheets_id = pd.merge(merged_sheets, mrn_record,
                              on=['MRN'], how='left')

    merged_sheets_id.rename(columns={'Sample Status': 'Sample_status'}, inplace=True)
    merged_sheets_id['LM_sample_status'] = ""
    merged_sheets_id.loc[merged_sheets_id.Sample_status == "Extracted", 'LM_sample_status'] = "Extracted"
    merged_sheets_id.loc[merged_sheets_id.Sample_status == "Buffy Coat Stored", 'LM_sample_status'] = "Stored"

    merged_sheets_id['Sample_status'] = merged_sheets_id['Sample_status'].replace(['Extracted'], 'Plasma')
    merged_sheets_id['Sample_status'] = merged_sheets_id['Sample_status'].replace(['Buffy Coat Stored'], 'Buffy Coat')
    merged_sheets_id.drop(['Date/Time - Complete', 'IRB', 'Investigator', "Sample Type", "Specimen Type"], axis=1, inplace=True)
    merged_sheets_id = merged_sheets_id[["Spectrum-OV", "MRN", "Study Protocol", "Excluded", "Name", "Patient Name", "Surgery Date", "Sample_status", "Accession", "Accession ", "2D Barcode#", "Date/Time - Drawn",	"Date/Time - In Lab", "LM_sample_status", "Volume Extracted (mL)", "cfDNA Elution Volume (uL)", "cfDNA Conc (ng/uL)", "cfDNA Total Yield (ng)"]]

    merged_sheets_id.to_csv(saved_filename, index=False)

#merge_cfdna_reports("Zamarin_cfDNA_March 2019.xlsx",
                   # "Zamarin_cfDNA_April 2019.xlsx",
                   # "Zamarin_cfDNA_May 2019.xlsx",
                   # "Zamarin_cfDNA_June 2019.xlsx",
                   # "Zamarin_cfDNA_July 2019.xlsx",
                   # "Zamarin_cfDNA_August 2019.xlsx",
                   # "Zamarin_cfDNA_September 2019.xlsx",
                   # "Zamarin_cfDNA_October 2019.xlsx",
                   # "Zamarin_cfDNA_November 2019.xlsx",
                   # "Zamarin_cfDNA_December 2019.xlsx",
                   # "Zamarin_cfDNA_January 2020.xlsx",
                   # "Zamarin_cfDNA_February 2020.xlsx",
                   # "Zamarin_cfDNA_March-April 2020.xlsx",
                   # "mrn_record.xlsx",
                   #  "LM cfDNA Collection_mar19-apr20.csv")

# converts current monthly cfDNA reports received from Lab Medicine into elab spreadsheet entry column format
def convert_cfdna_reports_for_elab_entry(month_file, mrn_file_name, saved_filename):
    monthly_file = pd.read_excel(month_file)
    mrn_record = pd.read_excel(mrn_file_name, converters={'Spectrum-OV': str})
    mrn_record['Spectrum-OV'] = 'SPECTRUM-OV-' + mrn_record['Spectrum-OV'].astype(str)

    merged_sheets_id = pd.merge(monthly_file, mrn_record,
                                on=['MRN'], how='left')

    merged_sheets_id.rename(columns={'Sample Status': 'Sample_status'}, inplace=True)
    merged_sheets_id['LM_sample_status'] = ""
    merged_sheets_id.loc[merged_sheets_id.Sample_status == "Extracted", 'LM_sample_status'] = "Extracted"
    merged_sheets_id.loc[merged_sheets_id.Sample_status == "Buffy Coat Stored", 'LM_sample_status'] = "Stored"

    merged_sheets_id['Sample_status'] = merged_sheets_id['Sample_status'].replace(['Extracted'], 'Plasma')
    merged_sheets_id['Sample_status'] = merged_sheets_id['Sample_status'].replace(['Buffy Coat Stored'], 'Buffy Coat')
    merged_sheets_id.drop(['Date - Complete', 'IRB', 'Investigator Group', "Sample Type"], axis=1,
                          inplace=True)
    merged_sheets_id = merged_sheets_id[
        ["Spectrum-OV", "MRN", "Study Protocol", "Excluded", "Name", "Patient Name", "Surgery Date", "Sample_status", "Accession",
         "2D Barcode#", "Date - Drawn", "Date - In Lab", "LM_sample_status",
         "Volume Extracted (mL)", "cfDNA Elution Volume (uL)", "cfDNA Conc (ng/uL)", "cfDNA Total Yield (ng)"]]

    merged_sheets_id.to_csv(saved_filename, index=False)


convert_cfdna_reports_for_elab_entry("Zamarin_cfDNA_JanFeb2021.xlsx", "mrn_record.xlsx", "LM cfDNA Collection_JanFeb2021.csv")