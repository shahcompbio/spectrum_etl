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
        rcdf = RedCap_DataFrame('hne_metadata')
        eldf = Elab_DataFrame('filtered_elab_sample_data')
        print(rcdf.indexed_df)
        print(eldf.indexed_df)
        #resulting_df = rcdf.merge(eldf)
        #resulting_df = eldf.merge(rcdf)

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
        self.df_blank = df_blank

    def set_index(self, pt_id, specimen_site):
        df = self.df_blank
        indexed_df = df.set_index([pt_id, specimen_site]).sort_values(by=[pt_id, specimen_site], ascending='false')
        self.indexed_df = indexed_df

    def merge(self, other_df):



class Elab_DataFrame(DataFrame):
    '''
    This is an child class for the transformation of genomic data from eLabInventory.
    '''

    def __init__(self, file_name):
        DataFrame.__init__(self, file_name)
        self.site_transform()
        self.set_index()

    def site_transform(self, specimen_site="Specimen Site", site_details="Site Details"):
        DataFrame.site_transform(self, specimen_site, site_details)

    def set_index(self, pt_id="Patient ID", specimen_site="Specimen Site"):
        return DataFrame.set_index(self, pt_id, specimen_site)


class RedCap_DataFrame(DataFrame):
    '''
    This is an child class for the transformation of pathology data from REDCap.
    '''

    def __init__(self, file_name):
        DataFrame.__init__(self, file_name)
        self.format_redcap_dataframe()
        self.site_transform()
        self.set_index()

    def format_column_header(self, header):
        self.dataframe[header] = self.dataframe[header].str.title()

    def format_redcap_dataframe(self):
        indexNames = self.dataframe[self.dataframe['gyn_pathology_therapy'] == "post-Rx"].index
        self.dataframe.drop(indexNames, inplace=True)

        self.format_column_header('gyn_pathology_specimen_site')
        self.format_column_header('gyn_pathology_specimen_subsite')

    def site_transform(self, specimen_site="gyn_pathology_specimen_site", site_details="gyn_pathology_specimen_subsite"):
        DataFrame.site_transform(self, specimen_site, site_details)

    def set_index(self, pt_id="patient_id", specimen_site="gyn_pathology_specimen_site"):
        DataFrame.set_index(self, pt_id, specimen_site)