'''
Created on March 26, 2020

@author: limj@mskcc.org
'''
import pprint
import pandas as pd
import json
import numpy as np

pp = pprint.PrettyPrinter(indent=4)

class Transformation(object):
    '''
    This is an experimental class for the integration of genomic data and pathology data from eLabInventory
    and REDCap respectively.
    '''

    def __init__(self):
        eldf = Elab_DataFrame('filtered_elab_sample_data')
        rcdf = RedCap_DataFrame('hne_metadata')
        final_df = eldf.merge(rcdf)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
        print(final_df)

class DataFrame:
    '''
    This is an experimental class for the import and transformation of genomic data and pathology data various databases
    into a dataframe.
    '''

    def __init__(self, file_name):
        self.dataframe = self.create_dataframe(file_name)

    def create_dataframe(self, file_name):
        with open(file_name) as data_file:
            metadata = json.load(data_file)
        return pd.DataFrame(metadata)

    def site_transform(self, specimen_site, site_details):
        df = self.dataframe
        df_blank = df.replace(np.nan, '', regex=True)
        df_blank.loc[df_blank[site_details] != "", specimen_site] = df_blank[site_details]
        df_blank = df.replace({'gyn_pathology_specimen_site':
                                   {'Omentum': 'Infracolic Omentum',
                                    'Peritoneum': 'Pelvic Peritoneum'}})
        self.df_blank = df_blank

    def merge(self, other_df):
        merged_df = pd.merge(self.df_blank, other_df.df_blank, how='left', left_on=['Patient ID', 'Specimen Site'], right_on=['patient_id', 'gyn_pathology_specimen_site'])
        final_df = merged_df.set_index(["Patient ID", "Specimen Site"])
        return final_df

class Elab_DataFrame(DataFrame):
    '''
    This is an child class for the transformation of genomic data from eLabInventory.
    '''

    def __init__(self, file_name):
        DataFrame.__init__(self, file_name)
        self.site_transform()

    def site_transform(self, specimen_site="Specimen Site", site_details="Site Details"):
        DataFrame.site_transform(self, specimen_site, site_details)

class RedCap_DataFrame(DataFrame):
    '''
    This is an child class for the transformation of pathology data from REDCap.
    '''

    def __init__(self, file_name):
        DataFrame.__init__(self, file_name)
        self.format_redcap_dataframe()
        self.site_transform()

    def format_column_header(self, header):
        self.dataframe[header] = self.dataframe[header].str.title()

    def format_redcap_dataframe(self):
        indexNames = self.dataframe[self.dataframe['gyn_pathology_therapy'] == "post-Rx"].index
        self.dataframe.drop(indexNames, inplace=True)

        self.format_column_header('gyn_pathology_specimen_site')
        self.format_column_header('gyn_pathology_specimen_subsite')

    def site_transform(self, specimen_site="gyn_pathology_specimen_site", site_details="gyn_pathology_specimen_subsite"):
        DataFrame.site_transform(self, specimen_site, site_details)