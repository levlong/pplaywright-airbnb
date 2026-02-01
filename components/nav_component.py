from pages.base_page import BasePage

class NavComponent(BasePage):
    AIRBNB_LOGO    = "//a[@aria-label='Airbnb homepage']"
    HOME_TAB       = "//a[@data-tabid='tabBarItem-STAYS']"
    EXPERIENCE_TAB = "//a[@data-tabid='tabBarItem-EXPERIENCES']"
    SERVICE_TAB    = "//a[@data-tabid='tabBarItem-SERVICES']"
    LANGUAGE       = "//button[@aria-label='Choose a language and currency']"
    MENU           = "//button[@aria-label='Main navigation menu']"

    def verify_logo_visible(self):
        self.expect_visible(self.AIRBNB_LOGO, "nav_logo_visible")
        return self

    def click_logo(self):
        self.click(self.AIRBNB_LOGO, "click_logo")
        return self

    def click_home_tab(self):
        self.click(self.HOME_TAB, "click_home_tab")
        return self

    def click_experience_tab(self):
        self.click(self.EXPERIENCE_TAB, "click_experience_tab")
        return self

    def click_service_tab(self):
        self.click(self.SERVICE_TAB, "click_service_tab")
        return self

    def click_language(self):
        self.click(self.LANGUAGE, "click_language_tab")
        return self

    def open_menu(self):
        self.click(self.MENU, "click_menu_icon")
        return self