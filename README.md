# Python Web Crawler

This is a Python Web Crawler created to automatically browse and monitor the content of 
specific websites.

## Web Crawlers


## Algos

The repository contains several versions of crawler, some are very simple and some other 
are more complex because they are programmed to address different goals.

**grab_links** obtains all the links (stored as href in the html code) from a specific url which is typed by the user  

1. input the url of the page from which you would like to grab all the links
2. algo grabs all the links and prints them on screen (the robots.txt is not checked)


**check_bots_file** checks the robots.txt file, where the pages that we are not allowed to crawl are listed. 
For more info go to the link [http://www.robotstxt.org](http://www.robotstxt.org).

1. input the homepage of the website you would like to check/crawl
2. the website's robots file is checked and the content is printed on screen
3. the user can check if a specific page/url can be crawled (input url of the page)
4. algo prints on screen if you are allowed to crawl the page


**crawl_full_website** obtains all the links composing the full website. Given the homepage, the algo finds all the other linked pages.

1. input homepage and domain
2. algo starts from the homepage and grabs all the links to other pages, then it goes on these pages to find other links
3. algo's goal is to find all the pages of the website (external links are not considered)
4. list of valid links found is printed on screen (not valid links are printed for checking)
5. user can search keywords (input keywords)
6. list of pages where the keywords were found is printed on screen

**crawler_excel** crawls multiple websites using Excel (crawler.xlsx) as database

1. list of websites (AR's) to crawl is taken from the Excel file (also the keywords to check), the user can edit the Excel file, deciding websites to crawl and keywords to check
2. for each website (AR), the algo finds all the links/pages composing the entire website and saves them in Excel with: count of characters for the html code, 
keywords found on the page, date of crawling with copy of previous craling to compare the results
3. the results are also printed on screen for double checking
4. algo asks if the user wants to open the Excel file						

**crawler_manual_links** crawls the links that are manually written in links_manual.db (SQLite database) used for websites where the pages can not be found automatically.

1. user writes AR's info in the table "control" of links.db (homepage and keywords to check)
2. user writes manually the website's links in the table of the AR
3. run the algo, which goes through the pages
4. results are written in links.db: date of crawling, count of characters (html code), keywords found
5. results are also printed on screen for double checking


**crawler_sql** crawls multiple websites using SQL database (crawler_database.db)

1. user selects the ARs to crawl and keywords to check in the control table
2. for each ARs, the algo finds all the links/pages to complete the full website
3. the links are saved in the sql database with keywords found, count of characters, html code
4. the results are also printed on screen for double checking 


**compare_pages** compares a page/link in T and T-1 (compare html code)and it is connected to crawler_database.db, where each page's html code is stored. 
It can be used when, in the database, there is a difference between count T and count T-1
  
1. user types name of the company (used to access the table in the sql database)
2. user types link/page to check (used to grab html in T and T-1 from the sql database)
3. the compare function creates compare_pages_table.html (to be be opened in the web browser)


**compare_pages_text** compares a page/link in T and T-1 (compare text) and it is connected to crawler_database.db, where each page's html code is stored. 
The text is extracted from the html code (the extraction is not perfect).  

1. user types name of the company (used to access the table in the sql database)
2. user types link/page to check (used to grab html in T and T-1 from the sql database)
3. BeautidulSoup.get_text is used to extract the text from the html code
4. the compare function creates compare_pages_text.html (to be opened in the web browser)