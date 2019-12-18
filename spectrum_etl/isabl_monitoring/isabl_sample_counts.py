import isabl_cli
import os

from spectrum_etl.isabl_monitoring.es_utils.elasticsearch import ElasticsearchClient

os.environ["ISABL_API_URL"] = 'https://isabl.shahlab.ca/api/v1/'
os.environ["ISABL_CLIENT_ID"] = "1"


samples_dict = {}
samples = isabl_cli.get_instances('samples')
samples_dict["total_samples"] = len(samples)
print(samples_dict)

INDEX = 'isabl_monitoring'

MAPPING = {
    "mappings": {
        "sample_type": {
            "dynamic": "strict",
            "properties": {
                "sample_count":  { "type":"integer"},

            }
        }
    }
}

DOC_ID = 'sample_count_id2342452523'

# if elasticsearch index does not exist, create one and add mapping
es_client = ElasticsearchClient()

if not es_client.is_index_exists(INDEX):
    es_client.create_index(INDEX)
    es_client


# if record does not exist create record for sample count
if not es_client.is_record_exists(INDEX, DOC_ID):
    es_client.create_record_with_id(INDEX, DOC_ID, {"sample_count": -1})

# update value of record
es_client.update_record_by_id(INDEX, DOC_ID, {"doc":{"sample_count": len(samples)}})
