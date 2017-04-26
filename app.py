from eksimsi.models import Entry
from eksimsi.utils import get_page_number, make_soup, get_subject_title, get_entry_url, create_subject, \
    get_first_subject_url, create_entries_from_a_subject_page, get_paginated_subject_url

try:
    while Entry.select().where(Entry.is_crawled == False)[0]:

        entry_id = Entry.select().where(Entry.is_crawled == False)[0].eksi_id

        a_entry_soup = make_soup(get_entry_url(entry_id))
        if a_entry_soup:
            subject = create_subject(a_entry_soup)

            first_subject_page_soup = make_soup(get_first_subject_url(a_entry_soup))

            created_ids = create_entries_from_a_subject_page(subject, first_subject_page_soup)

            page_number = get_page_number(first_subject_page_soup)
            for page_number in range(2, page_number+1):
                url = get_paginated_subject_url(first_subject_page_soup, page_number)
                any_page_soup = make_soup(url)

                created_ids = create_entries_from_a_subject_page(subject, any_page_soup)
        else:
            Entry.get(Entry.eksi_id == entry_id).delete_instance()
except:
    pass

print("Finito!")
