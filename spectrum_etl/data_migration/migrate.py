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
         self.add_missing_keys()

    def add_missing_keys(self, sample_sets=None):
        '''
        Extract SCRNA table from elab, look for records that are missing keys and add them with empty values.
        '''

        headers = {'Authorization': default_config.get_elab_api_token(), "Host": default_config.get_elab_host_url()}

        # get sample count
        response = requests.get(default_config.get_elab_api_url()+'sampleSeries?$records=1', headers=headers)
        total_records = response.json()['totalRecords']

        # get all sample meta meta data
        page = 0
        sample_sets = []
        while len(sample_sets) != total_records:
            response = requests.get(default_config.get_elab_api_url() + 'sampleSeries?$page='+str(page), headers=headers)
            sample_sets += response.json()['data']
            page += 1

        assert len(sample_sets) == total_records

        sample_meta_key_list = []

        for sample_set in sample_sets:
            sample = {}
            for sample_id in sample_set['sampleIDs']:

                response = requests.get(
                    default_config.get_elab_api_url() + 'samples/{sampleid}'.format(sampleid=sample_id), headers=headers)

                sample_json = response.json()
                sample['patient_id'] = sample_json['name']
                sample['type'] = sample_json['sampleType']['name']

                response = requests.get(
                    default_config.get_elab_api_url() + 'samples/{sampleid}/meta'.format(sampleid=sample_id),
                    headers=headers)
                sample_meta_list = response.json()['data']

                for field in sample_meta_list:
                    sample[field['key']] = 'x'
                    #sample[field['key']+'SampleDataType'] = field['sampleDataType']
                    #sample[field['key']+'SampleTypeMetaID'] = field['sampleTypeMetaID']
                    #if 'value' in field.keys():
                    #    sample['value'] = field['value']
                    #else:
                    #    sample['value'] = '<<MISSING>>'
            sample_meta_key_list.append(sample)



        # build csv header
        all_keys = []
        for sample_meta in sample_meta_key_list:
            for key in sample_meta.keys():
                all_keys.append(key)
        unique_keys = set(all_keys)

        with open('elab_data_migration.csv', 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file,
                                fieldnames=unique_keys,

                                )
            fc.writeheader()
            fc.writerows(sample_meta_key_list)






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

    ElabMigration()