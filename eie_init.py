from RealEstateInfo import RealEstateInfo
import asyncio


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


Eie = RealEstateInfo(
    'https://eie.no/eiendom/til-salgs?free_text=bod%C3%B8&county[]=18',
    "data_eie.json",
    [
        ["image", "figure img", "src"],
        ["address", ".card__headline"],
        ["city", ".card__overline"]
    ],
    "main div.section__body div.cards a.card", 
    special_case=special_case)
