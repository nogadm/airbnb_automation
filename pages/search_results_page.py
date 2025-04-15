import re
from enums import ReservationEnums
from pages.base_page import BasePage
from playwright.sync_api import expect


class SearchResultsPage(BasePage):
    """
    Listing results page class
    """
    listings = None

    # Validates location, dates and guests parameters are displayed with the expected value
    def validate_search_params(self, include_children: bool = False):
        expect(self.page.get_by_test_id("little-search-location").locator("div")) \
            .to_have_text(ReservationEnums.LOCATION.value)

        number_of_guests = int(ReservationEnums.ADULT_GUESTS.value) \
                           + (int(ReservationEnums.CHILD_GUESTS.value) if include_children else 0)
        expect(self.page.get_by_test_id("little-search-guests")).to_contain_text(str(number_of_guests))

        check_out_month = ReservationEnums.CHECK_OUT_MONTH.value['name'] \
            if ReservationEnums.CHECK_OUT_MONTH != ReservationEnums.CHECK_IN_MONTH else ''
        dates = f"{ReservationEnums.CHECK_IN_MONTH.value['name']} {ReservationEnums.CHECK_IN_DAY.value.lstrip('0')}" \
                f" – {check_out_month} {ReservationEnums.CHECK_OUT_DAY.value.lstrip('0')}"
        expect(self.page.get_by_test_id("little-search-anytime").locator("div")).to_have_text(dates)

    # Gets all listings in the executed search
    def get_listings(self):
        self.listings = []
        self.page.wait_for_timeout(2000)

        # Iterate over all available pages of the current search
        next_button = self.page.locator('a[aria-label="Next"]')
        while next_button.is_visible():
            self._collect_current_page_listings()
            next_button.click()
            self.page.wait_for_timeout(3000)
            next_button = self.page.locator('a[aria-label="Next"]')
        self._collect_current_page_listings()

    # Collect listings of the current page
    def _collect_current_page_listings(self):
        current_listings = self.page.locator('[itemprop="itemListElement"]')
        for i in range(current_listings.count()):
            self.listings.append(current_listings.nth(i))

    # Iterates over all listings and returns the top-rated one
    def get_highest_rated(self):
        highest_rating = 0.0
        best_listing = None

        for listing in self.listings:
            # Locate the element that contains the rating text
            rating_locator = listing.locator('text=/out of 5 average rating/')

            if rating_locator.count() > 0:
                rating_text = rating_locator.first.text_content()
                match = re.search(r"(\d+\.\d+)", rating_text)
                if match:
                    rating = float(match.group(1))
                    if rating > highest_rating:
                        highest_rating = rating
                        best_listing = listing

        return best_listing, highest_rating

    # Iterates over all listings and returns the one with the cheapest total price
    def get_cheapest(self):
        lowest_price = float("inf")
        cheapest_listing = None

        for listing in self.listings:
            # Look for the total price
            price_locator = listing.locator('span[aria-hidden="true"]:has-text("total")')

            if price_locator.count() > 0:
                price_text = price_locator.first.text_content()

                if price_text:
                    # Extract the numeric value
                    match = re.search(r"[\d,]+", price_text)
                    if match:
                        price_str = match.group(0).replace(",", "")
                        price = int(price_str)

                        if price < lowest_price:
                            lowest_price = price
                            cheapest_listing = listing

        return cheapest_listing, lowest_price

    # Prints to console the information of the selected listing
    def log_details(self, listing, label: str):
        try:
            title = listing.locator('[data-testid="listing-card-title"]').text_content(timeout=10000)
            description = listing.locator('[data-testid="listing-card-name"]').text_content(timeout=10000)
            url = listing.locator('meta[itemprop="url"]').get_attribute("content")
            print(f"{label}: "
                  f"{title.strip() if title else 'Unknown'} "
                  f"({description.strip() if description else 'Unknown'}), "
                  f"\nlink: {url.strip() if url else 'Unknown'}")
        except Exception as e:
            print(f"{label}: Failed to get listing info, Error: {e}")

    # Moves to top-rated listing page
    def click_top_rated_listing(self, listing):
        # Extract href from the given listing
        target_href = listing.locator('meta[itemprop="url"]').get_attribute("content")
        if target_href:
            if not target_href.startswith("http"):
                target_href = f"https://{target_href}"
            self.page.goto(target_href, wait_until="load")
