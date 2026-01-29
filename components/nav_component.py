from pages.base_page import BasePage

class NavComponent(BasePage):
    AIRBNB_LOGO    = "//a[@aria-label='Airbnb homepage']"
    HOME_TAB       = "//a[@data-tabid='tabBarItem-STAYS']"
    EXPERIENCE_TAB = "//a[@data-tabid='tabBarItem-EXPERIENCES']"
    SERVICE_TAB    = "tabBarItem-SERVICES"
    LANGUAGE       = "//button[@aria-label='Choose a language and currency']"
    MENU           = "//button[@aria-label='Main navigation menu']"

    def click_logo(self):
        self.click(self.AIRBNB_LOGO)

    def click_home_tab(self):
        self.click(self.HOME_TAB)

    def click_experience_tab(self):
        self.click(self.EXPERIENCE_TAB)

    def click_service_tab(self):
        self.click(self.SERVICE_TAB)

    def click_language(self):
        self.click(self.LANGUAGE)

    def open_menu(self):
        self.click(self.MENU)