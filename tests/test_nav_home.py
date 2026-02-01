from components.nav_component import NavComponent

def test_nav_home(page):
    nav = NavComponent(page)

    nav.goto("https://www.airbnb.com", "open_home")

    nav.expect_visible(nav.AIRBNB_LOGO, "logo_visible")

    nav.click_home_tab()
    nav.expect_contains_text(nav.HOME_TAB, "vc", "home_tab_text")
