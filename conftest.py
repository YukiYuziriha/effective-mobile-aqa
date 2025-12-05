import pytest
import allure
from typing import Dict, Any, Generator, cast
from playwright.sync_api import Page
from pytest import Item, CallInfo, TestReport, Function
from pages.main_page import MainPage

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }

@pytest.fixture
def main_page(page: Page) -> MainPage:
    """
    Fixture that initializes and returns the MainPage object.
    """
    return MainPage(page)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo[None]) -> Generator[None, Any, None]:
    """
    Hook to attach a screenshot to the Allure report on test failure.
    """
    outcome = yield
    rep: TestReport = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Check if item is a Function and 'page' fixture is available
        if isinstance(item, Function) and "page" in item.funcargs:
            page = cast(Page, item.funcargs["page"])
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
