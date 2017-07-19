#crawling multipel websites using an SQLite database (crawler_database.db)
#take homepages to crawl from the database, find all the links and check keywords

from bs4 import BeautifulSoup      #library to recognize objects in the html code
import requests
import sys
import datetime
import os
import sqlite3 as sq    #library to manage the sql database links.db
import pandas as pd
import urllib.robotparser           #urllib for the robots.txt check

#define function to check robots.txt file (using urllib.robotparser)
#given the homepage, check if a page can be crawled or not
def check_bots(homepage,page):
    url_check=page+'/'
    rp=urllib.robotparser.RobotFileParser()
    url_bots=homepage+'/robots.txt'
    rp.set_url(url_bots)
    rp.read()
    return(rp.can_fetch('*',url_check))

#define the general function to find the keywords
#given page/link and keywords (as string)
def find_keywords(html_code,words):
    words=words.split(', ')
    list_keywords_found=list()
    for word in words:
        if word.lower() in html_code.lower():
            list_keywords_found.append(word)
    return(list_keywords_found)

#define general function that, given a url/page, takes all the 'a' 'href' links from the html code
#it will be used to loop through all the pages of the website, and find all the links
#links found are stored in lists
def find_links(web,domain):
    #used BeautifulSoup to help us recognize 'a' and 'href' from the html code
    soup=BeautifulSoup(web,'html.parser')
    #loop through all the 'a' 'href' to find the links we need
    for x in soup.find_all('a'):
        link=x.get('href')         #from the 'a' get the 'href' where the link is coded
        if link==None:          #not valid links of NoneType are converted into string 'None', to prevent issues
            link='None'
            continue        #if link is None continue to next step of the for loop
        # if the link is an image/pdf add it to links_image_pdf list and continue to the next step of the loop
        if '.' in link:
            if link.rsplit('.', 1)[1].lower() in ['pdf', 'png', 'jpg', 'gif', 'jpeg']:  # if extension is image/pdf
                links_image_pdf.append(link)
                continue  # go to next step in the for loop
        #part of the URL after ? is not considered, it is deleted
        if '?' in link:
            link=link.split('?',1)[0]
        #if the link contains 'http' and domain, it is a valid link that we need (http://www.kession.com)
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
                        requests.get(link_full)       #check if the link works
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


#open the sql file crawler_database.db
#grab the control table as a pandas dataframe, only if CRAWL='x'
conn=sq.connect('crawler_database.db')
c=conn.cursor()
control=pd.read_sql_query("select * from control where CRAWL='x'", conn)   #ARs to crawl as dataframe
AR_links_taken=list()     #list of ARs crawled

#go through the ARs we want to crawl (CRAWL=x)
#for each AR, find links and keywords and write them into the AR's table
for x in range(len(control)):
    company=control['NAME'][x]
    AR_links_taken.append(company)
    print('\n-------------------------------\nCrawling the website of %s.' % (company))
    url=control['HOMEPAGE'][x]
    try:
        web = requests.get(url).text
    except:
        print('Homepage not working (%s)' % (url))
        continue  # if link does not work continue to next step of the for loop
    keywords=control['KEYWORDS'][x]
    domain=control['DOMAIN'][x]
    #create different lists where the links will be stored
    links_list = list()  # links that we will crawl, they make the full website
    links_list.append(url)  #add the url/homepage
    links_repeated = list()  # links that are repeated in links_list
    not_links_list = list()  # links that we are not allowed to crawl
    not_allowed_links = list()  # links that are not part of the website
    checked_pages = list()  # pages from which we have already taken the links 'href'
    links_image_pdf = list()  # valid links that are image or pdf format
    # use the function find_links to find all the links from the homepage
    find_links(web,domain)
    print('\nLinks taken from:', url)
    # starting from the list of valid links found in the homepage,
    # the function find_links is used to loop through all the pages and find other links
    # the pages checked are recorded in checked_links, to avoid checking multiple times the same page
    # the goal is to find all the pages that constitute the entire AR's website
    for page in links_list:
        # double check if we are allowed from the robots.txt
        bots_allowed = check_bots(url, page)  # using check_bots function
        # if allowed, get the page's code as a text
        if bots_allowed is True:
            try:
                web = requests.get(page).text
                find_links(web,domain)  # using the function to find the links in the page
                print('Links taken from:', page)
            except:
                print('Links not taken from:', page)  # if page's url is not working get a message
    # print the lists of links on the screen, it can be used to check if the script works fine
    print('\nList of valid links: ')
    for x in links_list:
        print(x)
    print('\nList of links in image or pdf format. ')
    for x in links_image_pdf:
        print(x)
    print('\nList of links repeated: ')
    for x in links_repeated:
        print(x)
    print('\nList of links that we are not allowed to crawl (see %s/robots.txt). ' % (url))
    for x in not_allowed_links:
        print(x)
    print('\nList of not valid links: ')
    for x in not_links_list:
        print(x)
    #write results in the database
    print("--------------------\nWriting the links in the AR's table (database crawler_database.db).")
    today=datetime.datetime.today()
    now = '%s %s:%s' %(today.date(), today.hour,today.minute)
    #in the AR's table, move the old links to the right to leave space for the new ones
    c.execute("update control set DATE=? where NAME=?", [now, company])  # update date in control
    c.execute("update [%s] set [DATE T-1]=DATE, [LINK T-1]=LINK, [COUNT T-1]=COUNT, [KEYWORDS T-1]=KEYWORDS, [HTML T-1]=HTML " % (company))  # copy first 4 column to the right (T-1)
    c.execute("update [%s] set DATE='', LINK='', COUNT='', KEYWORDS='', HTML='' " % (company))
    old_links=c.execute("select [LINK T-1] from [%s]" %(company)).fetchall()   #old links (list of tuples)
    links_old=[x[0] for x in old_links]         #from list of tuples to simple list
    #write new links into the AR's table
    #for each page/link run the find_keywords function, also the count
    print('Checking the keywords.')
    for link in links_list:
        #write the links in the AR's table
        if link in links_old:    #if page is not new, insert it next to the old crawl
            c.execute("update [%s] set LINK=? where [LINK T-1]=?" %(company), [link,link])
        else:  #if link is a new page, insert a new record in the table
            c.execute("insert into [%s] (LINK) values(?)" %(company), [link])
        c.execute("update [%s] set DATE=?" % (company), [now])  # update date into AR's table
        #find keywords
        try:
            code=requests.get(link).text
        except:
            print('Link %s not working.' %(link))
            message='link not working'
            c.execute('update [%s] set KEYWORDS=? where LINK=?' %(company), [message,link]) #to sql database
            continue
        length_html = len(code)  # count char in the html code
        c.execute("update [%s] set COUNT=? where LINK=?" % (company), [length_html, link])  # count to sql database
        c.execute("update [%s] set HTML=? where LINK=?" % (company), [code, link])  #html code to sql database
        keywords_found = ', '.join(find_keywords(code, keywords))  # run find_keywords function, list of links returned is transformed in a string
        if keywords_found == '':
            print('Checked %s ------------ Keywords not found.' % (link))  # screen message
            c.execute('update [%s] set KEYWORDS=? where LINK=?' % (company), ['', link])  # to sql database
        else:
            print('Checked %s ------------ Keywords found: %s' % (link, keywords_found))  # screen message
            c.execute('update [%s] set KEYWORDS=? where LINK=?' % (company), [keywords_found, link])  # to sql database
    conn.commit() #commit changes to the database
    # print the length of each list
    print('\nNumber of valid links: ', len(links_list))
    print('Number of image/pdf links: ', len(links_image_pdf))
    print('Number of valid links repeated: ', len(links_repeated))
    print('Number of links that we are not allowed to crawl: ', len(not_allowed_links))
    print('Number of not valid links: ', len(not_links_list))

conn.close()  #close the connection

#save changes to 'crawler.xlsx' file
print('-----------------------\nThe script has taken the links of:\n')
for x in AR_links_taken:
    print(x)
print('\n-----------------------\nData saved to crawler_database.db')