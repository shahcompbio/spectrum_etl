'''
Created on March 16, 2020

@author: pashaa@mskcc.org
'''
from spectrum_etl.config import default_config
import pprint
import requests

pp = pprint.PrettyPrinter(indent=4)

class Integration(object):
    '''
    This is an experimental class for the integration of genomic data and pathology data from eLabInventory
    and REDCap respectively.
    '''

    def __init__(self):
        #self.extract_hne_table()
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


    def extract_scrna_table(self, samples3=None):
        '''
        Extract SCRNA table from elab.
        '''

        headers = {'Authorization': default_config.get_elab_api_token(), "Host": default_config.get_elab_host_url()}

        # get sample count
        response = requests.get(default_config.get_elab_api_url()+'samples?$records=1', headers=headers)
        total_records = response.json()['totalRecords']

        # get all sample meta meta data
        page = 0
        samples = []
        while len(samples) != total_records:
            response = requests.get(default_config.get_elab_api_url() + 'samples?$page='+str(page), headers=headers)
            samples += response.json()['data']
            page += 1

        sample_subset = []
        pt_id_list = ["SPECTRUM-OV-002", "SPECTRUM-OV-003", "SPECTRUM-OV-004", "SPECTRUM-OV-006", "SPECTRUM-OV-007"]
        for i in range(0, len(pt_id_list)):
            filtered_pt_id_list = next(item for item in samples if item['name'] == pt_id_list[i] and item["sampleType"]["name"] == "Tissue")
            sample_subset.append(filtered_pt_id_list)

        assert len(samples) == total_records

        # get all sample meta data
        sample_data = []
        for sample in sample_subset:
            sampleid = sample["sampleID"]
            response = requests.get(default_config.get_elab_api_url()+'samples/{sampleid}/meta'.format(sampleid=sampleid), headers=headers)
            sample_meta = response.json()

            data = {}

            for meta in sample_meta['data']:
                if 'value' in meta.keys():
                    data[meta['key']] = meta['value']
                else:
                    data[meta['key']] = 'NONE'

            sample_data.append(data)

            # break  # just collect 1 since it takes time to collect all

        pp.pprint(sample_data)


    def extract_hne_table(self):
        '''
        Extract GYN Pathology table from REDCap.
        '''
        data = {
            'token': default_config.get_redcap_token(instance_name="production"),
            'content': 'record',
            'format': 'json',
            'type': 'flat',
            #'records[0]': 'SPECTRUM-OV-001',
            'records[1]': 'SPECTRUM-OV-002',
            'records[2]': 'SPECTRUM-OV-003',
            'records[3]': 'SPECTRUM-OV-004',
            #'records[4]': 'SPECTRUM-OV-005',
            'records[5]': 'SPECTRUM-OV-006',
            'records[6]': 'SPECTRUM-OV-007',
            #'records[7]': 'SPECTRUM-OV-008',
            #'records[8]': 'SPECTRUM-OV-009',
            #'records[9]': 'SPECTRUM-OV-010',
            #'records[10]': 'SPECTRUM-OV-011',
            #'records[11]': 'SPECTRUM-OV-012',
            #'records[12]': 'SPECTRUM-OV-013',
            #'records[13]': 'SPECTRUM-OV-014',
            #'records[14]': 'SPECTRUM-OV-015',
            #'records[15]': 'SPECTRUM-OV-016',
            #'records[16]': 'SPECTRUM-OV-017',
            #'records[17]': 'SPECTRUM-OV-018',
            #'records[18]': 'SPECTRUM-OV-019',
            #'records[19]': 'SPECTRUM-OV-020',
            #'records[20]': 'SPECTRUM-OV-021',
            #'records[21]': 'SPECTRUM-OV-022',
            #'records[22]': 'SPECTRUM-OV-023',
            #'records[23]': 'SPECTRUM-OV-024',
            #'records[24]': 'SPECTRUM-OV-025',
            #'records[25]': 'SPECTRUM-OV-026',
            #'records[26]': 'SPECTRUM-OV-027',
            #'records[27]': 'SPECTRUM-OV-028',
            #'records[28]': 'SPECTRUM-OV-029',
            #'records[29]': 'SPECTRUM-OV-030',
            #'records[30]': 'SPECTRUM-OV-031',
            #'records[31]': 'SPECTRUM-OV-032',
            #'records[32]': 'SPECTRUM-OV-033',
            #'records[33]': 'SPECTRUM-OV-034',
            #'records[34]': 'SPECTRUM-OV-035',
            #'records[35]': 'SPECTRUM-OV-036',
            #'records[36]': 'SPECTRUM-OV-037',
            #'records[37]': 'SPECTRUM-OV-038',
            #'records[38]': 'SPECTRUM-OV-041',
            #'records[39]': 'SPECTRUM-OV-042',
            #'records[40]': 'SPECTRUM-OV-044',
            #'records[41]': 'SPECTRUM-OV-045',
            #'records[42]': 'SPECTRUM-OV-046',
            #'records[43]': 'SPECTRUM-OV-047',
            #'records[44]': 'SPECTRUM-OV-048',
            #'records[45]': 'SPECTRUM-OV-049',
            #'records[46]': 'SPECTRUM-OV-050',
            #'records[47]': 'SPECTRUM-OV-051',
            #'records[48]': 'SPECTRUM-OV-052',
            #'records[49]': 'SPECTRUM-OV-053',
            #'records[50]': 'SPECTRUM-OV-054',
            #'records[51]': 'SPECTRUM-OV-056',
            #'records[52]': 'SPECTRUM-OV-057',
            #'records[53]': 'SPECTRUM-OV-059',
            #'records[54]': 'SPECTRUM-OV-060',
            #'records[55]': 'SPECTRUM-OV-062',
            #'records[56]': 'SPECTRUM-OV-063',
            #'records[57]': 'SPECTRUM-OV-064',
            #'records[58]': 'SPECTRUM-OV-065',
            #'records[59]': 'SPECTRUM-OV-066',
            #'records[60]': 'SPECTRUM-OV-067',
            #'records[61]': 'SPECTRUM-OV-068',
            #'records[62]': 'SPECTRUM-OV-070',
            #'records[63]': 'SPECTRUM-OV-071',
            #'records[64]': 'SPECTRUM-OV-072',
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

        pp.pprint(response.json())


if __name__ == '__main__':
    Integration()