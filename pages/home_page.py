from pages.base_page import BasePage
from components.nav_component import NavComponent

class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.nav = NavComponent(page)
