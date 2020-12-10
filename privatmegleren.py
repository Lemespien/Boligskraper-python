import os
import time
import json
import selenium.common.exceptions as Selenium_Exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox

limited = False
limit_count = 10


opts = Options()
opts.headless = True

assert opts.headless  # Operating in headless mode

driver = Firefox(options=opts)

driver.get("https://privatmegleren.no/kjope-bolig?a=true&c=%5B%7B%22id%22%3A%22Nordland%22%2C%22county%22%3A%22Nordland%22%2C%22locations%22%3A%5B%5D%7D%5D&l=%5B%7B%22id%22%3A%22Bod%C3%B8%22%2C%22county%22%3A%22Nordland%22%2C%22municipalityArea%22%3A%22Bod%C3%B8%22%7D%5D&mb=0&mv=false&p=1&pfv=1000000&ptv=10000000&q=bod%C3%B8&s=false&sfv=30&show_market_link=false&stv=400")
print("fetching, 5sec")
time.sleep(3)
results = driver.find_element_by_class_name("search__Results-sc-3j5t4h-15")

if results.is_displayed():
    cards = results.find_elements_by_class_name("property_card__CardContainer-ddw2fg-0")
    if len(cards) > 0:
        print("found stuff")
        data = {}
        count = 0
        print("scrolling to bottom")
        body = driver.find_element_by_tag_name("body")
        for card in cards:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
        print("At the bottom")
        with open("data_privatmegleren.json", "w", encoding='utf8') as f:
            for card in cards:
                if count > limit_count and limited:
                    break
                count += 1
                card_data = {}
                try:
                    if card.find_element_by_class_name("property_card__SoldTag-ddw2fg-10"):
                        print("Card is Sold")
                        continue
                except:
                    print("sold tag not found")
                print("new card \n")

                try:
                    address = card.find_element_by_class_name("property_card__Street-ddw2fg-6")
                    card_data["address"] = address.text
                except:
                    print("address not found")

                try:
                    link = card.find_element_by_tag_name("a")
                    if link:
                        link_value = link.get_attribute("href")
                        card_data["link"] = link_value
                    else:
                        print("no link")
                except:
                    print("link not found")
                try:
                    local_area = card.find_element_by_class_name("property_card__LocArea-ddw2fg-4")
                    card_data["area"] = local_area.text
                except:
                    print("local area not found")
                try:
                    asking_price = card.find_element_by_class_name("price__Container-sc-1jrn8lz-0")
                    card_data["asking_price"] = asking_price.text.split(" - ")[0].replace(".", "").replace(",-", "")
                except:
                    print("price not found")
                try:
                    card_type = card.find_element_by_class_name("property_card__PropertyInfo-ddw2fg-7")
                    print(card_type.text)
                    card_data["type"] = card_type.text.split()[0]
                    try:
                        primary_room_size = card_type.find_element_by_class_name("area__Container-sc-1y218oz-0")
                        print(primary_room_size.text.split()[0])
                        card_data["primary_room_size"] = primary_room_size.text.split()[0].replace("m2", "")
                    except:
                        print("Primary room size not found")
                except:
                    print("type not found")

                try:
                    image = card.find_element_by_tag_name("img")
                    print(f"Image_element= {image}")
                    card_data["image"] = image.get_attribute("src")
                except:
                    print("image not found")
                print(card.text)
                data[card_data["address"]] = card_data
                print("\n card end \n")
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print("failed")

driver.close()
