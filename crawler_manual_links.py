#sctipt to check the presence of specific kwywords on the links stored in the file links.db
#links/pages that we want to check are manually stored in links_manual.db
#the result are written in links.db

from bs4 import BeautifulSoup      #library to recognize objects in the html code
import requests
import sys
import datetime
import os
import sqlite3 as sq    #library to manage the sql database links.db
import pandas as pd

#define the general function to find the keywords
#given page/link and keywords (as string)
def find_keywords(page,keywords):
    keywords=keywords.split(', ')
    list_keywords_found=list()
    for word in keywords:
        if word.lower() in page.lower():
            list_keywords_found.append(word)
    return(list_keywords_found)


#open the sql file links.db
#grab the control table as a pandas dataframe
conn=sq.connect('links_manual.db')
c=conn.cursor()
control=pd.read_sql_query("select * from control where CRAWL='x'", conn)   #ARs to crawl

#go through the ARs we want to crawl (CRAWL=x)
#for each AR open their realtive table and take the links
for x in range(len(control)):
    company=control['NAME'][x]
    print('Checking %s.' %(company))
    keywords=control['KEYWORDS'][x]
    #select all the links from the company's table
    links=c.execute('select link from [%s]' %(company)).fetchall()  #result is a list of tuples
    #move coumns Count, Keywords and Date to the right (Count t-1, Keywords t-1, Date t-1)
    c.execute("update [%s] set [COUNT T-1]=COUNT, [KEYWORDS T-1]=KEYWORDS, [DATE T-1]=DATE" %(company))  #move columns 2,3,4 to columns 5,6,7
    c.execute("update [%s] set COUNT='', KEYWORDS='', DATE=''" %(company))  #delete content of columns 2,3,4
    #write date in control and company's table
    today = datetime.datetime.today()
    now = '%s %s:%s' % (today.date(), today.hour, today.minute)
    c.execute("update control set DATE=? where NAME=?", [now, company])
    c.execute("update [%s] set DATE=?" %(company), [now])
    c.execute("update [%s] set COUNT=?" %(company), [''])    #count characters in the html code
    #for each page/link run the find_keywords function
    for Link in links:
        link=Link[0]  #take the link from the list
        try:
            code=requests.get(link).text
            length_html=len(code)     #count
            c.execute("update [%s] set COUNT=?" %(company), [length_html])  #count to sql database
            keywords_found=', '.join(find_keywords(code,keywords))     #run find_keywords
            if keywords_found=='':
                print('Checked %s ------------ Keywords not found.' %(link))    #screen message
                c.execute('update [%s] set KEYWORDS=? where LINK=?' %(company), ['',link])    #to sql database
            else:
                print('Checked %s ------------ Keywords found: %s' %(link, keywords_found)) #screen message
                c.execute('update [%s] set KEYWORDS=? where LINK=?' %(company), [keywords_found,link])  #to sql database
        except:
            print('Link %s not working.' %(link))
            message='link not working'
            c.execute('update [%s] set KEYWORDS=? where LINK=?' %(company), [message,link]) #to sql database
            continue
conn.commit()
conn.close()










