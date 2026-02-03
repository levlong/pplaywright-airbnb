from pages.base_page import BasePage
from pages.device_page import DevicePage
from utils.logger import get_logger

class SideBarComponent(BasePage):

    logger = get_logger(__name__)

    DEVICE_TAB   = {"role": "link", "name": "Devices"}
    CUSTOMER_TAB = {"role": "link", "name": "Customers"}

    def click_device(self):
        """
        Ham nay click vao nut device nam trong entities menu
        """
        self.click(action_name="click_device_tab", **self.DEVICE_TAB)
        return DevicePage(self.page)
    
    def ensure_menu_open(self, menu_item):
        """
        Hàm này đảm bảo việc menu sẽ luôn được mở

        Cách dùng:
            ensure_menu_open("tên của menu")

        Args:
            menu_item (str): Tên của cái menu (toggled) ở side bar (ví dụ: entities, profiles)
        """
        toggle_menu_selector = (
            f"//span[normalize-space(text())='{menu_item}']"
            "/following-sibling::span[contains(@class,'tb-toggle-icon')]"
        )

        toggle_menu_el = self.el(toggle_menu_selector)

        menu_class = toggle_menu_el.get_attribute("class") or ""

        if "tb-toggled" not in menu_class:
            self.logger.info(f"Menu '{menu_item}' is closed → opening")
            self.click(
                action_name="click_toggle_menu",
                value=toggle_menu_selector
            )
        else:
            self.logger.info(f"Menu '{menu_item}' already open")

        return self