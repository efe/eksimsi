from eksimsi.models import Entry
from eksimsi.utils import get_page_number, make_soup, get_entry_url, create_subject, \
    get_first_subject_url, create_entries_from_a_subject_page, get_paginated_subject_url
import sys

arg = int(sys.argv[1]) # get arg^th non-crawled element.
offset = arg if arg else 0

while Entry.select().where(Entry.is_crawled == False)[offset]:

    try:
        entry_id = Entry.select().where(Entry.is_crawled == False)[offset].eksi_id

        a_entry_soup = make_soup(get_entry_url(entry_id))
        a_entry_soup = '5XX'

        # Walkaround for 5XX (REBASE THIS IN FUTURE)
        if a_entry_soup == '5XX':
            break

        if a_entry_soup:
            subject = create_subject(a_entry_soup)

            create_entries_from_a_subject_page(subject, a_entry_soup)  # breaking loop in entry/3942

            first_subject_page_soup = make_soup(get_first_subject_url(a_entry_soup))

            created_ids = create_entries_from_a_subject_page(subject, first_subject_page_soup)

            page_number = get_page_number(first_subject_page_soup)
            for page_number in range(2, page_number+1):
                url = get_paginated_subject_url(first_subject_page_soup, page_number)
                any_page_soup = make_soup(url)

                created_ids = create_entries_from_a_subject_page(subject, any_page_soup)
        else:
            Entry.get(Entry.eksi_id == entry_id).delete_instance()
    except Exception as e:
        print(e)
        pass

print("Finito!")
