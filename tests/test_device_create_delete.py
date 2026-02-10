import pytest
import time
from pages.login_page import LoginPage

def test_create_and_delete_device(page):
    """
    Test Flow:
    1. Login to thingsboard
    2. Navigate to Devices page
    3. Create a new device
    4. Verify device was created
    5. Delete the device
    6. Verify device was deleted
    """
    # Generate unique device name using timestamp
    device_name = f"Test_Device_{int(time.time())}"
    device_label = f"TD_{int(time.time())}"
    
    # Step 1-2: Navigate to login and login
    # Step 3: Navigate to Devices page
    # Step 4: Create new device
    device_page = (
        LoginPage(page)
        .goto("/login", "go_to_login")
        .login("hi.newagenewera@gmail.com", "Tuilasieunhan@")
        .ensure_menu_open(menu_item="Entities")
        .click_device()
        .verify_device_page()
        .add_new_device(device_name, device_label, "Customer A")
    )
    
    # Step 5: Delete the device
    device_page.delete_device(device_name)
