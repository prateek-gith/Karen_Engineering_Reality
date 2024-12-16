import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException, WebDriverException

# Function to fetch email from a page using regex
def fetch_email(page_source):
    # Regular expression pattern for matching email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zAZ0-9]{2,}'
    
    # Find all email addresses using the regular expression
    emails = re.findall(email_pattern, page_source)

    if emails:
        return emails[0]  # Return the first email found
    else:
        return None

# Function to handle unexpected alerts (e.g., geolocation prompt)
def handle_alert(driver):
    try:
        # Wait for the alert to be present and dismiss it
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print("Alert detected. Dismissing it.")
        alert.dismiss()  # Dismiss the alert to continue
    except:
        print("No alert present.")

# Initialize the WebDriver
driver = webdriver.Chrome()

# URL of the page
url = 'https://www.dnb.com/business-directory/company-information.residential_building_construction.co.html'
driver.get(url)

# Allow dynamic content to load
driver.maximize_window()
wait = WebDriverWait(driver, 10)
cookie_Recect='truste-consent-required'
clickcoo =wait.until(EC.presence_of_all_elements_located((By.ID, cookie_Recect)))
# wait = WebDriverWait(driver, 10)
if clickcoo:
    clickcoo=driver.find_element(By.ID, cookie_Recect)
    clickcoo.click()


# Create an empty list to store company data
company_data = []

# Function to save data to Excel
def save_data_to_excel(data, filename="company.xlsx"):
    df = pd.DataFrame(data, columns=["Company Name", "Revenue", "Website", "Email"])
    df.to_excel(filename, index=False)

# Loop through pages using pagination
while True:
    try:
        # Wait for the company list to load
        companies = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col-md-12.data')))

        # Iterate over companies by index to avoid stale element references
        for index in range(len(companies)):
            try:
                # Re-fetch the company list to ensure valid references
                companies = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col-md-12.data')))

                item = companies[index]

                # Extract company name and revenue
                company_name = item.find_element(By.CSS_SELECTOR, ".col-md-6 a").text
                revenue = item.find_element(By.CSS_SELECTOR, ".col-md-2.last").text.split("\n")[-1]
                print(f"Company Name: {company_name}")
                print(f"Revenue: {revenue}")

                # Click the company link
                link = item.find_element(By.CSS_SELECTOR, ".col-md-6 a")
                link.click()

                # Wait for the new page to load
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                try:
                    # Handle any unexpected alert (such as geolocation request)
                    # handle_alert(driver)

                    # Wait for the website link to be loaded
                    website_link_element = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//span[@name="company_website"]//a'))
                    )

                    website_url = website_link_element.get_attribute("href")
                    website_link_element.click()

                    # Switch to the new tab (if it opens in a new tab)
                    driver.switch_to.window(driver.window_handles[-1])

                    # Wait for the page to load fully
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                    print(f"Successfully navigated to {website_url}")

                    # Start the email search with a 20-second timeout
                    start_time = time.time()
                    email = None

                    while time.time() - start_time < 10:
                        # Fetch the page source and search for an email
                        page_source = driver.page_source
                        email = fetch_email(page_source)
                        if email:
                            break  # Stop searching if an email is found

                    if email:
                        print(f"Email found: {email}")
                    else:
                        print("No email found within 10 seconds.")
                        email='NA'

                    # Close the new tab and switch back to the original tab
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                except NoSuchElementException:
                    print("Website not present for this company.")
                    website_url = "NA"
                except TimeoutException:
                    print("Timed out while waiting for website link.")
                    website_url = "NA"
                except UnexpectedAlertPresentException:
                    # Handle the unexpected alert when opening the website
                    print("Geolocation alert detected and dismissed.")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    website_url = "NA"
                except WebDriverException as e:
                    print(f"WebDriver exception occurred: {e}")
                    website_url = "NA"
                except Exception as e:
                    print(f"Unexpected error extracting website: {e}")
                    website_url = "NA"

                # Fetch the email if available
                if email is None:
                    email = "NA"

                # Add company data to the list
                company_data.append([company_name, revenue, website_url, email])

                # Save data to Excel after each company
                save_data_to_excel(company_data)

                # Navigate back to the main list
                driver.back()

                # Wait for the main page to reload
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col-md-12.data')))

            except Exception as e:
                print(f"Error processing company at index {index}: {e}")
                # Save the data before continuing or exiting
                save_data_to_excel(company_data)
                break

        # Locate the "Next" button and navigate to the next page
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".next a")
            next_button.click()

            # Wait for the new page content to load
            wait.until(EC.staleness_of(companies[0]))
        except Exception as e:
            print("No more pages to process or next button not found. Exiting.")
            break

    except Exception as e:
        print(f"Error during page processing: {e}")
        # Save the data before exiting
        save_data_to_excel(company_data)
        break  # Exit the loop on errors

# Close the driver
driver.quit()
