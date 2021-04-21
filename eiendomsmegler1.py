"""###  """
import asyncio
from Element import Element
from write_to_file import write_to_file
from create_tasks import create_tasks
import json
# import requests
import selenium.common.exceptions as Selenium_Exceptions
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
# from selenium.webdriver import Firefox
# from bs4 import BeautifulSoup

opts = Options()
opts.headless = True

assert opts.headless  # Operating in headless mode

file_path = "data_eiendomsmegler1.json"
URL = "https://www.eiendomsmegler1.no/kjope-bolig?search=bod%C3%B8"

elements_list = [
    ["image", "img", "src"],
    ["building_type", ".unit-type"],
    ["primary_room_size", ".size"],
    ["city", ".city"],
    ["address", ".address"],
]


async def get_data_from_element(element, link):
    data_dict = {}
    print("task started")
    try:
        sold = element.find_element_by_css_selector(".showing-date")
        if sold and "SOLGT" in sold.text:
            return data_dict
    except Selenium_Exceptions.NoSuchElementException as no_element:
        print(no_element)
        print(link)
    data_dict["link"] = link
    Element.element_container = element
    for elements_spesifications in elements_list:
        title, css_selector, *attribute = elements_spesifications
        attribute = attribute[0] if attribute else "text"
        my_element = Element(title, css_selector, attribute)
        try:
            my_element.find_element()
            data_dict[my_element.title] = my_element.get_method()
        except Exception as err:
            print(type(err))
            print(err)
    try:
        data_dict = special_case(element, data_dict)
    except Selenium_Exceptions.NoSuchElementException as no_element:
        print(no_element)
        print(link)

    print("done with page")
    return data_dict


def special_case(element, data_dict):
    asking_price = element.find_element_by_css_selector(".price").text
    asking_price = asking_price.replace("kr", "")
    asking_price = asking_price.replace(" ", "")
    data_dict["asking_price"] = asking_price
    return data_dict


async def special_start(browser):
    load_more_div = browser.find_element_by_css_selector("div.buttons.is-centered")
    print(load_more_div)
    button = load_more_div.find_element_by_tag_name("button")
    while button:
        button.click()
        print("clicked button")
        await asyncio.sleep(1)
        try:
            button = load_more_div.find_element_by_tag_name("button")
        except:
            button = False
    print("no more to load")


async def mainstuff():
    try:
        browser = Chrome(executable_path="C:\Cmder\Python\PythonPaths\chromedriver.exe", options=opts)
        browser.get(URL)
        await asyncio.sleep(5)
        await special_start(browser)
        properties = browser.find_elements_by_class_name("property-card")
        print(len(properties))
        if properties:
            with open(file_path, "w", encoding='utf8') as file:
                file.write("{")
                count = 0
                task_dict = {}
                placeholder_count = 0
                all_keys = []
                try:
                    task_dict, placeholder_count, all_keys = await create_tasks(properties, file, placeholder_count, get_data_from_element, all_keys)
                    placeholder_count, all_keys = await write_to_file(file, task_dict, placeholder_count, all_keys)
                except Exception as err:
                    print(type(err))
                    print(err)
                file.write('"":""}')

    finally:
        browser.close()
        print("browser closed, final")

asyncio.run(mainstuff())
