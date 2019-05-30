'''
Created on May 23, 2019

@author: pashaa@mskcc.org
'''
import re
from typing import List
from openpyxl.worksheet.worksheet import Worksheet

MRN_CELL: str = 'A2'
ID_CELL: str = 'B2'
ID_PATTERN = r"(^SPECTRUM-OV-\d\d\d$)"

class Patient(object):
    '''
    A patient object.
    '''

    patient_sheet: Worksheet
    patient_mrn: int
    patient_id: str

    def __init__(self, patient_sheet: Worksheet):
        '''

        :param patient: a patient pandas dataframe from an excel sheet
        '''

        self.patient_sheet = patient_sheet
        self.validate()


    def validate(self) -> None:
        # patient_mrn
        try:
            self.patient_mrn = int(self.patient_sheet[MRN_CELL].value)
        except ValueError as ex:
            print('%s %s must be an integer in patients tab. %s' %
                  (MRN_CELL, self.patient_sheet[MRN_CELL], ex))

        # patient_id
        id_val = str(self.patient_sheet[ID_CELL].value)

        match = re.match(ID_PATTERN, id_val)

        if match is None:
            print('Invalid format for patient_id "%s" in patients tab. Expecting "%s"' % (id_val, ID_PATTERN))
        else:
            self.patient_id = match.groups()[0]


    def get_mrn(self) -> int:
        return self.patient_mrn

    def get_id(self) -> str:
        return self.patient_id

    def lock_columns(self, columns: List[str]):
        '''
        Locks the specified columns. Sheet is always kept protected.
        :param columns a list of valid column names.
        :return: None
        '''
        pass

    def unlock_columns(self, columns: List[str]):
        '''
        Unlocks the specified columns. Sheet is always kept protected.
        :param columns a list of valid column names.
        :return: None
        '''
        pass

    def lock_cells(self, cells: List[str]) -> None:
        '''
        Locks the specified cells. Sheet is always kept protected.
        :param cells a list of valid cell addresses [column, row]
        :return: None
        '''
        self.patient_sheet = True
        self.patient_sheet.enable()

    def unlock_cells(self, cells: List[str]) -> None:
        '''
        Unlocks the specified cells. Sheet is always kept protected.
        :param cells a list of valid cell addresses [column, row]
        :return: None
        '''
        self.patient_sheet = True
        self.patient_sheet.disable()



