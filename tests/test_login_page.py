from pages.login_page import LoginPage
from components.side_bar_component import SideBarComponent

def test_valid_login(page):
        side_bar_component = (
                LoginPage(page)
                .goto("/login", "go_to_login")
                .login("hi.newagenewera@gmail.com", "Tuilasieunhan@")
                )

        # side_bar_component.ensure_menu_open("entities")