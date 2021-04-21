from RealEstateInfo import RealEstateInfo
import asyncio
from selenium.webdriver.common.keys import Keys
import time


async def special_start(browser):
    cards = browser.find_elements_by_css_selector(".property_card__CardContainer-ddw2fg-0.bWajby")
    body = browser.find_element_by_tag_name("body")
    print("started scrolling")
    for card in cards:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    print("finished scrolling")
    await asyncio.sleep(1)


def special_case(element, data_dict):
    try:
        asking_price = element.find_element_by_css_selector(".price__Container-sc-1jrn8lz-0")
        data_dict["asking_price"] = asking_price.text.split(" - ")[0].replace(".", "").replace(",-", "")
    except:
        print("price not found")
    return data_dict


Privatmegleren = RealEstateInfo(
    "https://privatmegleren.no/kjope-bolig?a=true&c=%5B%7B%22id%22%3A%22Nordland%22%2C%22county%22%3A%22Nordland%22%2C%22locations%22%3A%5B%5D%7D%5D&l=%5B%7B%22id%22%3A%22Bod%C3%B8%22%2C%22county%22%3A%22Nordland%22%2C%22municipalityArea%22%3A%22Bod%C3%B8%22%7D%5D&mb=0&mv=false&p=1&pfv=1000000&ptv=10000000&q=&s=false&sfv=30&show_market_link=false&stv=400",
    "data_privatmegleren.json",
    [
        ["image", "img", "src"],
        ["address", ".property_card__Street-ddw2fg-6"],
        ["city", ".property_card__County-ddw2fg-5.cDtXLi"],
        ["asking_price", ".price__Container-sc-1jrn8lz-0"],
        ["primary_room_size", ".area__Container-sc-1y218oz-0"],
    ],
    ".property_card__CardContainer-ddw2fg-0.bWajby",
    special_start=special_start,
    special_case=special_case
)
