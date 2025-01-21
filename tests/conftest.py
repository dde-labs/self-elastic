# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
import os

import pytest
from pathlib import Path
from dotenv import load_dotenv

from src.wrapper import Es


load_dotenv('../.env')


@pytest.fixture(scope='session')
def es() -> Es:
    return Es(
        cloud_id=os.getenv('ES_CLOUD_ID'),
        api_key=os.getenv('ES_API_KEY'),
    )


@pytest.fixture(scope='session')
def test_path() -> Path:
    return Path(__file__).parent
