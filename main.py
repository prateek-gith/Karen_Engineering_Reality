import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file (for secure access to email credentials)
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


# Read data from Excel files  
def read_excel_data(file):
    try:
        Nfile = pd.read_excel(file)
        return Nfile
    except Exception as e:
        with open("log.txt", 'a') as f:
            f.write(f"Error loading Excel files: {str(e)}\n")


# Filter the Data Based On  NAICS Code & Country
def filter_opportunities(contractor, opportunities_df):
    filtered_opps =[]
    
    for index, row in opportunities_df.iterrows():
        if row['NAICS_Code'] == contractor['NAICS_Code'] and row['Country'] == contractor['Country']:
            filtered_opps.append(row)
    
    return filtered_opps


# Create A Email Template
def email_message(contractor, opportunities):
     
    greeting = f"Hello {contractor['Name']},\n\n"
    intro = "Here are some new business opportunities that match your profile:\n\n"
    
    # Build a list of opportunities to include in the email
    opp_list = ""
    for opp in opportunities:
        opp_list = opp_list + f"- {opp['Opportunity Title']}: {opp['Description']} (Location: {opp['Location']})\n"
    
    closing = "\nBest regards,\nYour Business Opportunities Team"
    return greeting + intro + opp_list + closing


# Send Mail To Contractor
def send_email(recipient, subject, content):
    try:
        # Prepare the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))
        
        # Use SSL for secure connection to the SMTP server
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send the email
        smtp_server.send_message(msg)
        
        smtp_server.quit()
        
        with open("log.txt", 'a') as f:
            f.write(f"{time.asctime(time.localtime(time.time()))}, Email sent to {recipient}\n")
        
    except Exception as e:
        with open("log.txt", 'a') as f:
            f.write(f"{time.asctime(time.localtime(time.time()))},  Failed to send email to {recipient}: {e}\n")



if __name__ == "__main__":
    
    contractors_file = 'contractors.xlsx'               # Path to contractors Excel file
    opportunities_file = 'opportunities.xlsx'           # Path to opportunities Excel file
    
    # Load contractors and opportunities data
    contractors_df = read_excel_data(contractors_file)
    opportunities_df = read_excel_data(opportunities_file)
    
    # Process each contractor to find relevant opportunities and send emails
    for index, contractor in contractors_df.iterrows():
        relevant_opps = filter_opportunities(contractor, opportunities_df)
        
        # If relevant opportunities exist, send an email
        if relevant_opps:
            email_content = email_message(contractor, relevant_opps)
            send_email(contractor['Email'], "New Business Opportunities for You", email_content)
        else:
            with open("log.txt", 'a') as f:
                f.write(f"No matching opportunities for {contractor['Name']}.")
