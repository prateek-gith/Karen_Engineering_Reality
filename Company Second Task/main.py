from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import os
import sys

@dataclass
class Business:
    """Holds business data"""
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None

@dataclass
class BusinessList:
    """Holds list of Business objects, and saves to both Excel and CSV"""
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        """Transform business_list to pandas dataframe"""
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="_")


    def save_to_excel(self, filename):
        """Saves pandas dataframe to Excel (XLSX) file"""
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"{self.save_at}/{filename}.xlsx", index=False)
        
    def append_unique(self, business):
        self.business_list.append(business)
        return True



def main():
    
    search_list = []
    input_file_name = 'input.txt'
    input_file_path = os.path.join(os.getcwd(), input_file_name)
    if os.path.exists(input_file_path):
        with open(input_file_path, 'r') as file:
            search_list = file.readlines()
    if len(search_list) == 0:
        print('Error occurred: You must either pass the -s search argument, or add searches to input.txt')
        sys.exit()

    total =  5  # Default to 1000 if no total provided


    # Scraping
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(5000)  # Dev wait, can be removed

        for search_for_index, search_for in enumerate(search_list):
            search_for = search_for.strip()
            print(f"{search_for_index} - {search_for}")

            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.wait_for_timeout(3000)

            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)

            # Load existing data to check for duplicates
            business_list = BusinessList()
            # existing_data = business_list.load_existing_data(f"google_maps_data_{search_for.replace(' ', '_')}")

            # Scroll and scrape logic
            scraped_urls = set()
            previous_count = 0

            while len(business_list.business_list) < total:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()

                # If the count of listings hasn't changed, break the loop
                current_count = len(listings)
                print(f"The Count is: {current_count}")
                if current_count == previous_count:
                    print(f"No more listings found for {search_for}. Stopping.")
                    break

                previous_count = current_count

                for listing in listings:
                    listing_url = listing.get_attribute('href')
                    if listing_url in scraped_urls:
                        continue

                    try:
                        listing.click()
                        page.wait_for_timeout(10000)

                        name_xpath = '//h1[contains(@class, "DUwDvf")]'
                        address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                        website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                        phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'

                        business = Business()

                        if page.locator(name_xpath).count() > 0:
                            business.name = page.locator(name_xpath).first.inner_text()
                            print(f"Business Name: {business.name}")

                        if page.locator(address_xpath).count() > 0:
                            business.address = page.locator(address_xpath).first.inner_text()
                        if page.locator(website_xpath).count() > 0:
                            business.website = page.locator(website_xpath).first.inner_text()
                        if page.locator(phone_number_xpath).count() > 0:
                            business.phone_number = page.locator(phone_number_xpath).first.inner_text()

                        scraped_urls.add(listing_url)
                        
                        if not business_list.append_unique(business):
                            continue
                        
                        if len(business_list.business_list) >= total:
                            break

                    except Exception as e:
                        print(f'Error occurred: {e}')
                
                # Scroll down
                page.mouse.wheel(0, 30000)
                print("Now Scrolling")
                page.wait_for_timeout(10000)

            
            # Output
            
            business_list.save_to_excel(f"google_maps_data_{search_for.replace(' ', '_')}")

        browser.close()

if __name__ == "__main__":
    main()
