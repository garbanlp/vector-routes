import logging
import re
from collections import defaultdict
from pathlib import Path

from const import LOCAL_OBSIDIAN_FILES


def _get_mnemo_data(raw_text: str)-> dict:
    title_match = re.search(r"title:(.*)\n", raw_text)
    description_match = re.search(r"description:(.*)\n", raw_text)
    date_creation_match = re.search(r"date-creation:(.*)\n", raw_text)
    content_match = re.search(r'---\n(.*?)\n---', raw_text, re.DOTALL)
    keyword_match = re.search(r'Keywords:\n(.*?)$', raw_text, re.DOTALL)

    assert len(re.findall(r"\n---\n", raw_text)) == 2

    if any(match is None for match in
           [title_match, description_match, date_creation_match, content_match,
            keyword_match]):
        logging.error(f"{raw_text} is incorrect created !!, correct manually ⛏️")

    return {
        'title': title_match.group(1),
        'description': description_match.group(1),
        'date_creation': date_creation_match.group(1),
        'content': content_match.group(1),
        'keywords': [kw.removeprefix('- ').strip() for kw in keyword_match.group(1).split('\n')]
    }


def get_obsidian_data(path_obsidian: Path) -> list[dict]:
    return [_get_mnemo_data(file_md.read_text())for file_md in sorted(path_obsidian.glob('*.md'))]


def get_obsidian_keywords_notes(obsidian_data: list[dict]) -> dict[list[int]]:
    kws_notes = defaultdict(list)
    for id_note, row in enumerate(obsidian_data):
        for kw in row['keywords']:
            kws_notes[kw].append(id_note)
    return kws_notes


if __name__ == '__main__':
    obsidian_data = get_obsidian_data(LOCAL_OBSIDIAN_FILES)
    keywords = get_obsidian_keywords_notes(obsidian_data)
