from pages.base_page import BasePage
from components.side_bar_component import SideBarComponent

class LoginPage(BasePage):

    # Locator by role
    LOGO      = { "role": "link", "name":"logo" }
    USERNAME  = { "role": "textbox", "name": "Username (email)" }
    PASSWORD  = { "role": "textbox", "name": "Password"}
    LOGIN_BTN = { "role": "button", "name":"Sign in" }

    def verify_logo_visible(self):
        self.expect_visible(action_name="nav_logo_visible", **self.LOGO)
        return self

    def click_logo(self):
        self.click(action_name="click_logo", **self.LOGO)
        return self
    
    def click_user_name(self):
        self.click(action_name="click_user_name", **self.USERNAME)
        return self
    
    def enter_user_name(self, username):
        self.fill(username, action_name="fill_user_name", **self.USERNAME)
    
    def click_password(self):
        self.click(action_name="click_password", **self.PASSWORD)
        return self
    
    def enter_password(self, password):
        self.fill(password, action_name="fill_password", **self.PASSWORD)
    
    def click_login(self):
        self.click(action_name="click_login", **self.LOGIN_BTN)
        return self
    
    def login(self, username, password):
        self.click_user_name()
        self.enter_user_name(username)
        self.click_password()
        self.enter_password(password)
        self.click_login()
        return SideBarComponent(self.page)
        
