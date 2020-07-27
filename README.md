# Project: mtg_stats

# Description:
- This Python program reads in a text file containing one Magic the Gathering card per line, then for each card, it scrapes EDHREC.com for the number of decks using the card and TCGPlayer.com for the card's market price. Finally, the script outputs all collected data to a CSV file for importing into a spreadsheet.

# Prerequisites, Dependencies, Installation, & Deployment:
- Python 3 - <https://www.python.org/>: 
- Selenium - <https://pypi.org/project/selenium/>:
- ChromeDriver - <https://sites.google.com/a/chromium.org/chromedriver/downloads>:
- BeautifulSoup - <https://www.crummy.com/software/BeautifulSoup/>:

# Author: Lee Newbill

# References & Acknowledgements: 
- "Learning Python with Raspberry Pi" by Alex Bradbury and Ben Everard: While I didn't use much from this book directly, it definitely got me started learning Python. The book is decently well-written with interesting and useful examples.
- Real Python - <https://realpython.com/beautiful-soup-web-scraper-python/>: This got me started with web scraping using BeautifulSoup.
- Stack Overflow - <https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python>: This helped me understand that I needed to wait for the JavaScript on the EDHREC site to generate the HTML that I was looking for before scraping it.
- Selenium with Python - <https://selenium-python.readthedocs.io/locating-elements.html>: This helped me learn how to use Selenium to search for HTML tags in webpages.
