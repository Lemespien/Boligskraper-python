"""###  """
import asyncio
import json
# import requests
import time
import selenium.common.exceptions as Selenium_Exceptions
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver import Firefox
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
# from bs4 import BeautifulSoup

opts = Options()
opts.headless = True

assert opts.headless  # Operating in headless mode

file_path = "data_eie.json"
URL = 'https://eie.no/eiendom/til-salgs?free_text=bod%C3%B8&county[]=18'


async def new_browser_shenanigans(link):
    print("task started")
    await asyncio.sleep(0.5)
    data_dict = {}
    try:
        print("creating browser")
        browser = Chrome(executable_path="C:\Cmder\Python\PythonPaths\chromedriver.exe", options=opts)

        print("browser created")
        await asyncio.sleep(0.5)
        browser.get(link)
        await asyncio.sleep(3)
        data_dict["link"] = link
        try:
            image = browser.find_element_by_class_name("EstateSearchResultListItemstyles__StyledListItemImage-zzmpr3-2").get_attribute("src")
            image_1 = "https://dnbeiendom.no/" + image
            data_dict["image"] = image_1
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            address = browser.find_element_by_class_name("EstateSearchResultListItemstyles__StyledListItemStreet-zzmpr3-7 exXJtp").text
            data_dict["address"] = address
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            city = browser.find_element_by_class_name("EstateSearchResultListItemstyles__StyledListItemDistrictCity-zzmpr3-6").text
            data_dict["city"] = city
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            estimate = browser.find_element_by_class_name(
                "EstateSearchResultListItemstyles__StyledListItemPriceHint-zzmpr3-9").find_element_by_class_name("dnb-number__selection dnb-no-focus").text
            data_dict["asking_price"] = estimate
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            total = browser.find_element_by_class_name(
                "EstateSearchResultListItemstyles__StyledDescriptionTextRowPrice-zzmpr3-13").find_element_by_class_name("dnb-number__selection dnb-no-focus").text
            data_dict["total_price"] = total
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            bedrooms = browser.find_element_by_class_name(
                "EstateSearchResultListItemstyles__StyledBedroomsCount-zzmpr3-15").find_element_by_class_name("dnb-number__selection dnb-no-focus").text
            data_dict["bedrooms"] = bedrooms
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            area = browser.find_element_by_class_name(
                "EstateSearchResultListItemstyles__StyledEstateArea-zzmpr3-14").find_element_by_tag_name("b").text
            data_dict["primary_room_size"] = area
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        # title_block = details_section.find_element_by_class_name("title-block")
        # title = title_block.find_element_by_tag_name("h1")
        print("done with page")
    finally:
        browser.close()
        print("browser closed")
    return data_dict


async def get_data_from_element(element, link):
    print("task started")
    await asyncio.sleep(0.5)
    data_dict = {}
    try:
        print("creating browser")
        browser = element
        print("browser created")
        data_dict["link"] = link
        try:
            image = browser.find_element_by_css_selector("figure img").get_attribute("src")
            data_dict["image"] = image
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            address = browser.find_element_by_css_selector(".card__headline").text  # get_attribute("innerHTML")
            data_dict["address"] = address
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            city = browser.find_element_by_css_selector(".card__overline").text  # get_attribute("innerHTML")
            data_dict["city"] = city
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            spans = browser.find_elements_by_css_selector(".card__subline span")
            datas = ["asking_price", "primary_room_size", "bedrooms"]
            index = 0
            for span in spans:
                data = span.text
                if ",-" in data:
                    data = data.replace("kr", "")
                    data = data.replace(",-", "")
                    data = data.replace(" ", "")
                    key = "asking_price"
                elif "soverom" in data:
                    data = data.replace("soverom", "")
                    data = data.replace(" ", "")
                    key = "bedrooms"
                elif "m²" in data:
                    key = "primary_room_size"
                data_dict[key] = data
                index += 1
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        # title_block = details_section.find_element_by_class_name("title-block")
        # title = title_block.find_element_by_tag_name("h1")
        print("done with page")
    finally:
        print("browser closed")
    return data_dict


async def mainstuff():
    try:
        browser = Chrome(executable_path="C:\Cmder\Python\PythonPaths\chromedriver.exe", options=opts)
        browser.get(URL)
        await asyncio.sleep(5)
        with open("properties_dnb.html", "w", encoding="utf8") as f:
            f.write(browser.page_source)

        properties = browser.find_elements_by_css_selector("main div.section__body div.cards a.card")
        print(len(properties))
        if properties:
            with open(file_path, "w", encoding='utf8') as file:
                file.write("{")
                count = 0
                task_dict = {}
                placeholder_count = 0
                try:
                    for advert in properties:
                        advert.location_once_scrolled_into_view
                        if count % 5 == 0:
                            for key in task_dict:
                                print("Waiting for task #{}".format(key))
                                await task_dict[key]
                                result = task_dict[key].result()
                                print("Result: {}".format(task_dict[key].result()))
                                title = f"placeholder_{placeholder_count}"
                                placeholder_count += 1
                                if "address" in result:
                                    title = result["address"]
                                file.write('"{}": {}, \n'.format(title, json.dumps(result, indent=4, ensure_ascii=False)))
                            task_dict = {}
                        link = advert.get_attribute("href")
                        if link:
                            # new_browser = Firefox(options=opts)
                            task_dict[count] = asyncio.create_task(get_data_from_element(advert, link))
                            print("task #{} created".format(count))
                            count += 1
                        else:
                            print("nothing here")
                    for key in task_dict:
                        print("Waiting for task #{}".format(key))
                        await task_dict[key]
                        result = task_dict[key].result()
                        print("Result: {}".format(task_dict[key].result()))
                        title = f"placeholder_{placeholder_count}"
                        placeholder_count += 1
                        if "address" in result:
                            title = result["address"] + "-" + result["asking_price"]
                        file.write('"{}": {}, \n'.format(title, json.dumps(result, indent=4, ensure_ascii=False)))
                except:
                    print("Error happened")
                file.write('"":""}')

    finally:
        browser.close()
        print("browser closed, final")


asyncio.run(mainstuff())
