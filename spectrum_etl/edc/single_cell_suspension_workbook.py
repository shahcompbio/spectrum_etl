'''
Created on May 23, 2019

@author: pashaa@mskcc.org
'''
from openpyxl.styles import PatternFill

from openpyxl import load_workbook, styles


# DONE get and set cell color
# DONE get and set worksheet protection state
# TODO read patient tab, check for one new patient entry and store value
# TODO read surgeries tab, check for one new surgery type entry, store value and generate surgery id
# TODO read specimen tab, get one or more specimen sites and counts, store and generate speciment ids
# TODO read generate aliquot ids
# TODO add logs

class SingleCellSuspension():
    '''
    Creates a spreadsheet for the Electronic Data Capture of SPECTRUM single cell suspension data.
    '''

    def __init__(self):
        wb = load_workbook('tests/spectrum_etl/edc/single_cell_suspension.xlsx')

        patient_sheet = wb['patients']


        patient_mrn_cell = patient_sheet['A2']
        patient_id_cell = patient_sheet['B2']

        # print('>>>>>>'+str(patient_mrn_cell.value))
        # print('>>>>>>' + str(patient_id_cell.value))

        surgery_sheet = wb['surgeries']

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


        #### get and set cell color ###

        index = patient_mrn_cell.fill.fgColor.index
        Colors = styles.colors.COLOR_INDEX
        # Colors[index] # for themed colors
        # 00000000 for no fill
        print(">>>>>> cell fill value: "+index)

        patient_mrn_cell.fill = PatternFill("solid", fgColor="CFE7F7")

        index = patient_mrn_cell.fill.fgColor.index
        value = patient_mrn_cell.fill.fgColor.value
        Colors = styles.colors.COLOR_INDEX
        print(">>>>>> cell fill value: " + str(index) + "; " + "; " + str(value))

        wb.save('single_cell_suspension_v1.xlsx')


        ####  get and set worksheet protection state  ###
        ws = patient_sheet
        ws.protection.sheet = True
        ws.protection.enable()
        #ws.protection.disable()

        print(">>>>> sheet protection: "+ str(patient_sheet.protection.sheet))

        wb.save('single_cell_suspension_v1.xlsx')

