from pages.base_page import BasePage

class SideBarComponent(BasePage):
    EXPERIENCE_TAB = { "role": "tab", "name" : "Trải nghiệm, mới" }
    
    def click_experience_tab(self):
        self.click(**self.EXPERIENCE_TAB, action_name="Click on experiences tab")
        return self