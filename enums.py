from enum import Enum


class ReservationEnums(Enum):
    """
    Reservation enum class
    These enums control the input params that are used by the tests
    """
    ADULT_GUESTS = "2"
    CHILD_GUESTS = "1"
    LOCATION = "Tel Aviv-Yafo"
    CHECK_IN_DAY = "30"
    CHECK_IN_MONTH = {"number": "04", "name": "Apr"}
    CHECK_IN_YEAR = "2025"
    CHECK_OUT_DAY = "02"
    CHECK_OUT_MONTH = {"number": "05", "name": "May"}
    CHECK_OUT_YEAR = "2025"

