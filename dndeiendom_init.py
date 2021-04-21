from RealEstateInfo import RealEstateInfo
import asyncio


async def special_start(browser):
    while True:
        try:
            browser.execute_script("document.querySelector(\"button.LoadMoreButtonstyles__StyledLoadMoreButton-sc-1p7l32l-1\").click()")
            print("clicking button")
            await asyncio.sleep(0.5)
        except:
            break
    print("no more to load")
    await asyncio.sleep(1)


DnbEiendom = RealEstateInfo(
    "https://dnbeiendom.no/bolig/Nordland/Bod%C3%B8",
    "data_dnbeiendom.json",
    [
        ["image", ".EstateSearchResultListItemstyles__StyledListItemImage-zzmpr3-2", "src"],
        ["address", ".EstateSearchResultListItemstyles__StyledListItemStreet-zzmpr3-7.exXJtp", "innerHTML"],
        ["city", "h3.EstateSearchResultListItemstyles__StyledListItemDistrictCity-zzmpr3-6", "innerHTML"],
        ["asking_price", "p.EstateSearchResultListItemstyles__StyledListItemPriceHint-zzmpr3-9 span.dnb-number__selection.dnb-no-focus", "innerHTML"],
        ["total_price", "p.EstateSearchResultListItemstyles__StyledListItemTotalPriceHint-zzmpr3-10 span.dnb-number__selection.dnb-no-focus", "innerHTML"],
        ["bedrooms", "p.dnb-p.EstateSearchResultListItemstyles__StyledBedroomsCount-zzmpr3-15 span.dnb-number__selection.dnb-no-focus", "innerHTML"],
        ["primary_room_size", "p.EstateSearchResultListItemstyles__StyledEstateArea-zzmpr3-14 b", "innerHTML"],
    ],
    ".EstateSearchResultListItemstyles__StyledItemContainer-zzmpr3-0",
    special_start=special_start
)
