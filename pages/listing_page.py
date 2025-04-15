from pages.base_page import BasePage


class ListingPage(BasePage):
    """
    Apartment listing page class
    """

    # Saves the listing details and prints them to console
    def save_and_print_listing_details(self):
        # Save listing details
        title = self.page.locator('h2').first.text_content() or "N/A"
        rating_text = self.page.locator('span:has-text("Rated")').first.text_content() or "N/A"
        guests_info = self.page.locator('ol > li').all_text_contents()
        guests_summary = " · ".join([info.strip() for info in guests_info])
        reviews = self.page.locator('a[href*="/reviews"]').first.text_content() or "N/A"

        # Print listing details
        print("Listing Details:")
        print(title)
        print(f"Rating: {rating_text}")
        print(f"Info: {guests_summary}")
        print(f"Reviews: {reviews}")

    # Clicks reserve button and asserts reservation page was loaded
    def click_reserve_button(self):
        # Click reserve button
        self.page.get_by_role("button", name="Reserve").click()

        # Assert button was clicked
        trip_heading = self.page.locator('h2', has_text="Your trip")
        trip_heading.wait_for(state="visible", timeout=5000)
        assert trip_heading.is_visible(), "'Your trip' heading was not displayed after clicking Reserve."

    # Closes popup window that might appear (popup window of translation settings)
    def click_close_button_if_exists(self):
        # Locate 'close' button
        close_btn = self.page.locator('button[aria-label="Close"]')

        # Attempt to click "close" button if it exists
        try:
            close_btn.wait_for(timeout=3000)
            close_btn.click()
        except:
            print("Close button not found.")

