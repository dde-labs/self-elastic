# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from markitdown import MarkItDown

from src.__types import AnyPathOrNone


def extract_all2markdown(file: str, target: AnyPathOrNone = None) -> None:
    """Extract any file to Markdown format with the simple logic that passing
    file directly to convert method.

    :param file: A file path that want to extract to markdown file format.
    :type file: str
    :param target: A target file path that want to save the markdown content. If
        this value does not pass or set to None, it will print the markdown
        content to the current stdout.
    :type target: AnyPathOrNone (=None)
    """
    markitdown = MarkItDown()
    try:
        result = markitdown.convert(file)

        if target:
            with open(target, mode='w', encoding='utf-8') as f:
                f.write(result.text_content)
        else:
            print(result.text_content[:1000])

        print(f"Successfully converted {file} to {target}")
    except Exception as e:
        print(f"Error converting {file}: {str(e)}")
