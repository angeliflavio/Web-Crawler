# Script to check the robots.txt file of a website and see if a specific page can be crawled

import urllib.robotparser
import requests
import sys

# Ask the homepage and check if it is working, if not ask again
while True:
    url = input('\nInput homepage: ')
    try:
        requests.get(url)
        break
    except:
        print('Homepage not working, check the URL please.')
        pass

# Define the function to check the robots.txt file, given a generic url / page
def check_robots():
    url_check=input('\nInput the URL / page you would like to check: ')+'/'
    url2=url+'/robots.txt'
    rp=urllib.robotparser.RobotFileParser()
    rp.set_url(url2)
    rp.read()
    allowed=rp.can_fetch('*', url_check)
    if allowed is True:
        print('Yes, you are allowed to crawl %s.' %(url_check))
    elif allowed is False:
        print('No, you are not allowed to crawl %s.' %(url_check))

# Print the content of the robots.txt file
bots_url=url+'/robots.txt'
bots=requests.get(bots_url).text
#if the website has a robots.txt, one of the following three words should be in the text
if ('User-agent' in bots) or ('Disallow' in bots) or ('Sitemap' in bots):
    print('\nThe Robots Exclusion Protocol %s: ' %(bots_url))
    print(bots)
else:
    print('There is no robots.txt for this website.')

# Ask if the user want to check if a specific page can be crawled, otherwise exit
# Run the check_robots function and print the outcome
while True:
    ask_continue=input('\nWould you like to check if a page can be crawled (y) or exit (n)? ')
    if ask_continue=='y':
        check_robots()
    elif ask_continue=='n':
        sys.exit(1)
    elif ask_continue in 'yn':
        pass
