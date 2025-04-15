from enums import ReservationEnums
from pages.base_page import BasePage
from playwright.sync_api import expect


class HomePage(BasePage):
    """
    Airbnb home page class
    """

    # Navigates to the Airbnb homepage
    def go_to_homepage(self):
        self.page.goto("https://www.airbnb.com")
        expect(self.page.get_by_placeholder("Search destinations")).to_be_visible()

    # Enters a location into the search field and selects the suggested result
    def enter_location(self, location: str = ReservationEnums.LOCATION.value):
        self.page.get_by_placeholder("Search destinations").click()
        self.page.get_by_placeholder("Search destinations").fill(location)
        self.page.get_by_text(location, exact=True).click()

        # Asserts the expected location is shown
        location_value = self.page.get_by_test_id("structured-search-input-field-query").get_attribute("value")
        assert location in location_value

    # Opens the guest selector and selects the number of adults
    def select_guests(self, adults=ReservationEnums.ADULT_GUESTS.value, children=ReservationEnums.CHILD_GUESTS.value,
                      include_children=False):
        self.page.get_by_text("Who").click()
        for _ in range(int(adults)):
            self.page.get_by_test_id("stepper-adults-increase-button").click()
        if include_children:
            for _ in range(int(children)):
                self.page.get_by_test_id("stepper-children-increase-button").click()

        # Asserts the expected number of guests is shown
        number_of_guests = int(adults) + (int(children) if include_children else 0)
        expect(self.page.get_by_test_id("structured-search-input-field-guests-button")) \
            .to_contain_text(f"{number_of_guests} guest" if number_of_guests == 1 else f"{number_of_guests} guests")

    # Selects check-in and check-out dates
    def select_dates(self):
        self.page.wait_for_timeout(1000)

        # Selects dates
        search_check_in_date = \
            f'{ReservationEnums.CHECK_IN_YEAR.value}-{ReservationEnums.CHECK_IN_MONTH.value["number"]}' \
            f'-{ReservationEnums.CHECK_IN_DAY.value}'
        search_check_out_date = \
            f'{ReservationEnums.CHECK_OUT_YEAR.value}-{ReservationEnums.CHECK_OUT_MONTH.value["number"]}' \
            f'-{ReservationEnums.CHECK_OUT_DAY.value}'
        self.page.locator(f'button[data-state--date-string="{search_check_in_date}"]').click()
        self.page.locator(f'button[data-state--date-string="{search_check_out_date}"]').click()

        # Asserts the expected dates are shown
        expected_checkin = \
            f'{ReservationEnums.CHECK_IN_MONTH.value["name"]} {ReservationEnums.CHECK_IN_DAY.value.lstrip("0")}'
        expected_checkout = \
            f'{ReservationEnums.CHECK_OUT_MONTH.value["name"]} {ReservationEnums.CHECK_OUT_DAY.value.lstrip("0")}'
        expect(self.page.get_by_test_id("structured-search-input-field-split-dates-0")
               .get_by_text(expected_checkin, exact=True)).to_be_visible()
        expect(self.page.get_by_test_id("structured-search-input-field-split-dates-1")
               .get_by_text(expected_checkout, exact=True)).to_be_visible()

    # Clicks the search button to execute the search
    def search_locations(self):
        self.page.get_by_role("button", name="Search").click()
