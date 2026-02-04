import os, pytest, glob, platform, getpass
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pytest_html import extras
from pytest_metadata.plugin import metadata_key


# Load config file
def detect_env():
    if os.getenv("JENKINS_URL"):
        return "ci"
    if os.getenv("CI") == "true":
        return "ci"
    return "local"

ENV = detect_env()
os.environ["ENV"]=ENV
load_dotenv(f"config/{ENV}.env", override=True)

# ================== READ CONFIG ==================
HEADLESS = os.getenv("HEADLESS") == "true"
SLOW_MO = int(os.getenv("SLOW_MO", 0))
BROWSER = os.getenv("BROWSER", "chromium")
BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise RuntimeError("BASE_URL is not set")
TIMEOUT = int(os.getenv("TIMEOUT", 30000))
TAKE_SCREENSHOT = os.getenv("TAKE_SCREENSHOT", "off")
TAKE_TRACE = os.getenv("TAKE_TRACE", "off")

@pytest.fixture(scope="function", autouse=True)
def page():
    launch_args = [
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--disable-gpu"
    ]

    with sync_playwright() as p:
        browser_type = getattr(p, BROWSER)

        browser = browser_type.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO if not HEADLESS else 0,
            args=launch_args
        )

        context = browser.new_context(
            viewport=None,
            base_url=BASE_URL
        )

        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()
        page.set_default_timeout(TIMEOUT)

        yield page

        context.tracing.stop(path="reports/trace.zip")
        context.close()
        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        screenshot_dir = "reports/screenshots"

        if not os.path.exists(screenshot_dir):
            return

        screenshots = glob.glob(f"{screenshot_dir}/*.png")
        if not screenshots:
            return

        latest_screenshot = max(screenshots, key=os.path.getctime)

        # path relative với report.html
        relative_path = latest_screenshot.replace("reports/", "")

        extra = getattr(report, "extra", [])
        extra.append(extras.image(relative_path))
        report.extras = extra

def pytest_html_report_title(report):
    report.title = "Airbnb Automation UI test"

def pytest_configure(config):
    md = config.stash[metadata_key]

    md.clear()

    md["Project"] = "Airbnb Playwright"
    md["Environment"] = os.getenv("ENV", "local")
    md["Browser"] = os.getenv("BROWSER", "chromium")
    md["Headless"] = os.getenv("HEADLESS")
    md["Base URL"] = os.getenv("BASE_URL")
    md["Timeout (ms)"] = os.getenv("TIMEOUT")
    md["OS"] = platform.system()
    md["User"] = getpass.getuser()