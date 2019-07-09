'''
Created on May 30, 2019

@author: pashaa@mskcc.org
'''


from openpyxl.styles import PatternFill, Protection
from openpyxl.worksheet.worksheet import Worksheet
from spectrum_etl.edc.constants import COLOR_PROCESSED
from typing import Tuple, List

TYPE_COL: str = 'A'   # surgery type column
SPECIMEN_COUNT_COL: str = 'B'  # specimen count column
ID_COL: str = 'C'  # surgery id column
ROW_MIN = 2  # row 1 is header and row 2 is first value row
ROW_MAX = 100  # assumption: a maximum of 100 surgeries per patient

TYPE_ENUM = [
    'Diagnostic laparoscopy with biopsies',
    'Primary debulking',
    'Interval debulking']

class Surgeries(object):
    '''
    A surgeries object. Holds information for a list of surgeries.

    Invariants: surgery_type and specimen_count are never changed in the worksheet.
    '''

    surgeries_sheet: Worksheet
    surgeries: Tuple[Tuple[int, str, int]]  # (row_id, surgeries_type, specimen_count)

    def __init__(self, surgeries_sheet: Worksheet):
        '''
        pre-condition:
        :param patient_sheet: a non None patient_sheet
        '''

        self.surgeries_sheet = surgeries_sheet
        self.surgeries = ()
        self.validate()


    def validate(self) -> None:
        '''
        pre-condition: a non None surgeries sheet.
        post-condition: a valid list of surgeries or exception
        '''
        count = 0
        for row in range(ROW_MIN,ROW_MAX):
            type = self.surgeries_sheet[TYPE_COL + str(row)].value

            # specimen count must be integer or None
            try:
                val = self.surgeries_sheet[SPECIMEN_COUNT_COL + str(row)].value

                if val is not None:
                    specimen_count = int(val)
                else:
                    specimen_count = None
            except ValueError as ex:
                raise Exception("Error: In surgeries tab, found an invalid specimen count %s on row %s. %s" %
                                (val, row, ex))

            # zero or both type and specimen_count must be specified (empty rows are allowed)
            if type is None and specimen_count is None: continue

            if type is None and specimen_count is not None:
                raise Exception("Error: In surgeries tab, found a specimen count %s with no surgery type on row %s." %
                                (specimen_count, row))

            if type is not None and specimen_count is None:
                raise Exception("Error: In surgeries tab, found a surgery type %s with no specimen count on row %s." %
                                (type, row))

            if type not in TYPE_ENUM:
                raise Exception("Error: In surgeries tab, an unknown surgery type %s was found on row %s!" %
                                (type, row))

            self.surgeries += ((row, type, specimen_count),)