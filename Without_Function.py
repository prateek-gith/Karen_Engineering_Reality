import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




Con_file = pd.read_excel('contractors.xlsx')
Opp_file = pd.read_excel('opportunities.xlsx')


for  i, Con_name in Con_file.iterrows():
    newapp=""
    for j, Opp_Name in Opp_file.iterrows():
        if Con_name['NAICS_Code'] == Opp_Name['NAICS_Code'] and Con_name['Country']== Opp_Name['Country']:
            a= f"{Opp_Name['Opportunity Title']}: {Opp_Name['Description']} (Location: {Opp_Name['Location']})\n"
            newapp = newapp + a
    
    if newapp:
        recep_name=Con_name['Name']
        receiver_address = Con_name['Email']
        message=newapp
        subject="New Business Opportunities for You"
        closing = "\nBest regards,\nYour Business Opportunities Team"
        mail_content=f""" Dear Sir{recep_name}\n
        Here are some new business opportunities that match your profile:\n
        - {message}
        {closing}
        """
        sender_address = "mail_address"
        password = "password_passkey"
        
        
        # Prepare the email message
        msg = MIMEMultipart()
        msg['From'] = sender_address
        msg['To'] = receiver_address
        msg['Subject'] = subject
        msg.attach(MIMEText(mail_content, 'plain'))
        

        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender_address, password)
        
        smtp_server.send_message(msg)
        
        smtp_server.quit()
        
        with open("temp.txt", 'a') as f:
            f.write(f"Email sent to {recep_name}\n")
    else:
        with open("temp.txt", 'a') as f:
            f.write(f"No matching opportunities found for {Con_name['Name']}\n")
        