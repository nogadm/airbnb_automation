from enums import ReservationEnums
from pages.base_page import BasePage


class ReservationPage(BasePage):
    """
    Reserve listing page class
    """

    # Validates the guest and date details on the reservation page
    def validate_reservation_details(self):
        # Locate the elements containing the selected date and guest information
        date_text = self.page.locator('div:below(h3:has-text("Dates"))').first
        guests_text = self.page.locator('div:below(h3:has-text("Guests"))').first

        # Extract and clean the actual displayed values
        actual_dates = date_text.text_content().strip() if date_text else ""
        actual_guests = guests_text.text_content().strip() if guests_text else ""

        # Build the expected date string based on enum values
        check_out_month = ReservationEnums.CHECK_OUT_MONTH.value['name'] \
            if ReservationEnums.CHECK_OUT_MONTH != ReservationEnums.CHECK_IN_MONTH else ''
        expected_dates = f"{ReservationEnums.CHECK_IN_MONTH.value['name']} " \
                         f"{ReservationEnums.CHECK_IN_DAY.value.lstrip('0')}" \
                         f" – {check_out_month} {ReservationEnums.CHECK_OUT_DAY.value.lstrip('0')}"

        # Build the expected guest count string
        expected_guests = \
            f'{int(ReservationEnums.ADULT_GUESTS.value) + (int(ReservationEnums.CHILD_GUESTS.value))} guests'

        # Normalize both expected and actual date strings for reliable comparison
        expected_dates = self.normalize_date_text(expected_dates)
        actual_dates = self.normalize_date_text(actual_dates)

        # Assert that the displayed info matches the expected info
        assert expected_dates in actual_dates, f"Expected dates '{expected_dates}', got '{actual_dates}'"
        assert expected_guests in actual_guests, f"Expected guests '{expected_guests}', got '{actual_guests}'"

    # Enters phone number in phone input box and Asserts
    def enter_phone_number(self, phone: str = "0540000000"):
        # Fill phone number input
        phone_input = self.page.locator('input[data-testid="login-signup-phonenumber"]')
        phone_input.fill(phone)

        # Assert the phone was typed
        typed_value = phone_input.input_value()
        assert typed_value == phone, f"Expected phone number '{phone}', but got '{typed_value}'"

    # Replaces special dashes and spaces with standard ones for reliable comparison
    def normalize_date_text(self, text):
        import re
        text = re.sub(r'[–—−]', '-', text)
        text = re.sub(r'[\u2009\u00A0]', ' ', text)
        return text.strip()
