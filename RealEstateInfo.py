class RealEstateInfo:
    def __init__(self, url, file_name, element_list, property_cards_css_selector, special_start=False, special_case=False):
        self.url = url
        self.file_name = file_name
        self.element_list = element_list
        self.property_cards_css_selector = property_cards_css_selector
        self.special_start = special_start
        self.special_case = special_case
