'''
Created on June 06, 2020

@author: pashaa@mskcc.org
'''

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import csv
import sys

from spectrum_etl.config import default_config
import pprint
import requests
import codecs
import json
import logging.config

pp = pprint.PrettyPrinter(indent=4)
# sample 004 - 7113160 - count 32
# sample 81 - 7115269 - count 76
# my sample 1 - 7115337 - count 68

# list all keys for the 3 samples and compare (and compare to list below)
# add a key that belongs to schema to my sample (see if it works)
# check to see if/how it affects view in UI
# see if delete key works
# add a key that does not belong to schema in my sample (see if it works)
# see if delete key works

'''
keys to be removed:
--------------------
cDNA QC File
DLP iLab Submission Form
DLP REX Sample ID
DLP REX Submission Form
DLP Sample Status
DLP IGO Submission ID
Library QC File
Microdissected?
Tumour Content (%)

complete key list:
-------------------
# of Cells Captured
# of Curls Cut
# Slides Cut for Microdissection
# Slides Submitted
BCCRC DLP Submission Form
BCCRC Jira Ticket
BCCRC Sample ID
BCCRC Sequencing ID
Concentration (ng/ul)
Date received from PPBC
Date requested from PPBC
DLP Date of Submission
DLP IGO ID
DLP iLab Submission Form (IGO)
DLP REX Sample ID (IGO)
DLP REX Submission Form (IGO)
DLP Sample Status (IGO)
DLP Sequencing Location
Downstream Submission
Excluded
Final Pathology
Flow Data fcs files
Flow Data Summary
Flow Instrument
H&E available?
IF Date of Submission
IF Panel
Initial Submission QC
Live Cell Count (cells/ml)
MRN
Notes
Patient ID
PPBC Accession #
PPBC Aliquot Number
PPBC Bank Number
PPBC Downstream Submission
Primary Site
Processing Date
QC Checks
Reason for exclusion
Room
scRNA Date of Submission
scRNA IGO ID
scRNA IGO Submission ID
scRNA iLab Submission Form
scRNA REX Sample ID
scRNA REX Submission Form
scRNA Sample Status
scRNA Sequencing Location
Sectioning Type
Sequencing Technique
Site Details
Sorting Method
Specify Diagnosis
Specimen Site
Storage Populations
Submitted Populations
Surgeon
Surgery #
Surgery Date
Surgery Location
Surgery Type
Thickness of tissue (um)
Tissue Type
Total Cell Count (cells/ml)
Total Volume (ml)
Viability (%)
Volume (ul)
WGS Date of Submission
WGS IGO ID
WGS IGO Submission ID
WGS iLab Submission Form
WGS Requested Reads
WGS REX Sample ID
WGS REX Submission Form
WGS Sample Status
WGS Sequencing Location



'''

class ElabMigration(object):
    '''
    This class is built to bring all elab data to a uniform state after one or more schema migrations have been performed.

    '''

    def __init__(self):
        self.headers = {'Authorization': default_config.get_elab_api_token(), "Host": default_config.get_elab_host_url()}


    def get_sample_meta(self, sample_type_name, meta_key):
        ''' Get sample meta information for only the specified meta key in all samples with the specified sample type
        :param sample_type_name: sample type name
        :param meta_key: meta key (field name)

        :returns example:
            {'meta_key': 'BCCRC Jira Ticket',
             'meta_option_values': [],
             'meta_sample_data_type': 'TEXT',
             'meta_sample_type_id': 25463,
             'sample_type_name': 'Tissue'}
        '''

        response = requests.get(default_config.get_elab_api_url() + 'sampleTypes', headers=self.headers)
        # get all sample types
        sample_types = response.json()['data']

        ret_type = None

        for type in sample_types:
            # filter by specified sample type name
            if type['name'] == sample_type_name:
                response = requests.get(default_config.get_elab_api_url() + 'sampleTypes/'+str(type['sampleTypeID'])+'/meta', headers=self.headers)
                sampleTypeMeta = response.json()['data']

                for meta in sampleTypeMeta:
                    if meta['key'] == meta_key:

                        ret_type = {
                            'sample_type_name': type['name'],
                            'meta_key': meta['key'],
                            'meta_sample_data_type': meta['sampleDataType'],
                            'meta_sample_type_id': meta['sampleTypeID'],
                            'meta_option_values': meta['optionValues']
                        }

                        return ret_type

        return ret_type


    def get_all_sample_sets(self):
        logger.info('getting all samples...')

        # get sample count
        response = requests.get(default_config.get_elab_api_url() + 'sampleSeries?$records=1', headers=self.headers)
        total_records = response.json()['totalRecords']

        # get all sample meta meta data
        page = 0
        sample_sets = []
        while len(sample_sets) != total_records:
            response = requests.get(default_config.get_elab_api_url() + 'sampleSeries?$page=' + str(page),
                                    headers=self.headers)
            sample_sets += response.json()['data']
            page += 1

        assert len(sample_sets) == total_records

        return sample_sets

    def get_sample(self, sample_id):
        ''':returns: Sample with the specified sample id. '''

        response = requests.get(
            default_config.get_elab_api_url() + 'samples/{sample_id}'.format(sample_id=sample_id), headers=self.headers)

        return response.json()

    def get_sample_meta(self, sample_id):
        response = requests.get(
            default_config.get_elab_api_url() + 'samples/{sample_id}/meta'.format(sample_id=sample_id),
            headers=self.headers)
        return response.json()

    def delete_sample_meta(self, sample_id, sample_meta_id):
        response = requests.delete(
            default_config.get_elab_api_url() + 'samples/{sample_id}/meta/{sample_meta_id}'.format(
                sample_id=sample_id, sample_meta_id=sample_meta_id),
                headers=self.headers)
        return response.status_code

    def is_key_in_sample_meta(self, sample_id, key):
        sample_meta_data = self.get_sample_meta(sample_id)['data']

        for element in sample_meta_data:
            if key == element['key']: return True

        return False

    def get_sample_type(self, name):
        '''
        Get sample type with specified name.
        '''
        response = requests.get(
            default_config.get_elab_api_url() + 'sampleTypes?name={name}'.format(name=name),
            headers=self.headers)
        return response.json()

    def get_sample_type_meta(self, sample_type_id):
        '''
        Get sample type meta with specified sample_type_id.
        '''
        response = requests.get(
            default_config.get_elab_api_url() + 'sampleTypes/{sample_type_id}/meta'.format(sample_type_id=sample_type_id),
            headers=self.headers)
        return response.json()

    def is_key_in_sample_type_meta(self, sample_type_id, key):
        sample_type_meta_data = self.get_sample_type_meta(sample_type_id)['data']

        for element in sample_type_meta_data:
            if key == element['key']: return True

        return False

    def get_sample_type_meta_id(self, sample_type_id, key):
        sample_type_meta_data = self.get_sample_type_meta(sample_type_id)['data']

        for element in sample_type_meta_data:
            if key == element['key']: return element['sampleTypeMetaID']

        return None

    def get_sample_data_type(self, sample_type_id, key):
        sample_type_meta_data = self.get_sample_type_meta(sample_type_id)['data']

        for element in sample_type_meta_data:
            if key == element['key']: return element['sampleDataType']

        return None



    def put_sample_meta(self, sample_id, key):
        '''
        This call will check if a meta field with the specified key already exists in the sample record with the
         specified sample_id. If it does exist, nothing is done.

        If a meta field with the specified key does not exist it, then a new meta field is created with an empty
         value.

        The key must exist in the sample type definition of the sample. This implies that the key needs to
         be added to the sample type definition for the sample before the key can be added to existing records
         through this function.

        The value for the key is always set to the empty string.

        :param sample_id sample id
        :param key field name
        :param sampleTypeMetaID sample type meta ID or field id defined in the sample type of sample with the
               specified sample id

        :returns updated sample record.

        :raise exception
             if key is not found in the sample type definition of sample specified by sample_id.
        '''
        # if key already exists in sample, do nothing
        if self.is_key_in_sample_meta(sample_id, key):
            return

        # get sample type id from sample with specified sample id
        sample = self.get_sample(sample_id)
        sample_type_id = sample['sampleType']['sampleTypeID']

        # check if key exists in sample type meta
        if self.is_key_in_sample_type_meta(sample_type_id, key) == False:
            raise Exception('key '+key+' is not found in sample type definition for sample with sample id '
                            +sample_id+'. See sample type definition -  \n'+
                            json.dumps(self.get_sample_type_meta(sample_type_id), indent=1))

        # put key with empty value field

        # data = '{ \
        #         "key": "'+key+'", \
        #         "sampleTypeMetaID": '+str(self.get_sample_type_meta_id(sample_type_id, key))+', \
        #         "sampleDataType": "'+self.get_sample_data_type(sample_type_id, key)+'" \
        #         }'

        data = {
                "key": key,
                "sampleTypeMetaID": self.get_sample_type_meta_id(sample_type_id, key),
                "sampleDataType": self.get_sample_data_type(sample_type_id, key)
              }

        print(data)

        response = requests.post(
            default_config.get_elab_api_url() + 'samples/{sample_id}/meta'.format(sample_id=sample_id),
            headers=self.headers, data=data)
        logger.info('put missing key ' + key + ' for sample with '
                    + sample_id + ' response: ' + str(response.text))

        response = requests.get(
            default_config.get_elab_api_url() + 'samples/{sample_id}/meta'.format(sample_id=sample_id),
            headers=self.headers)
        return response.json()


    def synch_db(self, sample_id):
        '''
        Algorithm:
        ----------
        Given sample id - provide stats - number of samples in series, number of fields per sample, number of fields per sample that is not null etc.

        schema is ground truth

        1. data fields are in schema      [do nothing]
        2. data fields are not in schema  [a) remove only if empty, b) force remove]
        3. schema fields are in data      [do nothing]
        4. schema fields are not in data  [add with empty values]


        monitoring run
            pull schema fields
            run checks 1-4 for all data
            report

        sync run
            pull schema fields
            run checks 1-4 for all data
            fix for case 2,4
            validate sync (case 2,4 results in empty sets)
            report fixes

        in the future, have an exlusion criteria
        '''
        pass



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

    #ElabMigration().add_missing_keys(keys=[{'name':'BCCRC Jira Ticket','sample_type_meta_id':11111,'sample_data_type':''}])

    #pp.pprint(ElabMigration().get_sample_meta('Tissue', 'BCCRC Jira Ticket'))

    x = ElabMigration().put_sample_meta('7115337', 'Total Cell Count (cells/ml)')

    #x = ElabMigration().delete_sample_meta('7115337', '58625757')

    #x = ElabMigration().get_sample_meta('7115337')

    #sample_type = ElabMigration().is_key_in_sample_type_meta('25463', 'DLP sample Status (IGO)')
    #keys = []

    #for field in sample:
    #    keys.append((field['key'], field['value']))

    pp.pprint(x)

    #sampleType = ElabMigration().get_sample_type('Tissue')

    #pp.pprint(sampleType)