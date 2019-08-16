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
    print(page_url)
    save_page(page_url)
    links = get_page_links(page_url)
    for link in links:
        scrap_page(link)



# read lyrics for the song
def save_page(page_url):

    result = requests.get(page_url)
    html_page = result.content
    soup = BeautifulSoup(html_page)


    curr_dir = page_url.replace(base_url,"")
    curr_dir.replace("\\","/")

    
    folders = curr_dir.split("/")

    folders = list(filter(None, folders))

 

    # get file name without extension
    if len(folders):
        file_name_ext = list.pop(folders)
        file_name = file_name_ext.split(".")[0]
        curr_file_path = files_path+curr_dir.rstrip('/')
    else:
        file_name_ext = "index.php"
        file_name     = "index"
        curr_file_path     = files_path+"index"
    
   

    local_dir     = ""

    for folder in folders:
        local_dir += "../"

    directory = os.path.dirname(curr_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


    # convert links to local directories
    for a in soup.findAll('a', attrs={'href': re.compile("^"+base_url)}):
        a['href'] = a['href'].replace(base_url,local_dir)
        #print(a['href'])
            
    # process css files
    for css in soup.find_all('link', attrs={'rel':"stylesheet",'href': re.compile("^"+base_url)}):
        css_file_link = css['href']
        css['href'] = css['href'].replace(base_url,local_dir)
        print(css['href'])

        split_link = os.path.split(os.path.abspath(css['href']))

        verify_directory(files_path+split_link[0])
        

    # process javascript files
    for script in soup.find_all('script', src=re.compile("^"+base_url)):
        script_file_link = script['href']
        script['href'] = script['href'].replace(base_url,local_dir)
        print(script['href'])

        split_link = os.path.split(os.path.abspath(script['href']))

        verify_directory(files_path+split_link[0])

    # process images
    for img in soup.find_all('img', src=re.compile("^"+base_url)):
        img_file_link = img['href']
        img['href'] = img['href'].replace(base_url,local_dir)
        split_link = os.path.split(os.path.abspath(img['href']))

        verify_directory(files_path+split_link[0])
        
        print(img['href'])
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
        link['href'] = link.get('href').split("#")[0]
        if link.get('href') not in all_links:
            links.append(link.get('href'))
            all_links.append(link.get('href'))
    
    for link in soup.findAll('a'):
        if link.get('href'):
            link['href'] = link.get('href').split("#")[0]
            if "http" not in link.get('href') and "www." not in link.get('href'):
                curr_url_local = page_url
                link_segments = link.get('href').split("/")
                for link_segment in link_segments:
                    if link_segment == "..":
                        a = curr_url_local.split("/")
                        a.pop()
                        curr_url_local = "/".join(a)
                if curr_url_local not in all_links:
                    links.append(curr_url_local+link.get('href').replace("..","").replace("//","/"))
                    all_links.append(curr_url_local+link.get('href').replace("..","").replace("//","/"))
            
            


    return links

def process_css(url):
    # TODO process css
    return ""


def process_js(url):
    # TODO process js
    return ""

base_url = r"https://dashboard.zawiastudio.com/"
files_path = files_path+"/"+base_url.replace("/","_")+"/"
verify_directory(files_path)
scrap_page(base_url)