# Download EMR data
log <- file(snakemake@log[[1]], open="wt")
sink(log)
sink(log, type="message")

library(RCurl)
library(redcapAPI)
library(REDCapRITS)
library(tidyverse)
library(lubridate)

# Initialize connection with REDCap API
connection <- redcapConnection(
    url = snakemake@params$api_uri,
    token = snakemake@params$api_token # Supply your own API token
    )
# Get the records
records <- exportRecords(
    rcon = connection,
    batch.size = 5 # Number of records to pull per batch
    )
# Get the metadata
metadata <- exportMetaData(
    rcon = connection
    )

parse_field_dates <- function(records, metadata) { 
  ds <- records %>%
    dplyr::mutate_at(
      metadata %>%
        # Only include intersection between field names in schema and records
        dplyr::filter(field_name %in% colnames(records)) %>%
        # Select date fields
        dplyr::filter(text_validation_type_or_show_slider_number == 'date_mdy') %>%
        dplyr::pull(field_name),
      lubridate::ymd
    ) %>%
    dplyr::mutate_at(
      metadata %>%
        # Only include intersection between field names in schema and records
        dplyr::filter(field_name %in% colnames(records)) %>%
        # Select datetime fields
        dplyr::filter(text_validation_type_or_show_slider_number == 'datetime_mdy') %>%
        dplyr::pull(field_name),
      lubridate::ymd_hms
    )
  ds
}

filter_records <- function(records, study_start_date = '2014-01-01') { 
  filter_fields <- list(
    'consents' = 'patient_consent_date',
    'consultations' = 'consult_date',
    'measures' = 'measure_date',
    'treatments' = 'treatment_start_date',
    'laboratory_tests' = 'laboratory_test_date',
    'specimens_ppbc' = 'specimen_ppbc_resection_datetime',
    'pathology_he' = 'he_pathology_acquisition_date',
    'radiology_ct_scans' = 'ct_acquisition_date',
    'radiology_mri_scans' = 'mri_acquisition_date',
    'radiology_pet_scans' = 'pet_acquisition_date',
    'gyn_chemo' = 'gyn_chemo_start_date'
  )

  filter_fields <- unlist(filter_fields)
  filtered_records <- records %>%
    group_by(patient_id) %>%
    dplyr::filter_at(vars(filter_fields), all_vars(as.Date(.) > as.Date(study_start_date) | is.na(.))) %>%
    ungroup()
  
  filtered_records
}

deidentify_records <- function(records, metadata) { 
  # Get list of identifier fields from REDCap schema
  identifiers <- metadata %>% 
    dplyr::filter(identifier == "y") %>% 
    dplyr::pull(field_name)
  
  ds <- records %>%
    group_by(patient_id) %>%
    fill(patient_date_of_birth) %>%
    mutate(anchor_date = patient_date_of_birth + sample(-365:365, 1, replace=TRUE)) %>%
    dplyr::mutate_at(
      metadata %>% 
        # Only include intersection between field names in schema and records
        dplyr::filter(field_name %in% colnames(records)) %>%
        # Select date or datetime fields
        dplyr::filter(text_validation_type_or_show_slider_number %in% c('date_mdy', 'datetime_mdy')) %>%
        dplyr::pull(field_name), 
      .funs = funs(as.Date(.) - unique(as.Date(anchor_date)))
    ) %>%
    ungroup() %>%
    select(-c(identifiers, patient_date_of_birth))
  
  ds
}

records <- parse_field_dates(records, metadata)

ds_id <- REDCapRITS::REDCap_split(
  records, 
  metadata, 
  forms = "all"
  )

ds_id_filtered <- REDCapRITS::REDCap_split(
  filter_records(records), 
  metadata, 
  forms = "all"
)

ds_deid <- REDCapRITS::REDCap_split(
  deidentify_records(records, metadata), 
  metadata, 
  forms = "all"
  )

ds_deid_filtered <- REDCapRITS::REDCap_split(
  deidentify_records(filter_records(records), metadata), 
  metadata, 
  forms = "all"
)

id_map <- ds_id$patients %>%
  dplyr::select(patient_id, patient_mrn)

message("Writing RDS output...")
# saveRDS(ds_id, file = snakemake@output$emr_id)
# saveRDS(ds_id_filtered, file = snakemake@output$emr_id_filtered)
saveRDS(ds_deid, file = snakemake@output$emr_no_id)
saveRDS(ds_deid_filtered, file = snakemake@output$emr_no_id_filtered_rds)
# saveRDS(id_map, file = snakemake@output$emr_id_map_rds)

message("Writing JSON output...")
# write(jsonlite::toJSON(deidentify_records(filter_records(records2), metadata2), dataframe = "rows"), snakemake@output$emr_no_id_filtered_joined_json)
# write(jsonlite::toJSON(ds_deid_filtered, dataframe = "rows"), snakemake@output$emr_no_id_filtered_split_json)
# readr::write_csv(ds_deid_filtered$radiology_ct_scans, gzfile(snakemake@output$emr_radiology))

message("Finished.\n")
