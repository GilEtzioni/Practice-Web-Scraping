from selenium import webdriver
from selenium.webdriver.common.by import By


# keep Chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach" , True)
driver = webdriver.Chrome(options = chrome_options)
driver.get("https://opensea.io/collection/degods")


# Open a new tab using JavaScript
driver.execute_script("window.open('', '_blank');")

# Switch to the new tab
driver.switch_to.window(driver.window_handles[1])
driver.get("https://example.com")  # Open a new URL in the new tab

# ---------------------------------------------------------------------------------------

# initialize an empty list to store the data
data_string = []      # Taking all the data from the web
data_rarity_rank = [] # Have only the rarity ranks
data_eth_price = []   # Have only the eth price

# split the data_rarity_rank and the data_eth_price, and delete unimportant data
data_prices = []      # e.g: 0.02789
data_coins = []       # e.g: ETH , Bitcoins , Dollars
data_names = []       # e.g: Springfield Punks , Apes
data_rarity = []       # e.g: 1479 , 2095


# find the elemnts
elements = driver.find_elements(By.CLASS_NAME, value = "text-sm")

# take only the wanted data
counter = 0
for element in elements:
    if counter < 27:
        counter += 1
    elif counter < 700:
        data_string.append(element.text)
        counter += 1
    else:
        break

# -----------------------------------------------------------------
# take only the relevant data
def create_vars_for_objects(starting_line, data):
    # tracking variables
    lines_counter = 0

    # loop through the data
    for index in data_string:

        # continue until the starting line
        if starting_line > lines_counter:
            lines_counter += 1

        # take the data
        elif starting_line == lines_counter:
            data.append(index)
            lines_counter += 1

        # take the data
        elif (lines_counter - starting_line) % 6 == 0:
            data.append(index)
            lines_counter += 1

        # continue to the next line
        else:
            lines_counter += 1

# use the functions
create_vars_for_objects(0, data=data_rarity_rank)
create_vars_for_objects(3, data=data_eth_price)

# -----------------------------------------------------------------
# functions that split the data

# find - data_prices
def find_data_prices():
    for my_string in data_eth_price:
        copied_chars = ""

        # Loop through each word
        for char in my_string:
            if char != ' ':
                copied_chars += char
            else:
                data_prices.append(copied_chars)
                break  # Stop the loop when a space is encountered


# find - data_names
def find_data_coins():
    for my_string in data_eth_price:
        found_space = False
        copied_chars = ""

        for char in my_string:
            if found_space:
                copied_chars += char
            elif char == ' ':
                found_space = True

        if copied_chars:
            data_coins.append(copied_chars)


# find - data_rarity
def find_data_rarity():
    for my_string in data_rarity_rank:
        found_hashtag = False
        extracted_chars = ""

        for char in my_string:
            if found_hashtag:
                extracted_chars += char
            elif char == '#':
                found_hashtag = True

        if extracted_chars:
            data_rarity.append(extracted_chars)


# find - data_names
def find_data_names():
    for my_string in data_rarity_rank:
        found_hashtag = False
        extracted_chars = ""

        for char in my_string:
            if char == ' ' and not found_hashtag:
                continue  # Skip spaces before '#'
            elif char == '#':
                found_hashtag = True
                break  # Stop processing after '#'
            else:
                extracted_chars += char

        if extracted_chars:
            data_names.append(extracted_chars)

# use it to start all the above functions
def split_the_important_data():
    find_data_prices()
    find_data_coins()
    find_data_rarity()
    find_data_names()

# use the functions
split_the_important_data()

# -----------------------------------------------------------------

# create the Object card
class Card:
  def __init__(self, price, coin, rarity, names):
    self.price = price
    self.coin = coin
    self.rarity = rarity
    self.names = names

# sum the num of Objects
num_of_objects = len(data_coins)

# create a list to store the Card objects
cards = []

# create Card objects dynamically
for i in range(num_of_objects):
    card = Card(data_prices[i], data_coins[i], data_rarity[i], data_names[i])
    cards.append(card)

print(f"\n{card.names} :\n")
# accessing individual cards
for i, card in enumerate(cards):
    print(f"Card {i+1}: Price= {card.price} {card.coin}, Rarity= {card.rarity}")


driver.quit()