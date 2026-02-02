from pages.base_page import BasePage

class SideBarComponent(BasePage):
    DEVICE_TAB   = {"role": "link", "name": "Devices"}
    CUSTOMER_TAB = {"role": "link", "name": "Customers"}
    ENTITY_TAB   = "categorycategoryEntities"

    def click_device(self):
        self.click(action_name="click_device_tab", **self.DEVICE_TAB)
        return self
    
    def click_entity_tab(self):
        self.click(action_name="click_entity_tab", text=self.ENTITY_TAB)
        return self
    
    def click_customer_tab(self):
        self.click(action_name="click_customer_tab", **self.CUSTOMER_TAB)
        return self