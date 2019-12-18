from elasticsearch import Elasticsearch
from elasticsearch import helpers

import types


class ElasticsearchClient():

    __DEFAULT_SETTINGS = {
        "settings": {
            "index": {
                "max_result_window": 50000
            }
        }
    }

    __DEFAULT_MAPPING = {
        'mappings': {
            "_doc": {
                "dynamic_templates": [
                        {
                            "string_values": {
                                "match": "*",
                                "match_mapping_type": "string",
                                "mapping": {
                                    "type": "keyword"
                                }
                            }
                        }
                ]
            }
        }
    }

    # TODO: host + port variables

    def __init__(self, host='localhost', port=9200):
        es = Elasticsearch(hosts=[{'host': host, 'port': port}])

        self.es = es

    # TODO: add settings
    def create_index(self, index, mapping=None):

        if mapping:
            self.es.indices.create(
                index=index,
                body={**self.__DEFAULT_SETTINGS, **mapping},
                include_type_name=True
            )
        else:
            self.es.indices.create(
                index=index,
                body={**self.__DEFAULT_SETTINGS, **self.__DEFAULT_MAPPING},
                include_type_name=True
            )

    def is_index_exists(self, index):
        return self.es.indices.exists(index)

    def is_record_exists(self, index, doc_id):
        return self.es.exists(index=index, id=doc_id)

    # ###############################
    # LOADING METHODS

    def create_record_with_id(self, index, doc_id, doc):
        self.es.create(index=index, id=doc_id, body=doc)

    def update_record_by_id(self, index, doc_id, doc):
        self.es.update(index=index, id=doc_id, body=doc)

    def load_record(self, index, record):
        if not self.is_index_exists(index):
            self.create_index(index)

        self.es.index(index=index, doc_type="_doc", body=record)

    def load_in_bulk(self, index, records):
        if not self.is_index_exists(index):
            self.create_index(index)

        if isinstance(records, types.GeneratorType):
            self.load_bulk_parallel(index, records)
        else:
            self.load_bulk(index, records)

    def load_bulk(self, index, records):
        try:
            helpers.bulk(self.es, records, index=index,
                         doc_type="_doc")
        except Exception as e:
            print("ERROR:", e)

    def load_bulk_parallel(self, index, generator):

        for success, info in helpers.parallel_bulk(self.es, generator,
                                                   index=index, doc_type="_doc"):
            if not success:
                print('Doc failed', info)
