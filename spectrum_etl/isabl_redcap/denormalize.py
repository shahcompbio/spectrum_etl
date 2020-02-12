import pandas as pd
import spectrum_etl.isabl_redcap.denormalize_columns as columns
import pprint
import json

pp = pprint.PrettyPrinter(width=80, compact=True, indent=2)


def get_data(patient_id, instrument, columns, all_data):
    df = all_data.loc[(all_data['patient_id'] == patient_id) & (all_data['redcap_repeat_instrument'] == instrument)]
    instrument_data = {}

    if not df.empty:
        for index, row in df.iterrows():
            for column in columns:
                instrument_data[column] = row[column]

    return instrument_data


def get_patient_redcap_json(patient_id, csv_path):
    all_data = pd.read_csv(csv_path).fillna('')
    data = {}

    # patient info
    patients_data = get_data(patient_id, '', columns.patients, all_data)

    # consent info for patient
    consents_data = get_data(patient_id, 'consents', columns.consents, all_data)

    # sequencing bulk dna info for patient
    seq_bulk_dna_data = get_data(patient_id, 'sequencing_bulk_dna', columns.sequencing_bulk_dna, all_data)

    data['patient']                        = {}
    data['patient']                        = patients_data
    data['patient']['consents']            = consents_data
    data['patient']['sequencing_bulk_dna'] = seq_bulk_dna_data

    # return json.dumps(data)
    return data


if __name__ == "__main__":
    csv_path = r'/Users/havasove/Desktop/15200MSKSPECTRUMOvar_DATA_RAW.csv'
    patient_id = 'SPECTRUM-OV-006'
    pp.pprint(get_patient_redcap_json(patient_id, csv_path))



