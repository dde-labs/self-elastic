from elasticsearch import Elasticsearch, helpers


class Index:
    def __init__(self, client: Elasticsearch, name: str):
        self.client = client
        self.name = name

    def get_mapping(self):
        return self.client.indices.get_mapping(index=self.name)


class ES:
    def __init__(self, cloud_id: str, api_key: str):
        self.client = Elasticsearch(cloud_id=cloud_id, api_key=api_key)

    def indices(self, name: str):
        return self.client.cat.indices(
            index=name,
            v=True,
            s="index",
        )

    def index(self, name: str) -> Index:
        return Index(self.client, name=name)
