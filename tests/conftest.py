import os

import pytest
from dotenv import load_dotenv

from src.wrapper import Es


load_dotenv('../.env')


@pytest.fixture(scope='session')
def es() -> Es:
    return Es(
        cloud_id=os.getenv('ES_CLOUD_ID'),
        api_key=os.getenv('ES_API_KEY'),
    )
