#script to compare a page/html in T and T-1
#user input the page/link and the code in T and T-1 are taken from the SQL database crawler_database.db
import difflib
from bs4 import BeautifulSoup
import requests
import webbrowser
import sys
import sqlite3

#define function to split the html in lines, because the compare_html will be made line by line
def split_html(code):
    code=BeautifulSoup(code,'html.parser').prettify()  #prettify the html code in lines
    return(code.splitlines())

#define function to compare the pages, using difflib
#print the output
def compare_html(url1,url2):
    diff=difflib.HtmlDiff().make_file(url1,url2)
    return(diff)

#access the database crawler_database.db, which has been populated by the script crawler
conn=sqlite3.connect('crawler_database.db')
c=conn.cursor()

#ask the company, it is used to access the right table in the SQL database
#check if company is present in the database
companies=c.execute("select NAME from control").fetchall()
companies=[x[0] for x in companies]    #list of companies from control
while True:
    company = input('Type the company: ')
    if company in companies:
        break
    else:
        print('The company is not on the database.')
        continue

#ask the link/page the user wants to check, it is used to grab the html in T and T-1
links=c.execute("select LINK from [%s]" %(company)).fetchall()
links=[x[0] for x in links]    #list of links from the company's table
while True:
    page = input('Page link: ')
    if page in links:
        break
    else:
        print('The page is not on the database.')
        continue

#take html T and T-1 from SQL databse (from the company's table of links)
#the code is splitted using split_html function
code1=c.execute("select HTML from [%s] where LINK=?" %(company), [page]).fetchall()[0][0]  #html code in T
code1_lines=split_html(code1)   #spit code in lines
code2=c.execute("select [HTML T-1] from [%s] where LINK=?" %(company), [page]).fetchall()[0][0]  #html code in T-1
code2_lines=split_html(code2)   #split code in lines

#run the compare_html function
compare_table=compare_html(code1_lines,code2_lines)
print(compare_table)

#write the compare table in an html file
f=open('compare_pages_table.html','w', encoding='utf-8')
f.write(compare_table)
f.close()

#ask to open the compare_T_T-1.html in the browser
while True:
    ask_open=input('Would you like to open (y) the file compare_pages_table.html showing the results? Otherwise exit (n). ')
    if ask_open=='y':
        webbrowser.open_new('compare_pages_table.html')   #open the comparison report in your browser
        sys.exit(0)
    elif ask_open=='n':
        sys.exit(0)
    else:
        continue