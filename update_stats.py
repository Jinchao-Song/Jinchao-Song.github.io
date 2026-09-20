"""Refresh Google Scholar's public All-time metrics; keep the last good snapshot on failure."""
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from urllib.request import Request, urlopen

AUTHOR_ID = 'GwY9nlEAAAAJ'
PROFILE_URL = f'https://scholar.google.com/citations?user={AUTHOR_ID}&hl=en'
DESTINATION = Path(__file__).resolve().parent / 'data' / 'metrics.json'


class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return ''.join(child.text() if isinstance(child, Node) else child for child in self.children)

    def find_all(self, predicate):
        if predicate(self):
            yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.find_all(predicate)


class ProfileParser(HTMLParser):
    VOID_TAGS = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def by_id(self, value):
        return next(self.root.find_all(lambda node: node.attrs.get('id') == value), None)


def clean(text):
    return ' '.join(''.join(c for c in text if unicodedata.category(c) != 'Cf').split())


def parse_profile(page):
    parser = ProfileParser()
    parser.feed(page)
    profile_name, table = parser.by_id('gsc_prf_in'), parser.by_id('gsc_rsb_st')
    if profile_name is None or clean(profile_name.text()) != 'Jinchao Song' or table is None:
        raise ValueError('Google Scholar profile unavailable or unrecognized; keeping the previous snapshot.')
    rows = [[clean(cell.text()) for cell in row.find_all(lambda node: node.tag in ('td','th'))]
            for row in table.find_all(lambda node: node.tag == 'tr')]
    if not rows or len(rows[0]) < 2 or rows[0][1] != 'All':
        raise ValueError('Unrecognized metric columns; keeping the previous snapshot.')
    values = {}
    for row in rows[1:]:
        if len(row) < 3 or row[0] not in ('Citations','h-index'):
            continue
        # Read the All column, never the recent-year column.
        if not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+)', row[1]):
            raise ValueError('Invalid metric value; keeping the previous snapshot.')
        values[row[0]] = int(row[1].replace(',', ''))
    return validate_stats({'authorId':AUTHOR_ID, 'name':'Jinchao Song', 'source':'Google Scholar',
                           'citationCount':values.get('Citations'), 'hIndex':values.get('h-index')})


def validate_stats(data):
    if data.get('authorId') != AUTHOR_ID or data.get('name') != 'Jinchao Song' or data.get('source') != 'Google Scholar':
        raise ValueError('Unexpected author record; keeping the previous snapshot.')
    for field in ('citationCount', 'hIndex'):
        if type(data.get(field)) is not int or data[field] < 0:
            raise ValueError(f'Invalid {field}; keeping the previous snapshot.')
    return {key: data[key] for key in ('authorId', 'name', 'citationCount', 'hIndex', 'source')}


def main():
    request = Request(PROFILE_URL, headers={'User-Agent':'Mozilla/5.0', 'Accept-Language':'en-US,en;q=0.9'})
    with urlopen(request, timeout=25) as response:
        snapshot = parse_profile(response.read().decode('utf-8'))
    snapshot['updated'] = datetime.now(timezone.utc).date().isoformat()
    snapshot['url'] = PROFILE_URL
    DESTINATION.parent.mkdir(exist_ok=True)
    temporary = DESTINATION.with_suffix('.tmp')
    temporary.write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8')
    temporary.replace(DESTINATION)
    print(f'Google Scholar All: citations={snapshot["citationCount"]}, h-index={snapshot["hIndex"]}; checked {snapshot["updated"]}')


if __name__ == '__main__':
    main()
