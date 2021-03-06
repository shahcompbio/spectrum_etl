This is an experimental package for the integration of genomic data and pathology data from eLabInventory and REDCap respectively. This task is critical for the multi-modal integration of this data as required by downstream analyses. It is expected that this exercise will reveal many inconsistencies in the data that make the joining of the tables from the two databases challenging. It is proposed that these challenges will be addressed by performing data transformations in order to make it possible to ultimately perform the table joins. In addition, the joined data will be saved in a json format that will allow users to execute sql queries on the data using Apache Drill.

Input: Elab metadata and REDCap metadata access via REST API

Process: Perform any necessary transformations and join tables using pandas

Output: json data formatted for Apache Drill queries.



Apache Drill installation instructions:

pre-requisites -
Java 8

https://drill.apache.org/docs/installing-drill-on-linux-and-mac-os-x/
- add drill to ~/.bash_profile
- source ~/.bash_profile
- sudo chown -R <user>:<group> /opt/apache-drill-1.17.0

- $ drill-embedded
Apache Drill 1.17.0
"Two things are infinite: the universe and Drill; and I'm not sure about the universe."

apache drill> SELECT * FROM dfs.`/Users/pashaa/dev/shahcompbio/spectrum_etl/drill_sample2.json` LIMIT 5;

# flatten data and list all patient ids
apache drill> SELECT t.flatdata.`Patient ID` as `patient id`, t.flatdata.`Specimen Site` as `specimen site` FROM (select flatten(data) AS flatdata FROM dfs.`/Users/limj/Desktop/Rockerfeller_University/Intro_to_Programming/Assignments/JamieLim_FinalProject/project_code/spectrum_etl/output_for_drill.json`) t;

    +-----------------+--------------------------------------------------+
    |   patient id    |                  specimen site                   |
    +-----------------+--------------------------------------------------+
    | SPECTRUM-OV-002 | Infracolic Omentum                               |
    | SPECTRUM-OV-002 | Right Ovary                                      |
    | SPECTRUM-OV-002 | Right Ovary                                      |
    | SPECTRUM-OV-003 | Ascites                                          |
    | SPECTRUM-OV-003 | Infracolic Omentum                               |
    | SPECTRUM-OV-003 | Left Adnexa                                      |
    | SPECTRUM-OV-003 | Left Upper Quadrant                              |
    | SPECTRUM-OV-003 | Pelvic Peritoneum                                |
    | ...                                                                |
    | SPECTRUM-OV-009 | Right Upper Quadrant                             |
    | SPECTRUM-OV-009 | Right Upper Quadrant                             |
    +-----------------+--------------------------------------------------+



# flatten data and list all patient ids for which we have a specimen site = 'Infracolic Omentum'
apache drill> SELECT t.flatdata.`Patient ID` as `Patient ID` FROM (select flatten(data) AS flatdata FROM dfs.`/Users/limj/Desktop/Rockerfeller_University/Intro_to_Programming/Assignments/JamieLim_FinalProject/project_code/spectrum_etl/output_for_drill.json`) t where t.flatdata.`Specimen Site` = 'Infracolic Omentum';

    +-----------------+
    |   Patient ID    |
    +-----------------+
    | SPECTRUM-OV-002 |
    | SPECTRUM-OV-003 |
    | SPECTRUM-OV-007 |
    | SPECTRUM-OV-007 |
    | SPECTRUM-OV-008 |
    | SPECTRUM-OV-008 |
    | SPECTRUM-OV-009 |
    | SPECTRUM-OV-009 |
    +-----------------+

# flatten data and list patient ids and number of specimen sites for all patients that have sample site = 'Infracolic Omentum'
apache drill> SELECT t.flatdata.`Patient ID` as `Patient ID`, count(t.flatdata.`Specimen Site`) as `Specimen Site Count` FROM (select flatten(data) AS flatdata FROM dfs.`/Users/limj/Desktop/Rockerfeller_University/Intro_to_Programming/Assignments/JamieLim_FinalProject/project_code/spectrum_etl/output_for_drill.json`) t where t.flatdata.`Specimen Site` = 'Infracolic Omentum'  GROUP BY `Patient ID`;

    +-----------------+---------------------+
    |   Patient ID    | Specimen Site Count |
    +-----------------+---------------------+
    | SPECTRUM-OV-002 | 1                   |
    | SPECTRUM-OV-003 | 1                   |
    | SPECTRUM-OV-007 | 2                   |
    | SPECTRUM-OV-008 | 2                   |
    | SPECTRUM-OV-009 | 2                   |
    +-----------------+---------------------+

# flatten data and get number of records that have a specimen site and group by patient id
apache drill> SELECT t.flatdata.`Patient ID` as `Patient ID`, count(t.flatdata.`Specimen Site`) as `Specimen Site Count` FROM (select flatten(data) AS flatdata FROM dfs.`/Users/limj/Desktop/Rockerfeller_University/Intro_to_Programming/Assignments/JamieLim_FinalProject/project_code/spectrum_etl/output_for_drill.json`) t GROUP BY `Patient ID`;

    +-----------------+---------------------+
    |   Patient ID    | Specimen Site Count |
    +-----------------+---------------------+
    | SPECTRUM-OV-002 | 3                   |
    | SPECTRUM-OV-003 | 7                   |
    | SPECTRUM-OV-007 | 13                  |
    | SPECTRUM-OV-008 | 6                   |
    | SPECTRUM-OV-009 | 15                  |
    +-----------------+---------------------+

apache drill> !quit


SELECT * FROM dfs.`/Users/pashaa/dev/shahcompbio/spectrum_etl/output_for_drill.json` LIMIT 5;