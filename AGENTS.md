# agents.md — AQA UI Test Project Guardrails

This document defines **non-negotiable rules** for working on this project with AI assistants.
The goal: **small, readable, boringly reliable** automation around `https://effective-mobile.ru`.

---

## 1. Project Scope & Tech Stack

**Scope for now**

- UI tests for the main page of `https://effective-mobile.ru`
- Navigation checks: clicking menu blocks → correct section / URL

**Stack**

- Python **3.10**
- `pytest`
- `pytest-playwright` (Playwright sync API)
- `allure-pytest`
- Docker (run tests in container)
- OS: assume Linux-compatible environment

**AI Rule:**  
Do **not** introduce new libraries, frameworks, or tools without an explicit instruction in the prompt.

---

## 2. Project Structure (File & Module Guardrails)

Target structure (can be expanded, but not randomly changed):

```text
project_root/
  pages/
    main_page.py
  tests/
    test_main_page_navigation.py
  conftest.py
  requirements.txt
  Dockerfile
  pytest.ini
  README.md
  agents.md
````

**Rules**

- All **UI interaction logic** lives in `pages/` as Page Objects.
    
- **No direct calls** to Playwright `page` in tests, except via Page Objects.
    
- New pages/components → new file in `pages/`, not stuffed into `main_page.py`.
    
- `conftest.py`:
    
    - Contains fixtures for browser, page, and Page Objects.
        
    - Contains **shared** test utilities only (e.g., hooks, screenshots on failure).
        
    - No business logic here.
        

---

## 3. Python & Code Style Guardrails

- Follow **PEP8-ish** style, but readability > strictness.
    
- Use **type hints** where not annoying:
    
    ```python
    def click_about(self) -> None: ...
    ```
    
- Use **explicit names**, even if longer:
    
    - ✅ `click_contacts_link()`
        
    - ❌ `click_c()`
        
- One responsibility per function/method.
    
- No clever one-liners that are hard to read.
    

**Patterns to avoid**

- No global mutable state.
    
- No complex logic in decorators.
    
- No “utility god modules” that do everything.
    

---

## 4. Page Object Model Guardrails

Every Page Object:

- Represents **one logical page** or area.
    
- Is responsible for:
    
    - URL (if applicable).
        
    - Locators.
        
    - Low-level actions (click, fill, etc.).
        
    - Small “assertion helpers” (e.g. `should_see_section`).
        

Example skeleton:

```python
from playwright.sync_api import Page, Locator

class MainPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = "https://effective-mobile.ru"

        # Locators
        self.nav_about: Locator = page.locator("text=О нас")
        self.nav_contacts: Locator = page.locator("text=Контакты")
        # ...

    def open(self) -> None:
        self.page.goto(self.url)

    def click_about(self) -> None:
        self.nav_about.click()

    def should_be_at_about_section(self) -> None:
        # assert visible section, or URL fragment, etc.
        ...
```

**Rules**

- No direct `page.locator("...")` inside tests. All locators are defined in the Page Object.
    
- Page Object methods should be **small and explicit**:
    
    - `click_about()`, `click_contacts()`, `scroll_to_section()`.
        
- If something requires more than ~15–20 lines, split it.
    

---

## 5. Locator Strategy Guardrails

Goal: **Stable, readable selectors**. Prefer semantics over fragile CSS paths.

Priority order (from best to worst):

1. **Test-friendly attributes** if they exist:
    
    - `data-testid`, `data-qa`, etc. (if present)
        
2. **Accessible text / role-based selectors**:
    
    - `page.get_by_role("link", name="О нас")`
        
    - `page.get_by_text("Контакты")`
        
3. Reasonable CSS with clear semantics:
    
    - `.header-nav a[href="#about"]`
        
4. As a last resort: positional or deeply nested selectors.
    

**Hard bans**

- ❌ Absolute XPaths like `/html/body/div[1]/div[2]/ul/li[3]/a`
    
- ❌ Selectors tied to random build hashes (e.g. `.css-1a2b3c`).
    
- ❌ Overly generic selectors (`"a"`, `"div"`, `"span"`) without context.
    

**AI Rule:**  
When generating locators, always explain in a code comment **why** this locator is chosen if it’s non-trivial or slightly brittle.

---

## 6. Test Design Guardrails

### 6.1. Test Structure

- Tests are **short** and **readable**.
    
- Use pytest **parametrization** for similar cases (navigation items).
    

Example:

```python
import pytest

 @pytest.mark.parametrize(
    "menu_name, expected_fragment",
    [
        ("about", "#about"),
        ("contacts", "#contacts"),
        # ...
    ],
)
def test_navigation_to_sections(main_page, menu_name, expected_fragment):
    main_page.open()
    main_page.click_menu(menu_name)
    main_page.should_be_at_section(expected_fragment)
```

### 6.2. Assertions

- Assertions should be **business-meaningful**, not low-level:
    
    - ✅ `main_page.should_be_at_contacts_section()`
        
    - ❌ `assert page.url == "..."` sprinkled everywhere.
        
- If assertion fails, the message should help debugging.
    

### 6.3. Flakiness Guardrails

- No `time.sleep()` unless absolutely unavoidable and justified in a comment.
    
- Use Playwright waiting mechanisms:
    
    - `locator.wait_for()`
        
    - Assertions that wait internally (`expect(locator).to_be_visible()` if we pull that in).
        
- Don’t assert on elements **before** they have a chance to appear.
    

---

## 7. Fixtures & Test Infrastructure Guardrails

**`conftest.py` responsibilities:**

- Browser and context fixtures:
    
    - Headed/headless can be controlled via CLI options / env vars.
        
- `Page` fixture.
    
- Page Object fixture:
    
    ```python
    @pytest.fixture
    def main_page(page: Page) -> MainPage:
        return MainPage(page)
    ```
    

**Rules**

- Fixtures should be **thin**. Heavy logic → helper functions or utilities.
    
- No cross-imports from `tests/` into `pages/`.
    
- No hidden side-effects in fixtures (e.g., random navigation).
    

---

## 8. Allure Reporting Guardrails

**Goals**

- Reports must tell a story: “What was tested, what steps were taken, what failed?”
    

**Rules**

- Use decorators where it improves clarity, not everywhere:
    
    ```python
    import allure
    
    @allure.feature("Main Page Navigation")
    @allure.story("Navigation via header menu")
    def test_navigation_to_sections(...):
        ...
    ```
    
- Use ` @allure.step` for composite methods or test steps, if it makes the report more readable.
    
- On failure:
    
    - Attach screenshot.
        
    - Optionally attach page source.
        
    
    Example (in fixture or hook):
    
    ```python
    import allure
    
    if request.node.rep_call.failed:
        allure.attach(
            page.screenshot(full_page=True),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    ```
    

**AI Rule:**  
When generating tests, ensure they are Allure-friendly (clear names, proper `feature`/`story`), but do not spam with unnecessary annotations.

---

## 9. Docker & Environment Guardrails

**Dockerfile goals:**

- Reproducible environment for running tests.
    
- Minimal steps, but not “clever”.
    

**Rules**

- Base image: official `python:3.10` (or slim variant if explicitly requested).
    
- Steps:
    
    1. Set `WORKDIR`.
        
    2. Copy `requirements.txt` and install dependencies.
        
    3. Install Playwright browsers (`playwright install`).
        
    4. Copy the rest of the project.
        
    5. Default CMD runs tests with Allure results, e.g.:
        
        ```dockerfile
        CMD ["pytest", "--alluredir=allure-results"]
        ```
        
- No hardcoded machine-specific paths.
    
- No secret tokens or env vars baked into the image.
    

---

## 10. README & Developer Experience Guardrails

`README.md` must include:

1. **Project description** (1–2 short paragraphs).
    
2. **Local setup**:
    
    - Clone repo
        
    - Create venv
        
    - `pip install -r requirements.txt`
        
    - `playwright install`
        
3. **How to run tests locally**:
    
    - `pytest`
        
    - `pytest --alluredir=allure-results`
        
4. **How to run via Docker**:
    
    - `docker build -t effective-mobile-tests .`
        
    - `docker run --rm effective-mobile-tests`
        
5. **How to view Allure report**:
    
    - `allure serve allure-results` (if available locally).
        

**AI Rule:**  
When updating tests or structure, update `README.md` to match reality.

---

## 11. AI Collaboration Rules

These are **hard constraints** for any AI assistant working on this repo:

1. **Do not touch `agents.md`** unless explicitly requested.
    
2. **Do not refactor the whole project** “for cleanliness” without request.
    
3. Before generating code:
    
    - Respect existing file structure.
        
    - Reuse existing patterns (fixture style, naming, locator strategy).
        
4. When in doubt:
    
    - Favor **simpler** code over “smart” abstractions.
        
5. Always:
    
    - Add minimal comments when something is non-obvious (e.g., fragile locator, tricky wait).
        
    - Avoid magic constants without explanation.
        

**If a generated change conflicts with these guardrails, the guardrails win.**
