# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import xml.etree.ElementTree as ET


# NOTE: IMAGE_EXT: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp")
IMAGE_EXT: tuple[str, ...] = ('png', 'jpeg', 'jpg')


def is_image(filename) -> bool:
    return any(filename.endswith(ext) for ext in IMAGE_EXT)
