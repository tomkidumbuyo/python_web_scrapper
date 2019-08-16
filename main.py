from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import os

# FIRST SCRAPE LYRICS FROM GENIUS
# first go to genius.com and scrape lyrics information from the site


all_links = []
files_path = "files"

def scrap_page(page_url):
    save_page(page_url)
    links = get_page_links(page_url)
    for link in links:
        scrap_page(link)



# read lyrics for the song
def save_page(page_url):

    result = requests.get(page_url)
    html_page = result.content
    soup = BeautifulSoup(html_page)

    print('\n\n\n\n\n\n-------------------------------------------')
    print(page_url)

    curr_dir = page_url.replace(base_url,"")
    curr_dir.replace("\\","/")

    
    folders = curr_dir.split("/")

    folders = list(filter(None, folders))

    print(folders)

    # get file name without extension
    if len(folders):
        file_name_ext = list.pop(folders)
        file_name = file_name_ext.split(".")[0]
        curr_file_path = files_path+curr_dir
    else:
        file_name_ext = "index.php"
        file_name     = "index"
        curr_file_path     = files_path+"index"
    
    print(curr_file_path)
    print(curr_dir)
    print('-------------------------------------------\n\n\n\n\n\n')

    local_dir     = ""

    for folder in folders:
        local_dir += "../"

    directory = os.path.dirname(curr_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    print(directory)

    # convert links to local directories
    for a in soup.findAll('a', attrs={'href': re.compile("^"+base_url)}):
        a['href'] = a['href'].replace(base_url,local_dir)
        #print(a['href'])
            
    # process css files
    for css in soup.find_all('link', attrs={'rel':"stylesheet",'href': re.compile("^"+base_url)}):
        css_file_link = css['href']
        css['href'] = css['href'].replace(base_url,local_dir)
        #print(css['href'])

        split_link = os.path.split(os.path.abspath(css['href']))

        verify_directory(files_path+split_link[0])
        

    # process javascript files
    for script in soup.find_all('script', src=re.compile("^"+base_url)):
        script_file_link = script['href']
        script['href'] = script['href'].replace(base_url,local_dir)
        #print(script['href'])

        split_link = os.path.split(os.path.abspath(script['href']))

        verify_directory(files_path+split_link[0])

    # process images
    for img in soup.find_all('img', src=re.compile("^"+base_url)):
        img_file_link = img['href']
        img['href'] = img['href'].replace(base_url,local_dir)
        split_link = os.path.split(os.path.abspath(img['href']))

        verify_directory(files_path+split_link[0])
        
        #print(img['href'])
        urllib.request.urlretrieve(img_file_link, img['href'])


    with open(curr_file_path+".html", "w", encoding='utf-8') as file:
        file.write(str(soup))

def verify_directory(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# get all links on the site
def get_page_links(page_url):
    global all_links
    result = requests.get(page_url)
    html_page = result.content
    soup = BeautifulSoup(html_page)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^"+base_url)}):
        if link.get('href') not in all_links:
            links.append(link.get('href'))
            all_links.append(link.get('href'))

    return links

def process_css():
    # TODO process css
    return ""


def process_js():
    # TODO process js
    return ""

base_url = r"https://genius.com"
files_path = files_path+"/"+base_url.replace("/","_")+"/"
verify_directory(files_path)
scrap_page(base_url)