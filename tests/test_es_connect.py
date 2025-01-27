import os
from elasticsearch import Elasticsearch


def test_direct_connect():
    client = Elasticsearch(
        cloud_id=os.getenv('ES_CLOUD_ID'),
        api_key=os.getenv('ES_API_KEY')
    )
    print(client.cat.health(format='json', v=True))
