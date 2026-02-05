import os
import time
from playwright.sync_api import Page, Locator, expect
from utils.logger import get_logger

class BasePage:

    logger = get_logger(__name__)

    """
    BasePage cung cấp các hành động chung cho tất cả Page / Component.

    - Cung cấp các action cơ bản: goto, click, fill, get_text
    - Được kế thừa bởi các Page Object / Component
    """
    def __init__(self, page: Page):
        """
        Khởi tạo Basepage
        
        :param page: Playwright Page instance
        """
        self.page = page
    
    def el(self, value=None, **kwargs) -> Locator:
        locator: Locator | None = None

        # Neu selector la xpath
        if value and isinstance(value, str):
            if value.startswith("//") or value.startswith("(//"):
                locator = self.page.locator(value)
            else:
                locator = self.page.get_by_text(value)
            
        # Lay locator theo role
        elif "role" in kwargs:
            locator = self.page.get_by_role(
                kwargs["role"], 
                name=kwargs.get("name"),
                checked=kwargs.get("checked", None)
            )
        
        # Lay locator theo text
        elif "text" in kwargs:
            locator = self.page.get_by_text(kwargs.get("text"))
        
        # Lay locator theo label
        elif "label" in kwargs:
            locator = self.page.get_by_label(kwargs.get("label"))
        
        # Lay locator theo placeholder
        elif "placeholder" in kwargs:
            locator = self.page.get_by_placeholder(kwargs.get("placeholder"))
        
        # Lay locator theo alt text
        elif "alt_text" in kwargs:
            locator = self.page.get_by_alt_text(kwargs.get("alt_text"))
        
        # Lay locator theo title
        elif "title" in kwargs:
            locator = self.page.get_by_title(kwargs.get("title"))
        
        # Lay locator theo test id
        elif "test_id" in kwargs:
            locator = self.page.get_by_test_id(kwargs.get("test_id"))
        else:
            raise ValueError(f"Unsupported selector {kwargs}")

        if "has_text" in kwargs:
            locator = locator.filter(has_text=kwargs.get("has_text"))

        return locator

    def goto(self, url: str, name: str = "goto_fail", wait="domcontentloaded"):
        try:
            self.page.goto(url)
            self.page.wait_for_load_state(wait)
        except Exception as e:
            self._fail_action(name)
            raise e
        return self

    def click(self, action_name: str = "click_fail", value=None, **kwargs):
            el = self.el(value, **kwargs)
            try:
                el.wait_for(state="visible")
                el.click()
            except Exception as e:
                self._fail_action(action_name)
                raise e
            return self
            
    def fill(self, text: str, action_name: str = "fill_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        try:
            el.wait_for(state="visible")
            el.fill(text)
        except Exception as e:
            self._fail_action(action_name)
            raise e
        return self
    
    def type(self, text: str, action_name: str = "type_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        try:
            el.wait_for(state="visible")
            el.type(text)
        except Exception as e:
            self._fail_action(action_name)
            raise e
        return self

    def get_text(self, action_name: str = "get_text_fail", value=None, **kwargs) -> str:
        el = self.el(value, **kwargs)
        try:
            el.wait_for(state="visible")
            return el.inner_text()
        except Exception as e:
            self._fail_action(action_name)
            raise e
    
    # ================= ASSERTIONS =================

    def expect_visible(self, action_name: str = "visible_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        self._ui_expect(el, action_name)(
            lambda e: expect(e).to_be_visible()
        )
        return self

    def expect_text(self, expected_text: str, action_name: str = "text_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        self.logger.info(el.inner_text())
        self._ui_expect(el, action_name)(
            lambda e: expect(e).to_have_text(expected_text)
        )
        return self

    def expect_contains_text(self, expected_text: str, action_name: str = "contain_text_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        self.logger.info(el.inner_text())
        self._ui_expect(el, action_name)(
            lambda e: expect(e).to_contain_text(expected_text)
        )
        return self

        
    def _ui_expect(self, locator: Locator, action_name: str="ui_fail", full_page=False):
        """
        Wrapper cho Playwright expect().

        Mục đích:
        - Thực hiện assertion với expect(locator)
        - Nếu assertion FAIL thì:
            + chụp screenshot đúng element bị fail
            + re-raise AssertionError để pytest đánh FAIL test

        Cách dùng:
            ui_expect(title, "home_title")(
                lambda el: expect(el).to_have_text("Home")
            )

        Args:
            locator (Locator): Playwright locator cần assert
            name (str): Tên file screenshot khi fail (không cần .png)

        Returns:
            function: Một function nhận vào expect_fn (assertion function)
        """
        def _wrap(expect_fn):
            ts = int(time.time())
            try:
                expect_fn(locator)
            except AssertionError:
                os.makedirs("reports/screenshots", exist_ok=True)
                if full_page:
                    locator.page.screenshot(
                        path=f"reports/screenshots/{action_name}_{ts}.png"
                    )
                else:
                    locator.screenshot(
                        path=f"reports/screenshots/{action_name}_{ts}.png"
                    )
                raise
        return _wrap
    
    def _fail_action(self, action_name: str):
        os.makedirs("reports/screenshots", exist_ok=True)
        ts = int(time.time())
        self.page.screenshot(
            path=f"reports/screenshots/{action_name}_{ts}.png"
        )
