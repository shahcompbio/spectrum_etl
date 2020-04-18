'''
Created on March 16, 2020

@author: pashaa@mskcc.org
'''
from spectrum_etl.config import default_config
import pprint
import requests
import json
from spectrum_etl.data_integration.transform import Transformation

pp = pprint.PrettyPrinter(indent=4)

class Integration(object):
    '''
    This is an experimental class for the integration of genomic data and pathology data from eLabInventory
    and REDCap respectively.
    '''

    def __init__(self):
         self.extract_hne_table()
         self.extract_scrna_table()

    def clean_json(self, json_str):
        '''
        Remove all carriage returns from the specified json string.

        :param json_str: json string with \r, \n
        :returns cleaned json string
        '''
        json_str = json_str.replace('\r', '')
        json_str = json_str.replace('\n', '')

        return json_str


    def extract_scrna_table(self, samples=None):
        '''
        Extract SCRNA table from elab.
        '''

        headers = {'Authorization': default_config.get_elab_api_token(), "Host": default_config.get_elab_host_url()}

        # get sample count
        response = requests.get(default_config.get_elab_api_url()+'sampleSeries?$records=1', headers=headers)
        total_records = response.json()['totalRecords']

        # get all sample meta meta data
        page = 0
        samples = []
        while len(samples) != total_records:
            response = requests.get(default_config.get_elab_api_url() + 'sampleSeries?$page='+str(page), headers=headers)
            samples += response.json()['data']
            page += 1

        assert len(samples) == total_records

        # filter by patient subset
        patient_subset = []

        pt_id_list = []
        for ii in range(1,73):  # patients 1 to 72
            id = 'SPECTRUM-OV-0' + str("{:02d}".format(ii))
            pt_id_list.append(id)

        for sample in samples:
            if sample['name'] in pt_id_list:
                patient_subset.append(sample)
                
        pp.pprint("attempting to get data for "+str(len(patient_subset))+" patients...")

        # get all sample meta data
        elab_sample_data = []
        filtered_elab_sample_data = []

        for patient in patient_subset:
            sampleids = patient["sampleIDs"]

            pp.pprint("getting data for patient "+patient['name'])

            for sampleid in sampleids:
                response = requests.get(default_config.get_elab_api_url()+'samples/{sampleid}'.format(sampleid=sampleid), headers=headers)

                # filter sample meta data by Tissue samples only
                if response.json()["sampleType"]["name"] == "Tissue":
                    response = requests.get(default_config.get_elab_api_url() + 'samples/{sampleid}/meta'.format(sampleid=sampleid),headers=headers)
                    sample_meta = response.json()

                    data = {}

                    # remove all meta data fields without values
                    for meta in sample_meta['data']:
                        if ('value' in meta.keys()) and (meta['value'] != ""):
                            data[meta['key']] = meta['value']

                    elab_sample_data.append(data)

        # filter sample meta data for patients/sites we have scRNA seq data
        for sample_metadata in elab_sample_data:
            if 'QC Checks' in sample_metadata.keys():
                if (sample_metadata['Excluded'] == "No") and ((sample_metadata['QC Checks'] == "Passed Library QC,Passed cDNA QC") or (sample_metadata['QC Checks'] == "Passed Library QC, Passed cDNA QC")):
                    filtered_elab_sample_data.append(sample_metadata)

        # break  # just collect 1 since it takes time to collect all

        with open("filtered_elab_sample_data", 'w') as outfile:
            json.dump(filtered_elab_sample_data, outfile)

        # pp.pprint(filtered_elab_sample_data)


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
            json.dump(hne_metadata, outfile)



if __name__ == '__main__':
    #Integration()
    transform = Transformation()
    transform.transform()