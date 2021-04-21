"""###  """
import asyncio
from Element import Element
from write_to_file import write_to_file
from create_tasks import create_tasks
import json
import selenium.common.exceptions as Selenium_Exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

opts = Options()
opts.headless = True

assert opts.headless  # Operating in headless mode

file_path = "data_eie.json"
URL = 'https://eie.no/eiendom/til-salgs?free_text=bod%C3%B8&county[]=18'
property_cards_css_selector = "main div.section__body div.cards a.card"

elements_list = [
    ["image", "figure img", "src"],
    ["address", ".card__headline"],
    ["city", ".card__overline"]]


async def get_data_from_element(element, link):
    print("task started")
    data_dict = {}
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
    spans = element.find_elements_by_css_selector(".card__subline span")
    datas = ["asking_price", "primary_room_size", "bedrooms"]
    index = 0
    for span in spans:
        data = span.text
        if ",-" in data:
            data = data.replace("kr", "")
            data = data.replace(",-", "")
            data = data.replace(" ", "")
            key = datas[0]
        elif "soverom" in data:
            data = data.replace("soverom", "")
            data = data.replace(" ", "")
            key = datas[2]
        elif "m²" in data:
            key = datas[1]
        data_dict[key] = data
        index += 1
    return data_dict


async def mainstuff():
    try:
        browser = Chrome(executable_path="C:\Cmder\Python\PythonPaths\chromedriver.exe", options=opts)
        browser.get(URL)
        await asyncio.sleep(5)
        properties = browser.find_elements_by_css_selector(property_cards_css_selector)
        print(len(properties))
        if properties:
            with open(file_path, "w", encoding='utf8') as file:
                file.write("{")
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
