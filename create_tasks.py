import asyncio
from write_to_file import write_to_file


async def create_tasks(properties, callback, realEstateInfo):
    task_dict = {}
    count = 0
    for advert in properties:
        advert.location_once_scrolled_into_view
        link = advert.get_attribute("href")
        if not link:
            link = advert.find_element_by_css_selector("a").get_attribute("href")
        if link:
            task_dict[count] = asyncio.create_task(callback(advert, link, realEstateInfo))
            print(f"task #{count} created")
            count += 1
        else:
            print("nothing here")
    return task_dict
