# Airbnb Test Automation Framework

This project is a test automation framework built with Python, Playwright, and Pytest, using the Page Object Model (POM) design pattern.

The framework automates Airbnb search and reservation flows, including validation of search parameters, listing analysis, and reservation behavior. It is structured for scalability and maintainability, with reusable page objects and clean test logic.

## Structure
- pages/ - Contains reusable page classes for different parts of the Airbnb site (home, search results, listing, reservation).
- tests/ - Contains the test scenarios written using Pytest.
- enums.py - Contains the input parameters used by the tests.
- requirements.txt - Lists the Python dependencies.
- conftest.py - Defines shared test fixtures.


## How to Run the Tests on Windows (Command Prompt or PowerShell) from the Project Root Folder

### Step 1: Create a virtual environment
    python -m venv venv

### Step 2: Activate the virtual environment
    .\venv\Scripts\activate

### Step 3: Install dependencies
    pip install -r requirements.txt

### Step 4: Install playwright 
    playwright install

### Step 5: Run the tests
    pytest tests/test_airbnb_flows.py

## Tools Used
- Playwright for browser automation
- Pytest as the test runner
- Page Object Model for clean test architecture

