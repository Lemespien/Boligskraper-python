"""###  """
import asyncio
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


async def new_browser_shenanigans(link, image="", building_type=""):
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
        try:
            data_dict["link"] = link
            data_dict["image"] = image
            data_dict["type"] = building_type
        except:
            print("link or image failed")
        try:
            data_dict["area"] = browser.find_element_by_class_name("prospect__hero-area").text
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)

        try:
            price = browser.find_element_by_class_name("prospect-home__price").text
            formatted_price = price.replace("kr", "").replace(" ", "")
            data_dict["asking_price"] = formatted_price
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)

        try:
            price = browser.find_element_by_class_name("prospect-home__sub-price-element").text
            print(price)
            formatted_price = price.replace("Totalpris", "").replace("kr", "").replace(" ", "")
            data_dict["total_price"] = formatted_price
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)

        try:
            addressText = browser.find_element_by_class_name("prospect__hero-address").text.split("\n")
            address = addressText[0]
            city_zip = addressText[1]
            zip_code = city_zip.split(" ")[0]
            city = city_zip.split(" ")[1]
            data_dict["address"] = address
            data_dict["zip_code"] = zip_code
            data_dict["city"] = city
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        # title_block = details_section.find_element_by_class_name("title-block")
        # title = title_block.find_element_by_tag_name("h1")
        data_elements = []
        info_detail = False
        try:
            details_section = browser.find_element_by_class_name("key-info-outer")
            info_detail = details_section.find_element_by_class_name("key-info")
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            if (info_detail is not False):
                data_elements = info_detail.find_elements_by_tag_name("td")
                for idx, data in enumerate(data_elements):
                    text = data.text.lower()
                    print(text)
                    if data.text == "adresse":
                        data_dict["address"] = data_elements[idx+1].text
                    elif text == "prisantydning":
                        price = data_elements[idx+1].text
                        formatted_price = price.replace(" ", "").replace("kr", "")
                        data_dict["asking_price"] = formatted_price
                    elif text == "fellesgjeld":
                        price = data_elements[idx+1].text
                        formatted_price = price.replace(" ", "").replace("kr", "")
                        data_dict["joint_debt"] = formatted_price
                    elif text == "omkostninger":
                        price = data_elements[idx+1].text
                        formatted_price = price.replace(" ", "").replace("kr", "")
                        data_dict["costs"] = formatted_price
                    elif text == "totalpris *":
                        price = data_elements[idx+2].text
                        formatted_price = price.replace(" ", "").replace("kr", "")
                        data_dict["total_price"] = formatted_price
                    elif text == "boligtype":
                        data_dict["type"] = data_elements[idx+1].text
                    elif text == "soverom":
                        data_dict["bedrooms"] = data_elements[idx+1].text
                    elif text == "rom":
                        data_dict["rooms"] = data_elements[idx+1].text
                    elif text == "primærrom":
                        room_size = data_elements[idx+1].text.split(" ")
                        data_dict["primary_room_size"] = room_size[0]
                    elif text == "bruksareal":
                        room_size = data_elements[idx+1].text.split(" ")
                        data_dict["usable_area"] = room_size[0]
                    elif text == "byggeår":
                        data_dict["build_year"] = data_elements[idx+1].text
                    elif text == "etasje":
                        data_dict["floor"] = data_elements[idx+1].text
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
        finally:
            print("done with page")
    finally:
        browser.close()
        print("browser closed")
    return data_dict


async def get_data_from_element(element, link):
    await asyncio.sleep(0.5)
    data_dict = {}
    try:
        print("fetching element")
        try:
            sold = element.find_element_by_css_selector(".showing-date").text
            if "SOLGT" in sold:
                return data_dict
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        data_dict["link"] = link
        try:
            image = element.find_element_by_css_selector("img").get_attribute("src")
            data_dict["image"] = image
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            building_type = element.find_element_by_css_selector(".unit-type").text
            data_dict["building_type"] = building_type
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            primary_room_size = element.find_element_by_css_selector(".size").text
            data_dict["primary_room_size"] = primary_room_size
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            city = element.find_element_by_css_selector(".city").text
            data_dict["city"] = city
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            address = element.find_element_by_css_selector(".address").text
            data_dict["address"] = address
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
        try:
            asking_price = element.find_element_by_css_selector(".price").text
            asking_price = asking_price.replace("kr", "")
            asking_price = asking_price.replace(" ", "")
            data_dict["asking_price"] = asking_price
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(link)
    except Exception as err:
        print(type(err))
        print(err)
    finally:
        print("element got got gotten")
    return data_dict


async def mainstuff():
    try:
        browser = Chrome(executable_path="C:\Cmder\Python\PythonPaths\chromedriver.exe", options=opts)
        browser.get(URL)
        await asyncio.sleep(5)
        with open("properties_dnb.html", "w", encoding="utf8") as f:
            f.write(browser.page_source)
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
                    for advert in properties:
                        if count % 5 == 0:
                            for key in task_dict:
                                print("Waiting for task #{}".format(key))
                                await task_dict[key]
                                result = task_dict[key].result()
                                print("Result: {}".format(task_dict[key].result()))
                                title = f"placeholder_{placeholder_count}"
                                if "address" in result:
                                    title = result["address"]
                                    if title in all_keys:
                                        title += f"_{placeholder_count}"
                                    all_keys.append(title)
                                placeholder_count += 1
                                file.write('"{}": {}, \n'.format(title, json.dumps(result, indent=4, ensure_ascii=False)))
                            task_dict = {}
                        link = advert.find_element_by_tag_name('a').get_attribute("href")
                        if link:
                            # new_browser = Firefox(options=opts)
                            # image = advert.find_element_by_tag_name("img").get_attribute("src")
                            # building_type = advert.find_element_by_class_name("unit-type").text
                            task_dict[count] = asyncio.create_task(get_data_from_element(advert, link))
                            # task_dict[count] = asyncio.create_task(new_browser_shenanigans(link, image, building_type))
                            print(f"task #{count} created")
                            count += 1
                        else:
                            print("nothing here")
                    for key in task_dict:
                        print(f"Waiting for task #{key}")
                        await task_dict[key]
                        result = task_dict[key].result()
                        if len(result) == 0:
                            print("Skipping empty result")
                            continue
                        print(f"Result: {result}")
                        title = f"placeholder_{placeholder_count}"
                        if "address" in result:
                            title = result["address"]
                            if title in all_keys:
                                title += f"_{placeholder_count}"
                            all_keys.append(title)
                        placeholder_count += 1
                        file.write('"{}": {}, \n'.format(title, json.dumps(result, indent=4, ensure_ascii=False)))
                except Exception as err:
                    print(type(err))
                    print(err)
                file.write('"":""}')

    finally:
        browser.close()
        print("browser closed, final")


asyncio.run(mainstuff())
