import allure
import pytest

from pages.main_page import MainPage


@allure.feature("Main Page Navigation")
class TestMainPageNavigation:
    @allure.story("Navigate through main menu items")
    @pytest.mark.parametrize(
        "nav_action, expected_fragment",
        [
            ("click_about", "about"),
            ("click_contacts", "contacts"),
            ("click_services", "services"),
            ("click_cases", "cases"),
            ("click_career", "career"),
            ("click_blog", "blog"),
        ],
    )
    def test_navigation_to_sections(
        self, main_page: MainPage, nav_action: str, expected_fragment: str
    ) -> None:
        main_page.open()

        # Dynamically call the click method
        getattr(main_page, nav_action)()

        # Verify URL contains the expected fragment/path
        # This is a basic verification, can be enhanced to check for specific visible elements
        main_page.should_have_url_fragment(expected_fragment)
