import bs4
import json
import logging
import requests
import sys
import time

from bs4 import BeautifulSoup as bs
from requests.exceptions import HTTPError


def create_json_from_list(filename, my_list):
    """Creates a JSON file from the supplied list. Logs filename to info.

    Will return None if
    1. Dict is None
    2. File is named incorrectly or isn't a JSON
    3. File exists already

    Args:
        filename (str): Name of file being created.
        my_list (list): List containing the data.
    """

    if my_list == None:
        logging.warning("{} is None".format(my_list))
        return None
    if isinstance(my_list, list) == False:
        logging.warning("{} isn't a list".format(my_list))
        return None

    if '.' not in filename:
        logging.warning("{} isn't named correctly".format(filename))
        return None
    if filename[-5:].lower() != '.json':
        logging.warning("{} isn't a JSON".format(filename))
        return None

    with open(filename, 'w', encoding="utf-8") as my_file:
        json.dump(my_list, my_file, indent=4, ensure_ascii=False)

    logging.info("Created file: {}".format(filename))


def get_ch_and_en(urls):
    """Gets the Chamoru and English versions of the article texts.

    Args:
        urls (str[]): List of URLs to access

    Returns:
        dict[], dict[]: Two lists of dict-objects, Chamoru and English respectively
    """

    base_url = 'https://www.guampdn.com'

    all_ch = []
    all_en = []

    for url in urls:
        article_url = base_url + url

        try:
            new_res = requests.get(article_url)
            new_res.raise_for_status()
        except HTTPError as http_err:
            logging.warning("Bad site at {}\n{}".format(url, http_err))
            continue

        new_soup = bs4.BeautifulSoup(new_res.text, 'html.parser')

        # Check if the article is CH-EN
        ch_title = new_soup.find('title').text
        if new_soup.find('h2') != None:  # English title style 1
            en_title = new_soup.find('h2').text
            if "English" in en_title and new_soup.find('h3', {'class': 'presto-h3'}) != None:  # English title style 2
                en_title = new_soup.find('h3', {'class': 'presto-h3'}).text
        else:
            # Don't add article
            continue

        # Dates are 4:7 or 3:6
        date = '-'.join(url.split('/')[4:7])
        if '202' not in date[0:4] and '201' not in date[0:4]:
            date = '-'.join(url.split('/')[3:6])

        # Set init vals
        ch = {}
        en = {}

        ch['date'], en['date'] = date, date
        ch['article'], en['article'] = [], []
        ch['url'], en['url'] = article_url, article_url

        ch['title'] = ch_title
        en['title'] = en_title

        # Get CH and EN article text
        texts = new_soup.find_all('p', {'class': 'gnt_ar_b_p'})

        i = 0
        # Get Chamoru text first; we assume it's half-half, so go halfway
        while i < len(texts) // 2:
            ch_para = texts[i].text

            if 'More:' in ch_para[:5]:
                i += 1
            elif 'Imel' in ch_para[:4]:
                i += 1
            elif 'English translation:' in ch_para:
                i = len(texts)
            else:
                ch['article'].append(ch_para)
                i += 1

        j = len(texts) // 2
        # Re-check English title
        en_para = texts[j].text

        if 'english' in en_title.lower() and 'translation' in en_title.lower():
            en_title = en_para
            en['title'] = en_title
            j += 1

        # Get English text
        while j < len(texts):
            ch_para = texts[j].text

            if 'Imel' in ch_para[:4]:
                j += 1
            elif 'More:' in ch_para[:5]:
                j += 1
            elif 'English translation:' in ch_para:
                j += 1
            elif 'Email' in ch_para[:5]:  # Marks the end of the article
                j = len(texts)
            else:
                en['article'].append(ch_para)
                j += 1

        all_ch.append(ch)
        all_en.append(en)

    return all_ch, all_en


def get_urls(web_soup, search_term, num):
    """Gets a specified number of URLs that contain the search term in the link's text. Use -1 to get all URLs.

    Args:
        web_soup (BeautifulSoup): BeautifulSoup HTML object.
        search_term (str): Term to search for.
        num (int): Number of URLs to get.

    Returns:
        str[]: List of URLs.
    """

    urls = []

    if num == -1:
        # Get all URLs
        for link in web_soup.find_all('a'):
            if search_term in link.text and '/story/opinion/columnists' in link.get('href'):
                urls.append(link.get('href'))

    elif num > 0:
        # Get a specified number of URLs
        ctr = 0
        for link in web_soup.find_all('a'):
            if search_term in link.text and '/story/opinion/columnists' in link.get('href'):
                ctr += 1
                urls.append(link.get('href'))
                if ctr == num:
                    break

        if len(urls) < num:
            logging.warning("get_urls() did not find %s URLs", str(num))

    else:
        logging.warning("Number supplied is incorrect. Must use -1 for all, or a number greater than 0")
        return None

    logging.info("Returning {} URLs".format(str(len(urls))))
    return urls


def get_single_page(page_url):
    """A type 1 search. Makes a request and returns the HTML text. Won't work for infinite scrolling pages.

    Args:
        page_url (str): URL to request.

    Returns:
        str: HTML of page as a string.
    """

    html_text = None

    try:
        r = requests.get(page_url)
        r.raise_for_status()
    except HTTPError as http_err:
        logging.warning("HTTPError: %s", http_err)
    except Exception as err:
        logging.warning("Error: %s", err)
    else:
        html_text = r.text

    return html_text


def search_pdn_for(term, type):
    """Searches the term on Guam PDN and returns the result as a BeautifulSoup object.

    Args:
        term (str): Search term.
        type (int): -1 for infinite-scrolling, 1 for no-scrolling, 2 for pagination.

    Returns:
        BeautifulSoup: Search result as a parsed HTML document
    """

    search_url = 'https://www.guampdn.com/search/'
    search_url += (term + '/')

    if type == -1:
        # full_page = get_scrolling_page(search_url)
        print("Not implemented")
    elif type == 1:
        full_page = get_single_page(search_url)
    elif type == 2:
        # page_sources = get_paginated_pages(search_url)
        # full_page = ' '.join(page_sources)  # Join so it's ONE string
        print("Not implemented")

    soup_search = bs(full_page, 'html.parser')

    return soup_search


def show_search_menu():
    """Displays the Search Menu to the user"""

    search_term = ""

    done_searching = False
    while not done_searching:

        valid_choice = False
        while not valid_choice:

            # Assume author
            search_term = 'Onedera'
            time.sleep(0.5)

            print("1. Most recent article")
            print("2. Specific number of articles")
            print("3. Return to main menu")
            print()

            menu_choice = input("Select an option: ")
            if menu_choice == "1":
                ch_latest = 'ch_latest.json'
                en_latest = 'en_latest.json'

                single_bso = search_pdn_for(search_term, 1)
                single_url = get_urls(single_bso, search_term, 1)
                single_article_ch, single_article_en = get_ch_and_en(single_url)

                print("Saving files:\n{}\n{}\n".format(ch_latest, en_latest))
                create_json_from_list(ch_latest, single_article_ch)
                create_json_from_list(en_latest, single_article_en)
                time.sleep(0.5)
                valid_choice = True
                done_searching = True

            elif menu_choice == "2":
                num_to_get = input("How many articles? (Leave blank to go back): ")

                if num_to_get == '' or num_to_get == ' ':
                    print("Returning")
                    valid_choice = False

                else:
                    ch_multi = 'ch_multi.json'
                    en_multi = 'en_multi.json'

                    try:
                        int_num = int(num_to_get)
                        print("Getting {} articles".format(int_num))

                        bso = search_pdn_for(search_term, 1)
                        urls = get_urls(bso, search_term, int_num)
                        ch, en = get_ch_and_en(urls)

                        print("Saving files:\n{}\n{}".format(ch_multi, en_multi))
                        create_json_from_list(ch_multi, ch)
                        create_json_from_list(en_multi, en)
                        logging.info("Created files:\n{}\n{}".format(ch_multi, en_multi))
                        print()

                    except ValueError:
                        print("That's not a valid number")
                        time.sleep(0.5)
                        print("Returning to previous screen")
                        print()

                done_searching = True

            elif menu_choice == "3":
                print("Returning")
                valid_choice = True
                done_searching = True

            else:
                print("Invalid choice. Try again")


def show_main_menu():
    """Show main menu to user."""

    done = False

    while not done:
        print("1. Get Siñot Onedera's Articles")
        print("2. Quit")
        print()

        choice = input("Select an option by #: ")

        if choice == "1":  # Search PDN by term
            print("Option 1 Selected\n")
            show_search_menu()
            time.sleep(0.5)

        elif choice == "2":
            print("Saina Ma'åse'")
            done = True

        else:
            print("Invalid option")
            print()
            time.sleep(1.5)


def main():
    """Main function"""
    log_filename = '_pdn_search_scraper.log'
    logging.basicConfig(filename=log_filename,
                        filemode='w',
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(funcName)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    print("Welcome to PDN Search\n")
    show_main_menu()


if __name__ == "__main__":
    if sys.version_info >= (3, ):
        main()
    else:
        logging.error("Unsupported Python version.\nMust be at least Python 3.0")
