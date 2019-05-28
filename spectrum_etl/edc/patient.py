'''
Created on May 23, 2019

@author: pashaa@mskcc.org
'''
from abc import ABC
import pandas as pd

class Patient(ABC):
    '''
    A patient object
    '''

    def __init__(self, patient):
        '''

        :param patient: a patient pandas dataframe from an excel sheet
        '''
        self.patient_mrn = patient['patient_mrn'][0]
        self.patient_id = patient['patient_id'][0]


    def get_mrn(self):
        return self.patient_mrn

    def get_id(self):
        return self.patient_id