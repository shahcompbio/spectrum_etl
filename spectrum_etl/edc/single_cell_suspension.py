'''
Created on May 23, 2019

@author: pashaa@mskcc.org
'''
from abc import ABC
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

class SingleCellSuspension(ABC):
    '''
    Creates a spreadsheet for the Electronic Data Capture of SPECTRUM single cell suspension data.
    '''

    def __init__(self):


        df = pd.read_excel("tests/spectrum_etl/edc/single_cell_suspension.xlsx", sheetname=None)

        print(df)
