# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from markitdown import MarkItDown


def convert_simple(file: str, target: str) -> None:
    """Convert any file to markdown format with the simple logic that passing
    file directly to convert method.
    """
    markitdown = MarkItDown()
    try:
        result = markitdown.convert(file)
        with open(target, mode='w', encoding='utf-8') as f:
            f.write(result.text_content)
        print(f"Successfully converted {file} to {target}")
    except Exception as e:
        print(f"Error converting {file}: {str(e)}")
