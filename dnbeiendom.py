"""###  """
import asyncio
import json
# import requests
import time
import selenium.common.exceptions as Selenium_Exceptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
# from bs4 import BeautifulSoup

opts = Options()
opts.headless = True

assert opts.headless  # Operating in headless mode


async def new_browser_shenanigans(link):
    print("task started")
    await asyncio.sleep(0.5)
    data_dict = {}
    try:
        print("creating browser")
        browser = Firefox(options=opts)
        print("browser created")
        await asyncio.sleep(0.5)
        browser.get(link)
        await asyncio.sleep(3)
        data_dict["link"] = link
        try:
            image = browser.find_element_by_class_name("intro-section").value_of_css_property("background-image")
            image_1 = image.replace('url("', '').replace('")', '')
            data_dict["image"] = image_1
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            zip_code = browser.find_element_by_class_name("zipcode").text
            data_dict["zip_code"] = zip_code
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            city = browser.find_element_by_class_name("city").text
            data_dict["city"] = city
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        # title_block = details_section.find_element_by_class_name("title-block")
        # title = title_block.find_element_by_tag_name("h1")
        data_elements = []
        try:
            details_section = browser.find_element_by_class_name("details-section")
            info_details = details_section.find_elements_by_class_name("info-details")
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            for details in info_details:
                data_elements += details.find_elements_by_class_name("ng-star-inserted")
            for idx, data in enumerate(data_elements):
                text = data.text
                if data.text == "ADRESSE":
                    data_dict["address"] = data_elements[idx+1].text
                elif text == "PRISANTYDNING":
                    price = data_elements[idx+1].text
                    formatted_price = price.replace(" ", "").replace("kr", "")
                    data_dict["asking_price"] = formatted_price
                elif text == "FELLESGJELD":
                    price = data_elements[idx+1].text
                    formatted_price = price.replace(" ", "").replace("kr", "")
                    data_dict["joint_debt"] = formatted_price
                elif text == "OMKOSTNINGER":
                    price = data_elements[idx+1].text
                    formatted_price = price.replace(" ", "").replace("kr", "")
                    data_dict["costs"] = formatted_price
                elif text == "TOTALPRIS *":
                    price = data_elements[idx+2].text
                    formatted_price = price.replace(" ", "").replace("kr", "")
                    data_dict["total_price"] = formatted_price
                elif text == "BOLIGTYPE":
                    data_dict["type"] = data_elements[idx+1].text
                elif text == "SOVEROM":
                    data_dict["bedrooms"] = data_elements[idx+1].text
                elif text == "ROM":
                    data_dict["rooms"] = data_elements[idx+1].text
                elif text == "PRIMÆRROM":
                    data_dict["primary_room_size"] = data_elements[idx+1].text
                elif text == "BRUKSAREA":
                    data_dict["usable_area"] = data_elements[idx+1].text
                elif text == "BYGGEÅR":
                    data_dict["build_year"] = data_elements[idx+1].text
                elif text == "ETASJE":
                    data_dict["floor"] = data_elements[idx+1].text
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
        finally:
            print("done with page")
    finally:
        browser.close()
        print("browser closed")
    return data_dict


async def mainstuff():
    try:
        browser = Firefox(options=opts)
        # browser = Firefox()
        URL = 'https://dnbeiendom.no/bolig/Nordland/Bod%C3%B8/Bod%C3%B8?pbti=0'
        browser.get(URL)
        await asyncio.sleep(5)
        with open("properties_dnb.html", "w", encoding="utf8") as f:
            f.write(browser.page_source)

        properties = browser.find_elements_by_class_name("results-wrap")
        print(len(properties))
        if properties:
            with open("dnbeiendom.json", "w", encoding='utf8') as file:
                file.write("{")
                count = 0
                task_dict = {}
                placeholder_count = 0
                try:
                    for advert in properties:
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
                        link = advert.find_element_by_tag_name('a').get_attribute("href")
                        if link:
                            # new_browser = Firefox(options=opts)
                            task_dict[count] = asyncio.create_task(new_browser_shenanigans(link))
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
                            title = result["address"]
                        file.write('"{}": {}, \n'.format(title, json.dumps(result, indent=4, ensure_ascii=False)))
                except:
                    print("Error happened")
                file.write('"":""}')

    finally:
        browser.close()
        print("browser closed, final")


asyncio.run(mainstuff())


async def test_function(browser):
    print("task started")
    browser.get("https://www.google.com/")
    print(browser)
    print("task completed sleepytime:{}".format(browser))
    return {
        "hello": "world"
    }


async def main_function():
    task_dict = {

    }
    count = 2
    for _ in range(count):
        new_browser = Firefox(options=opts)
        task_dict[new_browser] = asyncio.create_task(test_function(new_browser))
        print("task created #{}".format(new_browser))

    for key in task_dict:
        await task_dict[key]
        print("task #{} done".format(key))
        key.close()

# asyncio.run(main_function())
