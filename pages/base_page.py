from playwright.sync_api import Page


class BasePage:
    """
    Base page class
    """
    def __init__(self, page: Page):
        self.page = page
