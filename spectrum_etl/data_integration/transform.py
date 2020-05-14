'''
Created on March 26, 2020

@author: limj@mskcc.org
'''
import codecs
import logging
import pprint
import pandas as pd
import json
import numpy as np
import sys
from spectrum_etl.data_integration import validation

pp = pprint.PrettyPrinter(indent=4)

class Transformation(object):
    '''
    This is an experimental class for the integration of genomic data and pathology data from eLabInventory
    and REDCap respectively.
    '''

    def __init__(self, elab_file_name, redcap_file_name):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
        self.eldf = Elab_DataFrame(elab_file_name)
        self.rcdf = RedCap_DataFrame(redcap_file_name)

    # merge elab and redcap data frame and export to csv and json file
    def transform(self):
        final_df = self.eldf.merge(self.rcdf)
        final_df.to_csv(r'merged_metadata_from_elab_redcap.csv', index=True, header=True)

        with open("output_for_drill", 'w') as outfile:
            final_df.to_json(path_or_buf=outfile, orient='table')

        return final_df

class DataFrame:
    '''
    A high level abstraction of a pandas dataframe for multi-modal data.
    '''

    def __init__(self, file_name):
        self.dataframe = self.__create_dataframe(file_name)

    # open json file and load into data frame
    def __create_dataframe(self, file_name):
        with open(file_name) as data_file:
            metadata = json.load(data_file)
        return pd.DataFrame(metadata)

    # replace all NaNs with empty strings, replace specimen_site with values of site_details if available
    def site_transform(self, specimen_site, site_details):
        df = self.dataframe
        df_blank = df.replace(np.nan, '', regex=True)
        df_blank.loc[df_blank[site_details] != "", specimen_site] = df_blank[site_details]
        self.df_blank = df_blank
        return self.df_blank

    # merge dataframe based on preferred column headers, sets and sorts the index of merged table to Patient ID and Specimen Site
    def merge(self, other_df):
        merged_df = pd.merge(self.df_blank, other_df.df_blank, how='left', left_on=['Patient ID', 'Specimen Site'], right_on=['patient_id', 'gyn_pathology_specimen_site'])
        final_df = merged_df.set_index(["Patient ID", "Specimen Site"], append=True).sort_values(['Patient ID', 'Specimen Site'], ascending=True)
        return final_df

class Elab_DataFrame(DataFrame):
    '''
    This is an child class for the transformation of genomic data from eLabInventory.
    '''

    def __init__(self, file_name):
        super().__init__(file_name)
        self.__validate()
        self.site_transform()

    # pull patient id and specimen site from data frame and run validation code
    def __validate(self):
        allPass = True
        for row in self.dataframe.iterrows():
            if not validation.is_pt_id_valid(row):
                logger.error("Invalid Patient ID: %s" % row["Patient ID"])
                allPass = False

            if not validation.is_mrn_valid(row):
                logger.error("Invalid MRN (%s) for %s." % (row["MRN"], row["Patient ID"]))
                allPass = False

            if not validation.is_surgery_id_valid(row):
                logger.error("Please ensure surgery ID is valid for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_patient_excluded(row):
                allPass = False

            if not validation.is_specimen_site_valid(row):
                allPass = False

            if not validation.is_downstream_submission_valid(row):
                allPass = False

            if not validation.is_seq_info_valid(row):
                allPass = False

            if not validation.is_submitted_populations_valid(row):
                allPass = False

            if not validation.is_scrna_igo_id_valid(row):
                logger.error("Please ensure scRNA IGO ID is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_scrna_igo_sub_id_valid(row):
                logger.error("Please ensure scRNA IGO Submission ID is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_scrna_rex_id_valid(row):
                logger.error("Please ensure scRNA REX ID is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_qc_checks_valid(row):
                logger.error("Please ensure input for QC Checks are valid for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_dlp_rex_id_valid(row):
                logger.error("Please ensure DLP REX ID is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_wgs_tissue_type_valid(row):
                logger.error("Please ensure WGS bulk tumour tissue type is accurate for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_ppbc_acc_num_valid(row):
                logger.error("Please ensure PPBC accession number is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_ppbc_bank_num_valid(row):
                logger.error("Please ensure PPBC bank number is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_wgs_igo_id_valid(row):
                logger.error("Please ensure WGS IGO ID is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_wgs_igo_submission_id_valid(row):
                logger.error("Please ensure WGS IGO Submission ID is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_wgs_rex_id_valid(row):
                logger.error("Please ensure WGS REX ID is in proper format for %s." % row["Patient ID"])
                allPass = False

            if not validation.is_if_tissue_type_valid(row):
                logger.error("Please ensure IF tissue type is accurate for %s." % row["Patient ID"])
                allPass = False

        if allPass == False:
            sys.exit(1)

    # run site_transform from parent class
    def site_transform(self, specimen_site="Specimen Site", site_details="Site Details"):
        DataFrame.site_transform(self, specimen_site, site_details)

class RedCap_DataFrame(DataFrame):
    '''
    This is an child class for the transformation of pathology data from REDCap.
    '''

    def __init__(self, file_name):
        super().__init__(file_name)
        self.__format_redcap_dataframe()
        self.site_transform()

    # capitalize the headers of each column
    def __format_column_header(self, header):
        self.dataframe[header] = self.dataframe[header].str.title()

    # remove rows with post-Rx patient data
    def __format_redcap_dataframe(self):
        indexNames = self.dataframe[self.dataframe['gyn_pathology_therapy'] == "post-Rx"].index
        self.dataframe.drop(indexNames, inplace=True)

        self.__format_column_header('gyn_pathology_specimen_site')
        self.__format_column_header('gyn_pathology_specimen_subsite')

    # run site_transform from parent class
    def site_transform(self, specimen_site="gyn_pathology_specimen_site", site_details="gyn_pathology_specimen_subsite"):
        self.dataframe = self.dataframe.replace({'gyn_pathology_specimen_site':
                                   {'Omentum': 'Infracolic Omentum',
                                    'Peritoneum': 'Pelvic Peritoneum'}})
        super().site_transform(specimen_site, site_details)


if __name__ == '__main__':
    # create an initial logger. It will only log to console and it will disabled
    # when we read the logging configuration from the config file.
    # This logger can be useful when we need early logging. E.g. we may want to log
    # the location of the JSON file (e.g. if we get it from a CLI argument).
    logging.basicConfig(level="INFO")
    logger = logging.getLogger()
    logger.info("This is the logger configured by `logging.basicConfig()`.")

    # Load the configuration.
    config_file = "config_logging.json"
    with codecs.open(config_file, "r", encoding="utf-8") as fd:
        config = json.load(fd)

    # Set up proper logging. This one disables the previously configured loggers.
    logging.config.dictConfig(config["logging"])

    transform = Transformation("elab_metadata", "hne_metadata")
    transform.transform()