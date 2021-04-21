"""###  """
import asyncio
from Element import Element
from eiendomsmegler1_init import EiendomsMegler1
from write_to_file import write_to_file
from create_tasks import create_tasks
import json
import selenium.common.exceptions as Selenium_Exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


opts = Options()
opts.headless = True

assert opts.headless  # Operating in headless mode


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
    if EiendomsMegler1.special_case:
        try:
            data_dict = EiendomsMegler1.special_case(element, data_dict)
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)

    print("done with page")
    return data_dict


async def mainstuff():
    try:
        browser = Chrome(executable_path="C:\Cmder\Python\PythonPaths\chromedriver.exe", options=opts)
        browser.get(EiendomsMegler1.url)
        await asyncio.sleep(5)
        if EiendomsMegler1.special_start:
            await EiendomsMegler1.special_start(browser)
        properties = browser.find_elements_by_class_name("property-card")
        print(len(properties))
        if properties:
            with open(EiendomsMegler1.file_name, "w", encoding='utf8') as file:
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
