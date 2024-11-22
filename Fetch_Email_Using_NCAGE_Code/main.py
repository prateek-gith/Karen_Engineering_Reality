from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Path to your Excel file
excel_file = 'Temp_File.xlsx'

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# URL of your local website form
url = 'https://eportal.nspa.nato.int/Codification/CageTool/home'

# Create an empty list to store emails
email_addresses = []

# Read the Excel file
df = pd.read_excel(excel_file)

# Start Code Time
start_Code_Time = time.time()

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    
    # Fetch The Value "Cage_NCAGE" Column  From xlsx File 
    product_name = row['CAGE_NCAGE']
    
    # Check If Any "CAGE_NCAGE" is NaN
    if pd.isna(product_name):
        email_addresses.append("NA")
    else:
        # Sleep For 1 Sec.
        time.sleep(1)

        # Open URL
        driver.get(url)
        
        # Sleep For 2 Sec. For Loading Page
        time.sleep(2)
        
        # Maximize the window
        driver.maximize_window()

        # find The Input Area Till 20 sec.  Where We want to Input Our NCAGE Code
        input_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'inputCageCode')))
        input_element.send_keys(product_name)
        
        
        # Scroll the page after filling the input field
        driver.execute_script("window.scrollBy(0, 300);")  # Scroll down 300px
        
        time.sleep(1)
        
        # Submit the form or Click On The Submit Button
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        try :
            # Find The Detail button Till 20 sec. 
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary.btn-floating.ms-1[title="Details"]')))
            when_click= driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-floating.ms-1[title="Details"]')
        
            # Condition If Find The Detail Button Then Click
            if when_click:
                
                when_click.click()
                
                # Wait until the email link is visible
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/main/div/app-cage-view/app-cage-details/form/app-cage-contact-information/div/div/div/div[3]/div/div/span/a")))
                
                email_element = driver.find_element(By.XPATH, "/html/body/app-root/main/div/app-cage-view/app-cage-details/form/app-cage-contact-information/div/div/div/div[3]/div/div/span/a")
                
                # Extract the email address from the 'href' attribute
                email = email_element.get_attribute("href").replace("mailto:", "")  # Remove 'mailto:' from the link
                
                if email :
                    email_addresses.append(email)  # Append the email to the list
                else:
                    email_addresses.append("NA")  # Append the email to the list
         
        except Exception as e:
            email_addresses.append("NAN")  # Append 'NA' if something goes wrong (timeout, element not found, etc.)
            print(f"Error for CAGE code {product_name}: {e}")



df['Contact Email'] = email_addresses


# Load the existing workbook to avoid overwriting it
# Create a new sheet (Sheet2)
with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
    df.to_excel(writer, sheet_name='Sheet2', index=False)


# Close the browser after completing the task
driver.quit()

end_code_time = time.time()

time_teke = end_code_time - start_Code_Time

# Convert the total time to hours, minutes, and seconds
hours = int(time_teke // 3600)  # 1 hour = 3600 seconds
minutes = int((time_teke % 3600) // 60)  # 1 minute = 60 seconds
seconds = int(time_teke % 60)

print(f"When Code Star : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_Code_Time))}")
print(f"When Code End : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_code_time))}")
print(f"Total time Take The Code : {hours:02}:{minutes:02}:{seconds:02}")