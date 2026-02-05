import pytest
from pages.login_page import LoginPage
from components.side_bar_component import SideBarComponent

def test_valid_login(page):
        side_bar_component = (
                LoginPage(page)
                        .goto("/login", "go_to_login")
                        .login("hi.newagenewera@gmail.com", "Tuilasieunhan@")
                        .ensure_menu_open(menu_item="Entities")
                        .click_device()
                        .verify_device_page()
                        .add_new_device("Drain valve", "Valve", "Customer A")
                )
