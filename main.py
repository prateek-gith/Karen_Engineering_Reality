import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file (for secure access to email credentials)
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


# Configure logging to track activity and errors; saves logs to email_logs.log
logging.basicConfig(level=logging.INFO, filename='email_logs.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Load data from Excel files into pandas DataFrames    
def load_excel_data(contractors_file, opportunities_file):
    try:
        contractors_df = pd.read_excel(contractors_file)
        opportunities_df = pd.read_excel(opportunities_file)
        return contractors_df, opportunities_df
    except Exception as e:
        logging.error(f"Error loading Excel files: {e}")
        raise


# Filter the Data Based On  NAIC Code & Country
def filter_opportunities(contractor, opportunities_df):
    
    filtered_opps = opportunities_df[
        (opportunities_df['NAICS Code'] == contractor['NAICS Code']) &
        (opportunities_df['Country'] == contractor['Country'])
    ]
    return filtered_opps


# Create A Email Template
def create_email_content(contractor, opportunities):
     
    greeting = f"Hello {contractor['Name']},\n\n"
    intro = "Here are some new business opportunities that match your profile:\n\n"
    
    # Build a list of opportunities to include in the email
    opp_list = ""
    for index, opp in opportunities.iterrows():
        opp_list += f"- {opp['Opportunity Title']}: {opp['Description']} (Location: {opp['Location']})\n"
    
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
        
        logging.info(f"Email sent to {recipient}")
        
    except Exception as e:
        logging.error(f"Failed to send email to {recipient}: {e}")


def main():
    contractors_file = 'contractors.xlsx'               # Path to contractors Excel file
    opportunities_file = 'opportunities.xlsx'           # Path to opportunities Excel file
    
    # Load contractors and opportunities data
    contractors_df, opportunities_df = load_excel_data(contractors_file, opportunities_file)
    
    # Process each contractor to find relevant opportunities and send emails
    for Index, contractor in contractors_df.iterrows():
        relevant_opps = filter_opportunities(contractor, opportunities_df)
        
        # If relevant opportunities exist, send an email; otherwise, log no matches
        if not relevant_opps.empty:
            email_content = create_email_content(contractor, relevant_opps)
            send_email(contractor['Email'], "New Business Opportunities for You", email_content)
        else:
            logging.info(f"No matching opportunities for {contractor['Name']}.")

if __name__ == "__main__":
    main()
