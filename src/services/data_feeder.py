# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import os

from dotenv import load_dotenv

from ..wrapper import ES


load_dotenv()


def main():
    es: ES = ES(
        cloud_id=os.getenv('ES_CLOUD_ID'),
        api_key=os.getenv('ES_API_KEY'),
    )
    print(es.client)


if __name__ == '__main__':
    main()
