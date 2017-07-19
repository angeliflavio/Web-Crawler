# Script to crawl a website and check specific keywords
# The script obtains all the links from the website, starting from the homepage
# Crawl the links / pages and check if the keywords are present

from bs4 import BeautifulSoup      
import requests
import urllib.robotparser          #to check the robots.txt file (links permitted to crawl)
import sys
import datetime

# Ask the homepage of the website, it will be used to find all the other links / pages
# Check if the link is working, if not ask again
while True:
    url=input('Type the homepage you would like to search (http://www.bbc.com): ')
    try:
        web = requests.get(url).text
        break
    except:
        print('The homepage is not working, check it please.')
        pass

# Ask the domain, it will be used to filter the links
# Check if the domain is contained in the url, if not it could be wrong
while True:
    domain=input('Type the domain name of the website (bbc.com): ')
    if domain in url:
        break
    elif domain not in url:
        print('Please double check the domain %s.' %(domain))
        pass

# Create different lists where the links will be stored
links_list=list()           #links that we will crawl, they make the full website
links_list.append(url)
links_repeated=list()       #links that are repeated in links_list
not_links_list=list()       #links that we are not allowed to crawl
not_allowed_links=list()    #links that are not part of the website
checked_pages=list()        #pages from which we have already taken the links 'href'
links_image_pdf=list()      #valid links that are image or pdf format

# Define function to check robots.txt file (using urllib.robotparser)
# Given the homepage, check if a page can be crawled or not
def check_bots(homepage,page):
    url_check=page+'/'
    rp=urllib.robotparser.RobotFileParser()
    url_bots=homepage+'/robots.txt'
    rp.set_url(url_bots)
    rp.read()
    return(rp.can_fetch('*',url_check))

# Define general function that takes all the 'a' 'href' links from html code
# It will be used to loop through all the pages of the website, and find all the links
def find_links():
    #used BeautifulSoup to help us recognize 'a' and 'href' from the html code
    soup=BeautifulSoup(web,'html.parser')
    #loop through all the 'a' 'href' to find the links we need
    for x in soup.find_all('a'):
        link=x.get('href')         #from the 'a' get the 'href' where the link is coded
        if link==None:          #not valid links of NoneType are converted into string 'None', to prevent issues
            link='None'
            continue    #if link is None continue to next step of the for loop
        #if the link is an image/pdf add it to links_image_pdf list and continue to the next step of the loop
        if '.' in link:
            if link.rsplit('.',1)[1].lower() in ['pdf','png','jpg','gif','jpeg']:   #if extension is image/pdf
                links_image_pdf.append(link)
                continue        
        #do not consider the part of the URL after ?, it is deleted
        if '?' in link:
            link=link.split('?',1)[0]
        #if the link contains 'http' and domain, it is a valid link that we need (http://www.bbc.com)
        if 'http' in link:
            if domain in link[0:len(url)+5]:
                #check if the link is already stored in links_list, if not we need it
                if link not in links_list:
                    #check robots.txt file, are we allowed to crawl the link?
                    bots_allowed=check_bots(url,link)
                    if bots_allowed is True:
                        links_list.append(link)
                    elif bots_allowed is False:
                        not_allowed_links.append(link)
                if link in links_list:
                    links_repeated.append(link)
            else:
                not_links_list.append(link)
        #if the link starts with '/', add it to url and check if it works (/about)
        elif link.startswith('/'):
            link_full=url+link
            #check if link_full is already present in link_list, if not we need it
            if link_full not in links_list:
                #check robots file, are we allowed to crawl the link?
                bots_allowed=check_bots(url,link_full)
                if bots_allowed is True:
                    try:
                        requests.get(link_full)
                        links_list.append(link_full)
                    except:
                        not_links_list.append(link)
                elif bots_allowed is False:
                    not_allowed_links.append(link_full)
            elif link_full in links_list:
                links_repeated.append(link_full)
        #if the link does not fall in the above cases, it is not a valid link (#)
        else:
            not_links_list.append(link)

# Use the function find_links to find all the links from the homepage
find_links()
print('\nLinks taken from:', url)

# Starting from the list of valid links found in the homepage,
# the function find_links is used to loop through all the pages and find other links,
# the pages checked are recorded in checked_links, to avoid checking multiple times the same page
# The goal is to find all the pages that constitute the entire website
for page in links_list:    
    bots_allowed=check_bots(url, page)       #double check if we are allowed from the robots.txt
    if bots_allowed is True:
        try:
            web=requests.get(page).text
            find_links()                    
            print('Links taken from:', page)
        except:
            print('Links not taken from:', page)

# Print the different lists of links
print('\nList of valid links: ')
for x in links_list:
    print(x)
print('\nList of links in image or pdf format. ')
for x in links_image_pdf:
    print(x)
print('\nList of links repeated: ')
for x in links_repeated:
    print(x)
print('\nList of links that we are not allowed to crawl (see %s/robots.txt). ' %(url))
for x in not_allowed_links:
    print(x)
print('\nList of not valid links: ')
for x in not_links_list:
    print(x)

# Print the length of each list
print('\nNumber of valid links: ', len(links_list))
print('Number of image/pdf links: ', len(links_image_pdf))
print('Number of valid links repeated: ', len(links_repeated))
print('Number of valid links that we are not allowed to crawl: ', len(not_allowed_links))
print('Number of not valid links: ', len(not_links_list))

# Define function to loop through all the pages in the list of valid links and check if the keywords are present
# Print keyword and relative page where it was found
def find_keywords():
    keywords = input('Type the keywords you would like to search (management, crowdfunding, property): ')
    now=datetime.datetime.today()
    print('Date of crawling is %s' %(now))
    keywords=keywords.split(', ')      #create a list in case the user writes multiple keywords
    keyword_found=False
    for x in links_list:
        try:
            web=requests.get(x).text
            for keyword in keywords:
                if keyword.lower() in web.lower():
                    print('%s -----> %s' %(keyword,x))
                    keyword_found=True
        except:
            print('Not crawled for keywords: ', x)
    if keyword_found is False:
        print('No results found.')

# Ask if the user would like to search keywords, if not exit the program
while True:
    continue_variable=input('Would you like to search keywords on the website (y) or exit (n)? ')
    if continue_variable=='y':
        find_keywords()             
    elif continue_variable=='n':
        sys.exit(1)                 
    elif continue_variable not in ('yn'):
        pass                        
