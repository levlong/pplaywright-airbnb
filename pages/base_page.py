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

    def _locator(self, selector):
        """
        Tạo locator từ selector.

        :param selector: selector (xpath / css / text)
        """
        return self.page.locator(selector)

    def goto(self, url: str, name: str = "goto_fail", wait="domcontentloaded"):
        try:
            self.page.goto(url)
            self.page.wait_for_load_state(wait)
        except Exception as e:
            self._fail_action(name)
            raise e

    def click(self, locator: str, name: str = "click_fail"):
        el = self._locator(locator)
        try:
            el.wait_for(state="visible")
            el.click()
        except Exception as e:
            self._fail_action(name)
            raise e

    def fill(self, locator: str, text: str, name: str = "fill_fail"):
        el = self._locator(locator)
        try:
            el.wait_for(state="visible")
            el.fill(text)
        except Exception as e:
            self._fail_action(name)
            raise e

    def get_text(self, locator: str, name: str = "get_text_fail") -> str:
        el = self._locator(locator)
        try:
            el.wait_for(state="visible")
            return el.inner_text()
        except Exception as e:
            self._fail_action(name)
            raise e
    
     # ================= ASSERTIONS =================

    def expect_visible(self, locator: str, name: str = "visible_fail"):
        el = self._locator(locator)
        self._ui_expect(el, name)(
            lambda e: expect(e).to_be_visible()
        )

    def expect_text(self, locator: str, text: str, name: str = "text_fail"):
        el = self._locator(locator)
        self._ui_expect(el, name)(
            lambda e: expect(e).to_have_text(text)
        )

    def expect_contains_text(self, locator: str, text: str, name: str = "contain_text_fail"):
        el = self._locator(locator)
        self._ui_expect(el, name)(
            lambda e: expect(e).to_contain_text(text)
        )

        
    def _ui_expect(self, locator: Locator, name: str="ui_fail", full_page=False):
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
                        path=f"reports/screenshots/{name}_{ts}.png"
                    )
                else:
                    locator.screenshot(
                        path=f"reports/screenshots/{name}_{ts}.png"
                    )
                raise
        return _wrap
    
    def _fail_action(self, name: str):
        os.makedirs("reports/screenshots", exist_ok=True)
        ts = int(time.time())
        self.page.screenshot(
            path=f"reports/screenshots/{name}_{ts}.png"
        )
