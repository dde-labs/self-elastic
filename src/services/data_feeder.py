import os

from dotenv import load_dotenv

from ..wrapper import ES


load_dotenv()


def main():
    es = ES(cloud_id=os.getenv('ES_CLOUD_ID'), api_key=os.getenv('ES_API_KEY'))
    print(es.client)


if __name__ == '__main__':
    main()
