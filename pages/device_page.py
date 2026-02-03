from pages.base_page import BasePage

class DevicePage(BasePage):
    DEVICE_TITLE          = "devices_other devices_other Devices"
    ADD_DEVICE            = {"role": "button", "has_text": "add"}
    ADD_NEW_DEVICE        = {"role": "menuitem", "name": "Add new device"}
    DEVICE_NAME           = {"role": "textbox", "name": "Name"}
    DEVICE_LABEL          = {"role": "textbox", "name": "Label"}
    ASSIGN_DEVICE         = {"role": "combobox", "name": "Assign to customer"}
    CLOSE_CONFIRM         = {"role": "button", "name": "Close"}
    ADD_NEW_DEVICE_BUTTON = {"role": "button", "name": "Add"}

    def verify_device_page(self):
        self.expect_contains_text(expected_text="Devices", action_name="verify_device_page", text=self.DEVICE_TITLE)
        return self
    
    def click_add_device(self):
        self.click(action_name="Click_add_device", **self.ADD_DEVICE)
        return self
    
    def click_add_new_device(self):
        self.click(action_name="Click_add_new_device", **self.ADD_NEW_DEVICE)
        return self
    
    def enter_device_name(self, device_name):
        self.fill(device_name, action_name="Enter_device_name", **self.DEVICE_NAME)
        return self
    
    def enter_device_label(self, device_label):
        self.fill(device_label, action_name="Enter_device_name", **self.DEVICE_LABEL)
        return self
    
    def assign_device_to_user(self, user_name):
        self.click(action_name="assign_device_to_user", **self.ASSIGN_DEVICE)
        self.click(action_name="assign_new_device_to_user", role="option", name=user_name)
        return self
    
    def add_new_device(self, device_name, device_label, user_name):
        self.click_add_device()
        self.click_add_new_device()
        self.enter_device_name(device_name)
        self.enter_device_label(device_label)
        self.assign_device_to_user(user_name)
        self.click(action_name="Click_add_new_device_button", **self.ADD_NEW_DEVICE_BUTTON)
        self.click(action_name="Click_close_confirmation_form", **self.CLOSE_CONFIRM)
        self.expect_contains_text(expected_text=device_name, action_name="Verify_new_added_device", role="cell", name=device_name)

        return self