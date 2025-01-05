# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from markitdown import MarkItDown

markitdown = MarkItDown()
result = markitdown.convert(
    "../data/source/[CIO Brief] SCG CIO Old sGINII - Documentation.pdf"
)
print(result.text_content)
