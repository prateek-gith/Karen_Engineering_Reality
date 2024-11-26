from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import os
import sys
import re
from urllib.parse import urlparse



opera_path = 'C:\\Users\\hr21k\\AppData\\Local\\Programs\\Opera\\opera.exe'


@dataclass
class Business:
    """Holds business data"""
    name: str = None
    email: str = None
    website: str = None

@dataclass
class BusinessList:
    """Holds list of Business objects, and saves to both Excel and CSV"""
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output3'

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

def extract_email_from_website(page):
    """Try to extract the email from the business website"""
    email = None
    # Look for mailto links or any visible email on the page
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    
    try:
        # Check for "mailto" links on the page
        mailtos = page.locator('a[href^="mailto:"]').all()
        if mailtos:
            email = mailtos[0].get_attribute("href").replace("mailto:", "")
        else:
            # If no mailto link, search the page text for an email pattern
            page_content = page.content()
            email_matches = re.findall(email_pattern, page_content)
            if email_matches:
                email = email_matches[0]
    except Exception as e:
        print(f"Error extracting email from website: {e}")

    return email if email else "NA"

def validate_and_format_website(website_url):
    """Ensure the website URL is valid and properly formatted (prepend https:// if missing)"""
    if not website_url:
        return None

    # Check if the URL already has a scheme (http:// or https://)
    parsed_url = urlparse(website_url)
    if not parsed_url.scheme:
        # If no scheme is present, prepend https://
        website_url = f"https://{website_url}"

    return website_url

def main():
    search_list = []
    input_file_name = 'in.txt'
    input_file_path = os.path.join(os.getcwd(), input_file_name)
    
    if os.path.exists(input_file_path):
        with open(input_file_path, 'r') as file:
            search_list = file.readlines()

    if len(search_list) == 0:
        print('Error occurred: You must either pass the -s search argument, or add searches to input.txt')
        sys.exit()

    total = 200  

    # Scraping
    with sync_playwright() as p:
        
        browser = p.chromium.launch(executable_path=opera_path, headless=False)
        # browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)

        for search_for_index, search_for in enumerate(search_list):
            search_for = search_for.strip()
            print(f"{search_for_index} - {search_for}")

            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)

            # Load existing data to check for duplicates
            business_list = BusinessList()

            # Scroll and scrape logic
            scraped_urls = set()
            previous_count = 0

            while len(business_list.business_list) < total:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()

                # Check if there are any listings, and break if not
                current_count = len(listings)
                print(f"The Count is: {current_count}")
                if current_count == 0:
                    print(f"No listings found for {search_for}. Stopping.")
                    break

                # If the count of listings hasn't changed, break the loop
                if current_count == previous_count:
                    print(f"No more listings found for {search_for}. Stopping.")
                    break

                previous_count = current_count

                for listing in listings:
                    try:
                        # Get the href of the listing
                        listing_url = listing.get_attribute('href')

                        if not listing_url or listing_url in scraped_urls:
                            continue

                        listing.click()
                        page.wait_for_timeout(2000)

                        name_xpath = '//h1[contains(@class, "DUwDvf")]'
                        website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'

                        business = Business()

                        if page.locator(name_xpath).count() > 0:
                            business.name = page.locator(name_xpath).first.inner_text()
                            print(f"Business Name: {business.name}")

                        if page.locator(website_xpath).count() > 0:
                            business.website = page.locator(website_xpath).first.inner_text()

                        # Validate the website URL (ensure it is a valid URL)
                        business.website = validate_and_format_website(business.website)

                        # Extract email from Google Maps page, if present
                        email_xpath = '//button[contains(@data-item-id, "email:mailto:")]//div[contains(@class, "fontBodyMedium")]'
                        if page.locator(email_xpath).count() > 0:
                            business.email = page.locator(email_xpath).first.inner_text()
                            print(f"Email from Google Maps: {business.email}")
                        else:
                            # If email not found, go to the business website and search for it
                            if business.website:
                                try:
                                    # Open the business website in a new tab
                                    new_tab = browser.new_page()
                                    new_tab.goto(business.website)
                                    new_tab.wait_for_timeout(5000)
                                    business.email = extract_email_from_website(new_tab)
                                    print(f"Email from website: {business.email}")
                                    new_tab.close()  # Close the tab after checking the website
                                except Exception as e:
                                    print(f"Error navigating to website {business.website}: {e}")
                                    business.email = "NA"
                            else:
                                business.email = "NA"

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
                page.wait_for_timeout(5000)

            # Output
            business_list.save_to_excel(f"google_maps_data_{search_for.replace(' ', '_')}")

        browser.close()

if __name__ == "__main__":
    main()
