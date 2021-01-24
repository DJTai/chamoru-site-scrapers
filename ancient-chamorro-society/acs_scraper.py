import json
import logging
import os
import requests
import time
import urllib.request

from bs4 import BeautifulSoup as bs

def main():
    main_url = 'https://ancientchamorrosociety.weebly.com/'
    json_file = 'ancient_chamorro_society.json'
    cwd = os.getcwd()
    
    ## Create JSON of JPEG URLs for future reference
    hrefs = []  # ex: /chapter-1.html
    pages = {}

    r = requests.get(main_url)
    page_text = r.text
    page_soup = bs(page_text, 'html.parser')

    # Get all chapter & init chapter dict
    logging.info("Getting all of the Chapter HTMLs")
    for link in page_soup.find_all('a'):
        if 'chapter' in link.get('href').lower():
            href = link.get('href')[1:]
            hrefs.append(href)  # Don't include /
            key = link.get('href')[1:].split('.')[0]
            pages[key] = {}
            pages[key]['href'] = href
            pages[key]['images'] = []            

    # Create BeautifulSoup objs for all hrefs/chapters
    logging.info("Going through each Chapter HTML and getting image URLs")
    for href in hrefs:
        r = requests.get(main_url + href)
        if r.status_code != 200:
            print("Not 200 for {}".format(href))
            break

        page_text = r.text
        page_soup = bs(page_text, 'html.parser')

        for link in page_soup.find_all('meta'):
            if 'uploads' in link.get('content'):
                key = href.split('.')[0]        # ex: chapter-1, html
                content = link.get('content')   # Should be full URL to img

                if 'orig' not in content:
                    index = content.find('.jpg')    # To split
                    new_content = content[:index]   # up to .jpg
                    new_content += '_orig'          # append _orig
                    new_content += content[index:]  # add .jpg
                    pages[key]['images'].append(new_content)
                else:
                    pages[key]['images'].append(content)

    logging.info("Creating JSON")
    with open(json_file, 'w') as my_file:
        json.dump(pages, my_file, indent=4)

    ## DOWNLOAD IMAGES
    img_dir = 'acs_images'
    img_wd = cwd + '\\acs_images\\'
    logging.info("Creating %s", img_dir)
    os.makedirs(img_dir)

    logging.info("Load JSON")
    with open(json_file, 'r') as myfile:
        data = myfile.read()
    
    loaded_pages = json.loads(data)
    
    logging.info("Downloading JPEGs")
    for key in loaded_pages:    # ex: chapter-1
        os.chdir(img_wd)        # cd cwd\\acs_images\\

        logging.info("Creating dir for %s", key)
        os.makedirs(key)        # mkdir chapter-1
        os.chdir(key)           # cd chapter-1

        logging.info("Going through page %s", key)
        images = loaded_pages[key]['images']
        for i in range(0, len(images)):
            img_name = images[i].split('/')[-1]  # ex: filename_orig.jpg
            img_name = str(i).zfill(3) + '_' + img_name
            
            urllib.request.urlretrieve(images[i], img_name)


if __name__ == "__main__":
    main()