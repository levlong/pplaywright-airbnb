from pages.base_page import BasePage

class LoginPage(BasePage):

    # Locator by role
    LOGO      = { "role": "link", "name":"logo" }
    USERNAME  = { "role": "textbox", "name": "Username (email)" }
    PASSWORD  = { "role": "textbox", "name": "Password"}
    LOGIN_BTN = { "role": "button", "name":"Sign in" }

    def verify_logo_visible(self):
        self.expect_visible(**self.LOGO, action_name="nav_logo_visible")
        return self

    def click_logo(self):
        self.click(**self.LOGO, action_name="click_logo")
        return self
    
    def click_user_name(self):
        self.click(**self.USERNAME, action_name="click_user_name")
        return self
    
    def enter_user_name(self, username):
        self.fill(username, **self.USERNAME, action_name="fill_user_name")
    
    def click_password(self):
        self.click(**self.PASSWORD, action_name="click_password")
        return self
    
    def enter_password(self, password):
        self.fill(password, **self.PASSWORD, action_name="fill_password")
    
    def click_login(self):
        self.click(**self.LOGIN_BTN, action_name="click_login")
        return self
    
    def login(self, username, password):
        self.click_user_name()
        self.enter_user_name(username)
        self.click_password()
        self.enter_password(password)
        self.click_login()
        
