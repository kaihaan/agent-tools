""" "
To extract markdwon block from string
"""

import re


def extract_md_blocks(text: str, label: str) -> list:
    """
    Extracts fenced code blocks from markdown text.

    Args:
        text (str): The markdown text from which to extract code blocks.

    Returns:
        list: A list of extracted code blocks, stripped of leading/trailing whitespace.
    """
    pattern = rf"```{label}(?:\w+\s+)?(.*?)```"
    compiled_pattern = re.compile(pattern, re.DOTALL)
    matches = compiled_pattern.findall(text)
    return [block.strip() for block in matches]
