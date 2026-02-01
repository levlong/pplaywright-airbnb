from pages.home_page import HomePage

def test_homepage_nav(page):
    home = HomePage(page)
    home.goto("https://www.airbnb.com")
    home.nav.click_logo()
    home.nav.click_experience_tab()