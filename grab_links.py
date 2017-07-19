# Script to obtain all the links (href) from a specific webpage

from bs4 import BeautifulSoup
import requests
import sys
import  pandas

# Ask url to the user and run BeautifoulSoup
url=input('Type the url you would like to search: ')
web=requests.get(url).text    #get webpage html
soup=BeautifulSoup(web,'html.parser')   #apply BeautifuoulSoup function

# Find all the links in the page / html
# Each link can be found in href of '<a href=... /a>'
links_list=list()
for x in soup.find_all('a'):
    links_list.append(x.get('href'))

# Print the list of links on screen
for x in links_list:
    print(x)

# Option to save the list as a csv file
while True:
    ask=input('Would you like to save the links in a csv file? Save to links_list.csv (y) or Exit (n). ')
    if ask=='y':
        df=pandas.DataFrame(links_list,columns=['Links'])
        df.to_csv('links_list.csv',index=False)  #save to csv without index column
        sys.exit(0)
    elif ask=='n':
        sys.exit(0)
    else:
        continue
