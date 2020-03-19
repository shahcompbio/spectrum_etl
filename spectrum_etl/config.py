'''
Created on October 17, 2019

@author: pashaa@mskcc.org
'''

import yaml
import sys

class Config():

    def __init__(self, config_file="config.yaml"):
        self._config_file = config_file


    def _get_config(self):
        '''

        :param config_file: Default config file is config.yaml
        :return: config generator object
        '''
        # read config file
        try:
            stream = open(self._config_file, 'r')
        except IOError as err:
            print("Error: Unable to find a config file with name "+self._config_file+
                  ". Please use config.yaml.template to make a "+self._config_file)
            sys.exit(1)

        config = yaml.load_all(stream, Loader=yaml.FullLoader)

        return config


    def get_redcap_token(self, instance_name=None):
        '''

        :param instance_name: see config.yaml file for instance names
        :return: string token from config file
        '''
        token_list = []
        token = ''

        for doc in self._get_config():
            for key, value in doc.items():
                if key == 'redcap_token_list':
                    token_list = value

        if instance_name is None:
            print("Error: Please specify REDCap instance for which to get token")
            sys.exit(1)

        for token_dict in token_list:
            if instance_name == next(iter(token_dict.keys())):
                token = next(iter(token_dict.values()))
                break

        if token == '':
            print("Error: Token for REDCap instance "+instance_name+" not found in "+self._config_file)
            sys.exit(1)

        return token

    def get_redcap_api_url(self):
        '''
        :return: string representation of url.
        '''
        for doc in self._get_config():
            for key, value in doc.items():
                if key == 'redcap_api_url': return value

        print("Error: REDCap API URL not found in " + self._config_file)
        sys.exit(1)



    def get_elab_api_token(self):
        '''

        :return: string token from config file
        '''
        for doc in self._get_config():
            for key, value in doc.items():
                if key == 'elab_api_token': return value

        print("Error: elab token not found in " + self._config_file)
        sys.exit(1)


    def get_elab_api_url(self):
        '''

        :return: string token from config file
        '''
        for doc in self._get_config():
            for key, value in doc.items():
                if key == 'elab_api_url': return value

        print("Error: elab url not found in " + self._config_file)
        sys.exit(1)




# an instance that reads from the defaul config.yaml file
default_config = Config()

if __name__ == '__main__':
    print(default_config.get_redcap_token(instance_name="production"))
