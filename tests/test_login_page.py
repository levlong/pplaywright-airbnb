from pages.login_page import LoginPage

def test_valid_login(page):
        loginPage = LoginPage(page)
        loginPage.goto("/login", "go_to_login")
        loginPage.login("hi.newagenewera@gmail.com", "Tuilasieunhan@")