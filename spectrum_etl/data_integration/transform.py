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
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
        self.eldf = Elab_DataFrame('filtered_elab_sample_data')
        self.rcdf = RedCap_DataFrame('hne_metadata')

    def transform(self):
        final_df = self.eldf.merge(self.rcdf)

        with open("output_for_drill", 'w') as outfile:
            final_df.to_json(path_or_buf=outfile, orient='table')


class DataFrame:
    '''
    A high level abstraction of a pandas dataframe for multi-modal data.
    '''

    def __init__(self, file_name):
        self.dataframe = self.__create_dataframe(file_name)

    def __create_dataframe(self, file_name):
        with open(file_name) as data_file:
            metadata = json.load(data_file)
        return pd.DataFrame(metadata)

    def site_transform(self, specimen_site, site_details):
        '''
        Replaces all NaNs with empty strings, replaces specimen_site with values of site_details if available
        @:param specimen_site column name of specimen site in this table
        @:param site_details column name of site details in this table
        :returns the transformed dataframe
        '''

        df = self.dataframe
        df_blank = df.replace(np.nan, '', regex=True)
        df_blank.loc[df_blank[site_details] != "", specimen_site] = df_blank[site_details]
        self.df_blank = df_blank
        return self.df_blank

    def merge(self, other_df):
        '''
        Merges the dataframe based on preferred column headers and sets and sorts the index of merged table to Patient ID and Specimen Site
        @:param other_df the data frame to be merged into the object
        :returns the merged dataframe
        '''

        merged_df = pd.merge(self.df_blank, other_df.df_blank, how='left', left_on=['Patient ID', 'Specimen Site'], right_on=['patient_id', 'gyn_pathology_specimen_site'])
        final_df = merged_df.set_index(["Patient ID", "Specimen Site"]).sort_values(['Patient ID', 'Specimen Site'], ascending=True)
        # upon merge, Specimen Site pulls from the elab version, so the details from redcap specimen site does not merge
        # how do we transfer redcaps specimen site to the merged table as well?
        return final_df

class Elab_DataFrame(DataFrame):
    '''
    This is an child class for the transformation of genomic data from eLabInventory.
    '''

    def __init__(self, file_name):
        super().__init__(file_name)
        self.site_transform()

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

    def __format_column_header(self, header):
        '''
        Capitalizes the headers of each column
        '''
        self.dataframe[header] = self.dataframe[header].str.title()

    def __format_redcap_dataframe(self):
        '''
        Removes rows with post-Rx patient data
        '''
        indexNames = self.dataframe[self.dataframe['gyn_pathology_therapy'] == "post-Rx"].index
        self.dataframe.drop(indexNames, inplace=True)

        self.__format_column_header('gyn_pathology_specimen_site')
        self.__format_column_header('gyn_pathology_specimen_subsite')

    def site_transform(self, specimen_site="gyn_pathology_specimen_site", site_details="gyn_pathology_specimen_subsite"):
        self.dataframe = self.dataframe.replace({'gyn_pathology_specimen_site':
                                   {'Omentum': 'Infracolic Omentum',
                                    'Peritoneum': 'Pelvic Peritoneum'}})
        super().site_transform(specimen_site, site_details)
