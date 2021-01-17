# Chamoru Site Scrapers

Web scrapers for Chamoru-related websites.

## Index of Sites

These are the sites that are currently scrapable using this code:

- [Chamoru.info](http://www.chamoru.info/)

## Prerequisites

- Python >= 3.X
- Following modules:
  - [progressbar >= 3.53.1](https://pypi.org/project/progressbar2/3.53.1/)
  - [BeautifulSoup >= 4.9.1](https://pypi.org/project/beautifulsoup4/4.9.1/)
  - [requests >= 2.24.0](https://pypi.org/project/requests/2.24.0/)

## Using The Code

There is currently 1 site scrapable with this code.

### Chamoru.info

1. Run `python chamoru_dict_creator.py`. This will establish the dictionary and store the data in a shelf file.
2. To access the dictionary via command-line, run `python access_dict.py`. This will allow you to search the dictionary on the command-line. **Note:** in the current state, your search is case-sensitive, i.e., searching "Håfa" is different than "håfa".
