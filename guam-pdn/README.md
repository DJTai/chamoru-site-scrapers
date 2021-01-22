# Guam PDN

Files related to scraping the [Guam PDN](https://www.guampdn.com/).

## Pre-requisites

- Python >= 3.X
- Modules:
  - [BeautifulSoup >= 4.9.1](https://pypi.org/project/beautifulsoup4/4.9.1/)
  - [requests >= 2.24.0](https://pypi.org/project/requests/2.24.0/)

## Using This Scraper

1. Run `python pdn_search_scraper.py`. This will present you with a menu: Select `1` to get Siñot Onedera's articles or `2` to quit.
2. If you select `1`, then you can either get
   1. His most recent article
   2. A specific number of articles. **NOTE:** this number can't be greater than the number of articles found from the returned page, i.e., if the returned search only found 5 articles then you only get 5, even if you requested 20.
