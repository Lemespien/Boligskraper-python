class Element:

    element_container = ""

    def __init__(self, title, css_selector, attribute="text"):
        self.css_selector = css_selector
        self.attribute = attribute
        self.title = title
        if attribute in ["src", "href", "innerHTML"]:
            self.get_method = self.get_data_from_attribute
        elif attribute in ["text"]:
            self.get_method = self.get_data_from_text

    def find_element(self):
        self.target_element = self.element_container.find_element_by_css_selector(self.css_selector)

    def get_data_from_attribute(self):
        data = ""
        try:
            data = self.target_element.get_attribute(self.attribute)
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(self.element_container)
        finally:
            return data

    def get_data_from_text(self):
        data = ""
        try:
            data = self.target_element.text
        except Selenium_Exceptions.NoSuchElementException as no_element:
            print(no_element)
            print(self.element_container)
        finally:
            return data
