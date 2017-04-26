"""
This file contains methods of eksimsi.
"""
import requests
from bs4 import BeautifulSoup

from .models import Subject, Entry


def time_string_to_time_objects(date_string):
    from datetime import datetime

    start_datetime = None
    end_datetime = None

    if len(date_string) == 16:  # "19.04.2015 13:05"
        start_datetime = datetime.strptime(date_string, '%d.%m.%Y %H:%M')

    elif len(date_string) == 10:  # "15.02.1999"
        start_datetime = datetime.strptime(date_string, '%d.%m.%Y')

    elif len(date_string) == 24:  # "19.09.2014 15:13 ~ 20:31"
        start_datetime_string = date_string[:16]
        end_datetime_string = date_string[:11] + date_string[-5:]

        start_datetime = datetime.strptime(start_datetime_string, '%d.%m.%Y %H:%M')
        end_datetime = datetime.strptime(end_datetime_string, '%d.%m.%Y %H:%M')

    elif len(date_string) == 29 and date_string[11] == '~':  # "15.02.1999 ~ 05.12.2006 20:20"
        start_datetime_string = date_string[:10]
        end_datetime_string = date_string[-16:]

        start_datetime = datetime.strptime(start_datetime_string, '%d.%m.%Y')
        end_datetime = datetime.strptime(end_datetime_string, '%d.%m.%Y %H:%M')

    elif len(date_string) == 29 and date_string[17] == '~':  # "23.02.2002 23:50 ~ 24.02.2002"
        start_datetime_string = date_string[:16]
        end_datetime_string = date_string[-10:]

        start_datetime = datetime.strptime(start_datetime_string, '%d.%m.%Y %H:%M')
        end_datetime = datetime.strptime(end_datetime_string, '%d.%m.%Y')

    elif len(date_string) == 35:  # "13.06.2001 21:30 ~ 24.05.2006 21:18"
        start_datetime_string = date_string[:16]
        end_datetime_string = date_string[-16:]

        start_datetime = datetime.strptime(start_datetime_string, '%d.%m.%Y %H:%M')
        end_datetime = datetime.strptime(end_datetime_string, '%d.%m.%Y %H:%M')

    return {"start_datetime": start_datetime, "end_datetime": end_datetime}


def make_soup(url):
    from eksimsi.cookie import cookie

    r = requests.get(url, cookies=cookie)
    # r = requests.get(url)
    print("A Request to %s || HTTP %s" % (url, r.status_code))
    if r.status_code == requests.codes.ok:
        r = requests.get(url, cookies=cookie)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    else:
        return None


# Custom Beautiful Soup Methods

def get_page_number(soup):
    """
    It is only in subject page.
    """
    try:
        page_number = int(soup.find("div", {"class": "pager"})["data-pagecount"])
    except TypeError:
        page_number = 1
    return page_number


def get_paginated_subject_url(soup, page_number):
    """
    It is only in subject page.
    Example: https://eksisozluk.com/pena--31782?p=
    """
    path = str(soup.find("a", {"itemprop": "url"})["href"])
    return "https://eksisozluk.com" + path + "?p=" + str(page_number)


def get_subject_title(soup):
    return soup.find("span", {"itemprop": "name"}).text


def get_subject_id(soup):
    return int(soup.find("a", {"itemprop": "url"})["href"].split("--")[1])


def get_ids_in_a_subject_page(soup):
    return [int(id["href"].replace("/entry/", "")) for id in soup.findAll("a", {"class": "entry-date"})]


def get_bodies_in_a_subject_page(soup):
    for br in soup.find_all("br"):
        br.replace_with("\n")

    return [body.text.replace("\r\n    ", "").replace("\r\n  ", "") for body in soup.findAll("div", {"class": "content"})]


def get_authors_in_a_subject_page(soup):
    return [author.text for author in soup.findAll("a", {"class": "entry-author"})]


def get_dates_in_a_subject_page(soup):
    return [time_string_to_time_objects(date.text) for date in soup.findAll("a", {"class": "entry-date"})]


def get_entry_url(id):
    return "https://eksisozluk.com/entry/%s" % str(id)


def create_subject(soup):
    subject, created = Subject.create_or_get(eksi_id=get_subject_id(soup), title=get_subject_title(soup))
    if created:
        subject.save()
    return subject


def get_first_subject_url(soup):
    parameter = soup.find("span", {"itemprop": "name"}).findParent()['href'] # '/teknoloji--31888'
    return "https://eksisozluk.com%s" % parameter


def create_entries_from_a_subject_page(subject, soup):
    ids = get_ids_in_a_subject_page(soup)
    bodys = get_bodies_in_a_subject_page(soup)
    authors = get_authors_in_a_subject_page(soup)
    dates = get_dates_in_a_subject_page(soup)

    for j in range(0, len(ids)):
        try:
            dummy_entry = Entry.get(Entry.eksi_id == ids[j])
            dummy_entry.delete_instance()
            Entry.create(content=bodys[j], start_datetime=dates[j]["start_datetime"], end_datetime=dates[j]["end_datetime"], author=authors[j], subject=subject, eksi_id=ids[j], is_crawled=True)
        except:
            Entry.create(content=bodys[j], start_datetime=dates[j]["start_datetime"], end_datetime=dates[j]["end_datetime"], author=authors[j], subject=subject, eksi_id=ids[j], is_crawled=True)

        print(ids[j])
