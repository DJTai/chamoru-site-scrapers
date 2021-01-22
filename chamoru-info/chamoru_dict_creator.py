import csv
import logging
import progressbar
import requests
import shelve

from bs4 import BeautifulSoup as bs
from chamoru_data import ChamoruWord
from requests.exceptions import HTTPError

def get_single_page(page_url):
    """Makes a request and returns the HTML text.

    Args:
        page_url (str): URL to request.

    Returns:
        str: HTML of page as a string.
    """

    html_text = None

    try:
        logging.info("Accessing {}".format(page_url))
        r = requests.get(page_url)
        r.raise_for_status()
        html_text = r.text
    except HTTPError as http_err:
        logging.warning("HTTPError: {}".format(http_err))
    except Exception as err:
        logging.warning("Error: {}".format(err))
    else:
        html_text = r.text

    return html_text

def create_dictionary(shelf_file, url, start, stop):
    """Creates a Dict of ChamoruWord objects.

    Args:
        shelf_file (str): Filename of shelf that stores the resulting Dict.
        url (str): URL being accessed.
        start (int): 1st ID to access.
        stop (int): Last ID to access.
        
    Returns:
        Nothing, but the dictionary is stored in the shelf file supplied.
    """

    ch_dict = {}

    # Progress bar not needed - it just makes it look neat
    with progressbar.ProgressBar(max_value=stop) as bar:

        for i in range(start, stop + 1):
            url_to_access = url + str(i)
            word_html = get_single_page(url_to_access)
            soup_search = bs(word_html, 'html.parser')

            # <trs> elements have the data
            trs = soup_search.find_all('tr')

            word = trs[0].text.split('\n')[2]

            if word not in ch_dict.keys():
                # Create ChamoruWord
                ch_word = ChamoruWord(word)

                ch_word.definition = trs[2].text.split('\n')[2]
                ch_word.pronunciation = trs[1].text.split('\n')[2]
                ch_word.origin = trs[3].text.split('\n')[2]
                
                # Chamoru & English example
                exs = trs[4].text.split('\n')
                if exs[2] != '' and exs[2] != ' ':
                    ch_word.ch_example = exs[2]
                    ch_word.en_example = exs[3]

                # Associate word with ChamoruWord obj
                ch_dict[word] = ch_word

            bar.update(i)

    ch_shelf = shelve.open(shelf_file)
    ch_shelf['dictionary'] = ch_dict
    ch_shelf.close()

def main():
    """Main function"""

    log_filename = '_chamoru_dict_creator.log'
    logging.basicConfig(filename=log_filename,
                        filemode='w',
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    shelf_file = 'chamoru_dictionary.db'

    definition_url = "http://www.chamoru.info/dictionary/display.php?action=view&id="
    id_beg = 1
    id_end = 10211  # Last accessible ID on site

    create_dictionary(shelf_file, definition_url, id_beg, id_end)

if __name__ == "__main__":
    main()
