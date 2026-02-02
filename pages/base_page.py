import os
import time
from playwright.sync_api import Page, Locator, expect

class BasePage:
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
        # Neu selector la xpath
        if value and isinstance(value, str):
            if value.startswith("//") or value.startswith("(//"):
                return self.page.locator(value)
            return self.page.get_by_text(value)
            
        # Lay locator theo role
        if "role" in kwargs:
            return self.page.get_by_role(
                kwargs["role"], name=kwargs.get("name")
            )
        
        # Lay locator theo text
        if "text" in kwargs:
            return self.page.get_by_text(kwargs["text"])
        
        # Lay locator theo label
        if "label" in kwargs:
            return self.page.get_by_label(kwargs["label"])
        
        # Lay locator theo placeholder
        if "placeholder" in kwargs:
            return self.page.get_by_placeholder(kwargs["placeholder"])
        
        # Lay locator theo alt text
        if "alt_text" in kwargs:
            return self.page.get_by_alt_text(kwargs["alt_text"])
        
        # Lay locator theo title
        if "title" in kwargs:
            return self.page.get_by_title(kwargs["title"])
        
        # Lay locator theo test id
        if "test_id" in kwargs:
            return self.page.get_by_test_id(kwargs["test_id"])

        raise ValueError(f"Unsupported selector {kwargs}")

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

    def expect_text(self, text: str, action_name: str = "text_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        self._ui_expect(el, action_name)(
            lambda e: expect(e).to_have_text(text)
        )
        return self

    def expect_contains_text(self, text: str, action_name: str = "contain_text_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        self._ui_expect(el, action_name)(
            lambda e: expect(e).to_contain_text(text)
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
