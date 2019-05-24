'''
Created on May 23, 2019

@author: pashaa@mskcc.org
'''
from abc import ABC
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

from spectrum_etl.edc.data.patient import Patient

from openpyxl import load_workbook


class SingleCellSuspension(ABC):
    '''
    Creates a spreadsheet for the Electronic Data Capture of SPECTRUM single cell suspension data.
    '''

    def __init__(self):
        wb = load_workbook('tests/spectrum_etl/edc/single_cell_suspension.xlsx')

        patient_sheet = wb.get_sheet_by_name('patients')


        patient_mrn_cell = patient_sheet['A2']
        patient_id_cell = patient_sheet['B2']

        # print('>>>>>>'+str(patient_mrn_cell.value))
        # print('>>>>>>' + str(patient_id_cell.value))

        surgery_sheet = wb.get_sheet_by_name('surgeries')

        surgery_type_cell_range = surgery_sheet['A2':'A10']

        # surgery id is patient_id + surgery_type + autoinc_integer
        for cell_tup in surgery_type_cell_range:
            cell = cell_tup[0]
            if cell.value is not None:
                    print(">>>>>"+str(cell.row))
                    key = 'B'+str(cell.row)
                    surgery_id_cell = surgery_sheet[key]
                    surgery_id_cell.value = 'XXXXX'
            else:
                print(">>" + str(cell.row))


            #print(str(cell[0].value))

        #print(">>>>>" + str(surgery_type_cell_range))
        #print(">>>>>" + str(surgery_id_cell_range))

        # for cell_tup in surgery_type_cell_range:
        #     print(">>>>>" + str(cell_tup[0].value))
        #
        # print("\n\n")
        # for cell_tup in surgery_id_cell_range:
        #     print(">>>>>" + str(cell_tup[0].value))

        wb.save('single_cell_suspension_v1.xlsx')



        # df = pd.read_excel("tests/spectrum_etl/edc/single_cell_suspension.xlsx",
        #                    sheet_name=None,
        #                    index_col=0,
        #                     dtype = {'Name': str, 'Value': str}
        #                    )  # all sheets
        #
        # #self.patient = Patient(df['patient'])
        #
        # print(">>>>"+str(type(df)))
        # #print(">>>>"+str(self.patient.get_id()))
        #
        # # get surgery
        # # get specimens
        # # get aliquots
        #
        # # get surgery type
        # # populate surgery ids
        #
        #
        # # write to new excel sheet
        # writer = pd.ExcelWriter('single_cell_suspension_v1.xlsx', engine='xlsxwriter')
        #
        # # Convert the dataframe to an XlsxWriter Excel object.
        # df.to_excel(writer, sheet_name=None) # all sheets
        #
        # # Close the Pandas Excel writer and output the Excel file.
        # writer.save()
        #
        # # test with pre-existing data
