import os
import time
from playwright.sync_api import Page, Locator, expect
from utils.logger import get_logger
from typing import Literal, TypedDict, Optional, Union

# Định nghĩa một Type cho các Role hợp lệ trong Playwright để AI gợi ý chuẩn
RoleType = Literal[
    "button", "checkbox", "combobox", "grid", "heading", "img", 
    "link", "listbox", "menu", "meter", "radio", "textbox", "searchbox"
]

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
    
    def el(
        self, 
        value: Optional[Union[str, Locator]] = None, 
        role: Optional[RoleType] = None,
        name: Optional[Union[str, dict]] = None,
        text: Optional[str] = None,
        label: Optional[str] = None,
        placeholder: Optional[str] = None,
        alt_text: Optional[str] = None,
        title: Optional[str] = None,
        test_id: Optional[str] = None,
        checked: Optional[bool] = None,
        has_text: Optional[str] = None,
        base: Optional[Locator] = None,
        **kwargs
    ) -> Locator:
        """
        Tìm kiếm Locator dựa trên các tham số được cung cấp.
        Gợi ý: Luôn ưu tiên dùng test_id hoặc role để test bền vững hơn.
        """
        locator: Optional[Locator] = None
        root = base if base else self.page

        # 0. Nếu value đã là Locator thì dùng luôn
        if isinstance(value, Locator):
            return value

        # 1. Xpath hoặc Text thuần
        if value and isinstance(value, str):
            if value.startswith("//") or value.startswith("(//"):
                locator = root.locator(value)
            else:
                locator = root.get_by_text(value)
        
        # 2. Locator theo chuẩn Playwright mới
        elif role:
            locator = root.get_by_role(role, name=name, checked=checked)
        elif text:
            locator = root.get_by_text(text)
        elif label:
            locator = root.get_by_label(label)
        elif placeholder:
            locator = root.get_by_placeholder(placeholder)
        elif alt_text:
            locator = root.get_by_alt_text(alt_text)
        elif title:
            locator = root.get_by_title(title)
        elif test_id:
            locator = root.get_by_test_id(test_id)
        else:
            raise ValueError(f"Ít nhất một selector phải được cung cấp. Nhận được: {kwargs}")

        # 3. Filter bổ trợ
        if has_text:
            locator = locator.filter(has_text=has_text)

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

    def hover(self, action_name: str = "hover_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        try:
            el.wait_for(state="visible")
            el.hover()
        except Exception as e:
            self._fail_action(action_name)
            raise e
        return self
    
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

    def expect_hidden(self, action_name: str = "hidden_fail", value=None, **kwargs):
        el = self.el(value, **kwargs)
        self._ui_expect(el, action_name)(
            lambda e: expect(e).to_be_hidden()
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
