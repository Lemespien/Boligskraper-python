from RealEstateInfo import RealEstateInfo
import asyncio


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

EiendomsMegler1 = RealEstateInfo(
    "https://www.eiendomsmegler1.no/kjope-bolig?search=bod%C3%B8",
    "data_eiendomsmegler1.json",
    [
        ["image", "img", "src"],
        ["building_type", ".unit-type"],
        ["primary_room_size", ".size"],
        ["city", ".city"],
        ["address", ".address"],
    ],
    ".property-card",
    special_start=special_start,
    special_case=special_case
)
