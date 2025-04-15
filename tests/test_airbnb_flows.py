from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.listing_page import ListingPage
from pages.reservation_page import ReservationPage


def test_airbnb_search(page):
    home = HomePage(page)
    search = SearchResultsPage(page)

    # Step 1: Perform search flow
    home.go_to_homepage()
    home.enter_location()
    home.select_dates()
    home.select_guests()
    home.search_locations()

    # Step 2: Validate that search parameters were applied correctly
    search.validate_search_params()

    # Step 3: Get listings
    search.get_listings()

    # Step 4: Find the best-rated and cheapest listings
    best_listing, best_rating = search.get_highest_rated()
    cheapest_listing, cheapest_price = search.get_cheapest()

    # Step 5: Assert results were found
    assert best_listing is not None, "No highest-rated listing found"
    assert cheapest_listing is not None, "No cheapest listing found"

    # Step 6: Print extracted details
    search.log_details(best_listing, f"Highest Rated Listing: (★ {best_rating})")
    search.log_details(cheapest_listing, f"Cheapest Listing (₪ {cheapest_price} total)")


def test_airbnb_reservation(page):
    home = HomePage(page)
    search = SearchResultsPage(page)
    listing = ListingPage(page)
    reservation = ReservationPage(page)

    # Step 1: Perform search flow
    home.go_to_homepage()
    home.enter_location()
    home.select_dates()
    home.select_guests(include_children=True)
    home.search_locations()

    # Step 2: Validate that search parameters were applied correctly
    search.validate_search_params(include_children=True)

    # Step 3: Get listings
    search.get_listings()

    # Step 4: Find the best-rated listing
    best_listing, best_rating = search.get_highest_rated()

    # Step 5: Assert result was found
    assert best_listing is not None, "No highest-rated listing found"

    # Step 6: Click on top-rated listing and print details
    search.click_top_rated_listing(listing=best_listing)
    listing.click_close_button_if_exists()
    listing.save_and_print_listing_details()

    # Step 7: Attempt to start reservation
    listing.click_reserve_button()
    reservation.validate_reservation_details()
    reservation.enter_phone_number()
