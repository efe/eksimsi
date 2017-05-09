from models import Entry

import sys

arg = int(sys.argv[1])


def get_crawled_entry_count():
    return Entry.select().where(Entry.is_crawled == True).count()

if arg == 'counter':
    print(get_crawled_entry_count())
