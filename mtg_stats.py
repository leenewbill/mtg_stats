from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import re

# Program variables
debug = False                        # set to True to print debug data
driver_timeout = 100                 # seconds to wait for webpages containing JavaScript to load
cardlist_filename = "cardlist.txt"   # input file containing list of cards to be processed
csv_writer_filename = "mtg_out.csv"  # output file for writing CSV data

# Configure Chrome webdriver for headless operation (webpages not generated on the screen)
options = Options()
options.headless = True
driver = webdriver.Chrome(options = options, executable_path = "./chromedriver")

# Read cardlist (one MTG card entry per line) for processing
with open(cardlist_filename, "r") as cardlist_file:
    cardlist = cardlist_file.read().splitlines()

if debug:
    print(cardlist)

# Create an empty list to store our card data
cards = []

# Iterate through each card in the card list, collect useful data about each card, and store
#       that data in a list
for card in cardlist:
    print("Processing:", card)

    # Tokens will all have either a "(" or a "[". We will not process them.
    if "(" in card or "[" in card:
        cards.append([card, "TOKEN", "TOKEN", "TOKEN"])
    else:
        # Generate an EDHREC URL from the card name
        url = card
        url = re.sub(" \/\/ ", "-", url)
        url = re.sub(" ", "-", url)
        url = re.sub("'", "", url)
        url = re.sub(",", "", url)
        url = re.sub('"', "", url)
        url = "http://www.edhrec.com/cards/" + url.lower()

        # Use the Chrome webdriver with Selenium to open the webpage
        driver.get(url)

        # Use Selenium to wait for the JavaScript code from EDHREC to generate the HTML we are 
        #       looking for. If we time out, create an output entry for the card and throw an 
        #       error. If the data is found, then continue processing the card.
        try:
            WebDriverWait(driver, driver_timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 
                    "card__label")))
        except:
            cards.append([card, "ERROR", "ERROR", "ERROR"])
            print("ERROR: WebDriverWait_timeout")
        else:
            # Use BeautifulSoup to grab the webpage source
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find the HTML tag that contains data we want
            find_div = soup.find('div', class_="card__label")
            
            # Search for the number of EDHREC decks that use the card. The ".text" ignores the
            #       HTML tag and just searches the content to be displayed on then screen.
            decks_search = re.search(r'In (\d+) decks', find_div.text)

            # If we found the data, copy it; otherwise, throw an error
            if decks_search:
                decks = decks_search.group(1)
            else:
                decks = "ERROR"
                print("ERROR: decks_search")

            # Find the HTML tag that contains the data we want
            find_div = soup.find('div', class_="card__price-border-crop")

            # Search for the TCG price that's listed on EDHREC. (I'm unsure how this price is
            #       calculated, so let's also go get the market price for the card from TCG.)
            edhrec_tcg_price_search = re.search(r'\$.+(\$\d+\.\d\d)', find_div.text)

            # If we found the data, copy it; otherwise, throw an error
            if edhrec_tcg_price_search:
                edhrec_tcg_price = edhrec_tcg_price_search.group(1)
            else:
                edhrec_tcg_price = "ERROR"
                print("ERROR: edhrec_tcg_price_search")

            # Search for the TCG URL on the card's EDHREC page. Since the data we want is inside
            #       the HTML tag, we need to search the HTML as a string.
            tcg_url_search = re.search(r'(https:\/\/store\.tcgplayer\.com.+?)\?', str(find_div))

            # If we did NOT find the data, throw an error; otherwise, copy it and continue processing
            if not tcg_url_search:
                tcg_url = "ERROR"
                tcg_market = "ERROR"
                print("ERROR: tcg_url_search")
            else:
                tcg_url = tcg_url_search.group(1)
                
                # Use the Chrome webdriver with Selenium to open the webpage
                driver.get(tcg_url)

                # Use BeautifulSoup to grab the webpage source
                soup = BeautifulSoup(driver.page_source, "html.parser")

                # Find the HTML tag that contains the data we want
                find_div = soup.find('div', class_="price-point--market")

                # Search for the card's market price
                tcg_market_search = re.search(r'Normal\s+(\$\d+\.\d\d)', find_div.text)

                # If we found the data, copy it; otherwise throw an error
                if tcg_market_search:
                    tcg_market = tcg_market_search.group(1)
                else:
                    tcg_market = "ERROR"
                    print("ERROR: tcg_market_search")

            # Add the card and the data we collected for it to the master list
            cards.append([card, decks, edhrec_tcg_price, tcg_market])
            
if debug:
    print(cards)
        
# Write the card data to a file in CSV format, which can be imported into a spreadsheet
with open(csv_writer_filename, "w", newline = '') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter = ',', quotechar = "\"",
            quoting = csv.QUOTE_MINIMAL)

    # Write each card as a separate line
    for card in cards:
        csv_writer.writerow(card)

# Close the webdriver
driver.quit()
