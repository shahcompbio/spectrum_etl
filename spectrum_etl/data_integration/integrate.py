'''
Created on March 16, 2020

@authors: limj@mskcc.org; pashaa@mskcc.org
'''

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from spectrum_etl.config import default_config
import pprint
import requests
import codecs
import json
import logging.config
from spectrum_etl.data_integration import validation
import sys

pp = pprint.PrettyPrinter(indent=4)

class Integration(object):
    '''
    This is an experimental class for the integration of genomic data and pathology data from eLabInventory
    and REDCap respectively.
    '''

    def __init__(self):
         #self.extract_hne_table()
         #self.extract_scrna_table()
         self.__validate()
         #self.filter()

    def clean_json(self, json_str):
        '''
        Remove all carriage returns from the specified json string.

        :param json_str: json string with \r, \n
        :returns cleaned json string
        '''
        json_str = json_str.replace('\r', '')
        json_str = json_str.replace('\n', '')

        return json_str


    def extract_scrna_table(self, sample_sets=None):
        '''
        Extract SCRNA table from elab.
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

        # filter by patient subset
        patient_subset = []

        pt_id_list = []
        for ii in range(1,73):  # patients 1 to 72
            id = 'SPECTRUM-OV-0' + str("{:02d}".format(ii))
            pt_id_list.append(id)

        for sample in sample_sets:
            if sample['name'] in pt_id_list:
                patient_subset.append(sample)

        logger.info("attempting to get data for "+str(len(patient_subset))+" patients...")

        # get all sample meta data for patient subset
        #elab_sample_data = []

        elab_metadata = []

        for patient in patient_subset:
            sample_ids = patient["sampleIDs"]

            logger.info("getting data for patient "+patient['name'])

            for sample_id in sample_ids:
                response = requests.get(default_config.get_elab_api_url()+'samples/{sampleid}'.format(sampleid=sample_id), headers=headers)

                # filter sample meta data by Tissue samples only
                if response.json()["sampleType"]["name"] == "Tissue":
                    response = requests.get(default_config.get_elab_api_url() + 'samples/{sampleid}/meta'.format(sampleid=sample_id),headers=headers)
                    all_elab_metadata = response.json()

                    # pull key value attributes only from elab API pull
                    data = {}

                    for meta in all_elab_metadata['data']:
                        if 'value' not in meta.keys():
                            data[meta['key']] = meta['files'][0]['name']
                        else:
                            data[meta['key']] = meta['value']

                    elab_metadata.append(data)

        # break  # just collect 1 since it takes time to collect all

        with open("elab_metadata", 'w') as outfile:
            jstr = json.dumps(elab_metadata, sort_keys=True,
                  indent=2, separators=(',', ': '))
            outfile.write(jstr)

        # pp.pprint(elab_metadata)

    # run validation code on API pull
    def __validate(self):
        with open("elab_metadata", "r") as read_file:
            elab_metadata = json.load(read_file)

        allPass = True
        for row in elab_metadata:

            if not validation.is_pt_id_valid(row):
                allPass = False

            if not validation.is_mrn_valid(row):
                allPass = False

            if not validation.is_surgery_id_valid(row):
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
                allPass = False

            if not validation.is_scrna_igo_sub_id_valid(row):
                allPass = False

            if not validation.is_scrna_rex_id_valid(row):
                allPass = False

            if not validation.is_qc_checks_valid(row):
                allPass = False

            if not validation.is_dlp_rex_id_valid(row):
                allPass = False

            if not validation.is_bccrc_dlp_sample_id_valid(row):
                allPass = False

            if not validation.is_wgs_tissue_type_valid(row):
                allPass = False

            if not validation.is_ppbc_acc_num_valid(row):
                allPass = False

            if not validation.is_ppbc_bank_num_valid(row):
                allPass = False

            if not validation.is_wgs_igo_id_valid(row):
                allPass = False

            if not validation.is_wgs_igo_submission_id_valid(row):
                allPass = False

            if not validation.is_wgs_rex_id_valid(row):
                allPass = False

            if not validation.is_if_tissue_type_valid(row):
                allPass = False

        if allPass == False:
            sys.exit(1)

    # filter out metadata fields with blanks and patients excluded from study
    def filter(self):
        with open("elab_metadata", "r") as read_file:
            elab_metadata = json.load(read_file)

        meta_noBlanks = []
        meta_onStudy = []

        for row in elab_metadata:

            if elab_metadata[row.values()] != "":
                elab_metadata[row['key']] = row['value']

            meta_noBlanks.append(elab_metadata)

            if meta_noBlanks[row["Excluded"]] == "No":
                meta_onStudy.append(elab_metadata)

    # remove all meta data fields without values
    # for meta in sample_meta['data']:
    #     if ('value' in meta.keys()) and (meta['value'] != ""):
    #         data[meta['key']] = meta['value']
    #
    # elab_sample_data.append(data)

    # filter sample meta data for patients/sites we have scRNA seq data
    # for sample_metadata in elab_sample_data:
    #     if 'QC Checks' in sample_metadata.keys():
    #         if sample_metadata['Excluded'] == "No":
    #             filtered_elab_sample_data.append(sample_metadata)

    # break  # just collect 1 since it takes time to collect all

    def extract_hne_table(self):
        '''
        Extract GYN Pathology table from REDCap.
        '''

        hne_metadata = []

        for ii in range(1,73):  # patients 1-72
            data = {
                'token': default_config.get_redcap_token(instance_name="production"),
                'content': 'record',
                'format': 'json',
                'type': 'flat',
                'records[0]': 'SPECTRUM-OV-0'+str("{:02d}".format(ii)),
                'fields[0]': 'patient_id',
                'forms[1]': 'gyn_pathology',
                'events[0]': 'tissue_collection_arm_1',
                'rawOrLabel': 'raw',
                'rawOrLabelHeaders': 'raw',
                'exportCheckboxLabel': 'false',
                'exportSurveyFields': 'false',
                'exportDataAccessGroups': 'false',
                'returnFormat': 'json'
            }


            response = requests.post(url=default_config.get_redcap_api_url(), data=data)
            path_metadata = response.json()

            # filter metadata for samples with values
            for meta in path_metadata:
                filtered_meta = {}
                for k, v in meta.items():
                    if v != "":
                        filtered_meta[k] = v
                hne_metadata.append(filtered_meta)

            pp.pprint("got patient "+str(ii))

        # export filtered metadata as a json file
        with open("hne_metadata", 'w') as outfile:
            jstr = json.dumps(hne_metadata, sort_keys=True,
                              indent=2, separators=(',', ': '))
            outfile.write(jstr)


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

    Integration()