import shlex
import json
import requests
import time
from pages.base_page import BasePage
from utils.logger import get_logger

class DevicePage(BasePage):

    logger = get_logger(__name__)

    DEVICE_TITLE          = "devices_other devices_other Devices"
    ADD_DEVICE            = {"role": "button", "has_text": "add"}
    ADD_NEW_DEVICE        = {"role": "menuitem", "name": "Add new device"}
    DEVICE_NAME           = {"role": "textbox", "name": "Name"}
    DEVICE_LABEL          = {"role": "textbox", "name": "Label"}
    ASSIGN_DEVICE         = {"role": "combobox", "name": "Assign to customer"}
    CLOSE_CONFIRM         = {"role": "button", "name": "Close"}
    ADD_NEW_DEVICE_BUTTON = {"role": "button", "name": "Add"}
    REFRESH_DEVICE_BUTTON = {"role": "button", "has_text": "refresh"}
    DEVICE_STATUS         = "Active"
    API                   = "curl -v -X POST http://demo."

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
        self.type(device_name, action_name="Enter_device_name", **self.DEVICE_NAME)
        return self
    
    def enter_device_label(self, device_label):
        self.fill(device_label, action_name="Enter_device_name", **self.DEVICE_LABEL)
        return self
    
    def assign_device_to_user(self, user_name):
        self.click(action_name="assign_device_to_user", **self.ASSIGN_DEVICE)
        self.click(action_name="assign_new_device_to_user", role="option", name=user_name)
        return self
    
    def curl_to_requests(self, curl_cmd: str):
        parts = shlex.split(curl_cmd)
        method = "GET"
        url = None
        headers = {}
        data = None

        i = 0
        while i < len(parts):
            part = parts[i]

            if part == "-X":
                method = parts[i + 1]
                i += 2

            elif part.startswith("http"):
                url = part
                i += 1

            elif part in ("-H", "--header"):
                key, value = parts[i + 1].split(":", 1)
                headers[key.strip()] = value.strip()
                i += 2

            elif part in ("-d", "--data", "--data-raw"):
                data = parts[i + 1]
                i += 2

            else:
                i += 1

        # Nếu content-type là json thì parse data
        json_data = None
        if data and "application/json" in headers.get("Content-Type", ""):
            try:
                json_data = json.loads(data)
                data = None
            except json.JSONDecodeError:
                pass  # để raw data, không ép

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json_data,
            data=data,
            timeout=10
        )

        self.logger.info(response)

        return response
    
    def __verify_new_device(self, api):
        self.logger.info("Verify new device by calling activate API")

        response = self.curl_to_requests(api)

        # Verify status
        assert response.status_code == 200, response.text

        self.logger.info("Device activated successfully via API")
    
    def add_new_device(self, device_name, device_label, user_name):
        ts = int(time.time())
        self.click_add_device()
        self.click_add_new_device()
        self.enter_device_name(f"{device_name}_{ts}")
        self.enter_device_label(device_label)
        self.assign_device_to_user(user_name)
        self.click(action_name="Click_add_new_device_button", **self.ADD_NEW_DEVICE_BUTTON)

        active_device_api = self.get_text(action_name="Get_active_device_api", text=self.API)

        self.logger.info(active_device_api)

        self.__verify_new_device(active_device_api)

        self.click(action_name="Click_close_confirmation_form", **self.CLOSE_CONFIRM)

        self.click(action_name="Refresh_device_tab", **self.REFRESH_DEVICE_BUTTON)

        self.click(action_name="Refresh_device_tab", **self.REFRESH_DEVICE_BUTTON)

        device_status = (f"//mat-row[.//mat-cell[contains(@class,'mat-column-name')]"
                        f"//span[normalize-space()='{device_name}_{ts}']]"
                        f"//mat-cell[contains(@class,'mat-column-active')]"
                        f"//div[contains(@class,'status')]")

        self.expect_contains_text(expected_text="Active", action_name="Verify_device_status", value=device_status)

        self.expect_contains_text(
            expected_text=f"{device_name}_{ts}", 
            action_name="Verify_new_added_device", 
            role="cell", 
            name=f"{device_name}_{ts}")

        return self