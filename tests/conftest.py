import pytest
from playwright.sync_api import sync_playwright, Page

@pytest.fixture(scope="function", autouse=True)
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport=None)
        page = context.new_page()
        yield page
        context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("page")
        if page:
            page.screenshot(
                path=f"reports/screenshots/{item.name}.png",
                full_page=True
            )
