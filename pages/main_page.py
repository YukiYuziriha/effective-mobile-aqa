import allure
from playwright.sync_api import Page, expect


class MainPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = "https://effective-mobile.ru"

        # Locators using Role Strategy (Best Practice)
        self.nav_about = page.get_by_role("link", name="О нас")  # noqa: RUF001
        self.nav_contacts = page.get_by_role("link", name="Контакты")
        self.nav_services = page.get_by_role("link", name="Услуги")
        self.nav_cases = page.get_by_role("link", name="Кейсы")
        self.nav_career = page.get_by_role("link", name="Карьера")
        self.nav_blog = page.get_by_role("link", name="Блог")

    @allure.step("Open the main page")
    def open(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Click on 'About' navigation link")
    def click_about(self) -> None:
        self.nav_about.first.click()

    @allure.step("Click on 'Contacts' navigation link")
    def click_contacts(self) -> None:
        self.nav_contacts.first.click()

    @allure.step("Click on 'Services' navigation link")
    def click_services(self) -> None:
        self.nav_services.first.click()

    @allure.step("Click on 'Cases' navigation link")
    def click_cases(self) -> None:
        self.nav_cases.first.click()

    @allure.step("Click on 'Career' navigation link")
    def click_career(self) -> None:
        self.nav_career.first.click()

    @allure.step("Click on 'Blog' navigation link")
    def click_blog(self) -> None:
        self.nav_blog.first.click()

    def get_current_url(self) -> str:
        return self.page.url

    @allure.step("Verify URL contains {fragment}")
    def should_have_url_fragment(self, fragment: str) -> None:
        expect(self.page).to_have_url(f".*{fragment}")

    @allure.step("Verify page title or header is visible")
    def should_show_section_title(self, title_text: str) -> None:
        """
        Checks if a heading with the expected text is visible.
        This confirms we actually loaded the content, not just changed URL.
        """
        expect(self.page.get_by_role("heading", name=title_text).first).to_be_visible()
