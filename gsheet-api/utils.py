#Needed packages for this project:
#pip install: google-api-python-client, google-auth-httplib2 google-auth-oauthlib
# gspread
# no need to install the second as it follows the first

import gspread
from google.oauth2.service_account import Credentials as SheetsCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64  #for gmail api
from email.mime.text import MIMEText
from email.utils import formataddr
import streamlit as st

import pandas
from dotenv import load_dotenv
import os
from openai import OpenAI


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def gmail_authenticate():
    secrets = st.secrets["gmail_token"]

    token_info = {
        "token": secrets["token"],
        "refresh_token": secrets["refresh_token"],
        "token_uri": secrets["token_uri"],
        "client_id": secrets["client_id"],
        "client_secret": secrets["client_secret"],
        "scopes": [secrets["scopes"]],
    }

    creds = Credentials.from_authorized_user_info(info=token_info)
    service = build("gmail", "v1", credentials=creds)
    return creds


#Google Sheets API Scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
#creds = SheetsCredentials.from_service_account_file("gsheet-credentials.json", scopes=scopes)
service_account_info = dict(st.secrets["gsheet_credentials"])
# Reconstruct proper private key formatting
service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")

    # Authorize credentials in-memory
creds = SheetsCredentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)
#client = gspread.authorize(creds)

sheet_id = "1ZRiIvGx3sFngZL5eCvdejh-xO-sMaMPD0hDvYS0gn-4"
spreadsheet = client.open_by_key(sheet_id)

worksheet = spreadsheet.get_worksheet(0)
sheet_records = worksheet.get_all_records()

#Convert the JSON records into a pandas DataFrame
records_df = pandas.DataFrame(sheet_records)




#Generate and send email via OpenAI
#Install and import openai
#load_dotenv()
#to check if dotenv works
#print("Email:", os.getenv("EMAIL"))

#api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def craft_email(name, role, pain_point):
    prompt = (
        f"Write a short, friendly cold email to {name}, a {role}, "
        f"about how my hypothetical company: 'NGX' can help them solve this pain point: “{pain_point}”."
        f"Don't mention or imply that the company is hypothetical. Just make up solutions tailored to the pain point."
        f"Use a warm tone."
        f"Start the email with: Subject: <your subject here>\n"
        f"Then write the email body\n"
        f"End the email with this signature:\n"
        f"Best regards, \n\nNneoma Uche\nAutomation Engineer at NGX"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    full_msg = response.choices[0].message.content.strip()

    #print(full_msg)
    if full_msg.lower().startswith("subject:"):
        lines = full_msg.split("\n", 1) #split into 2 parts: subject n body
        sub = lines[0].replace("Subject:", "").strip()
        msg_body = lines[1].strip()
    else:
        sub = "Quick idea for you"
        msg_body = full_msg.strip()

    return sub, msg_body


#loop through the DataFrame to get their name, email and painpoint:
#Pasting for loop below the craft email function and calling same after, allows to craft email for all


def send_mail(service, email, name, sub, msg_body):
    sender_name = "Nneoma Uche"
    sender_email = "oma.codespython@gmail.com"

    #Format the actual email to be sent
    message = MIMEText(msg_body)
    message['to'] = formataddr((name, email))  # e.g. James <james@example.com>
    message['from'] = formataddr((sender_name, sender_email))  # Nneoma Uche <...>
    message['subject'] = sub

    # Encode and send
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
    print(f"✅ Sent to {name} <{email}>")
   

#Call all functions, loop and send messages to all
if __name__ == "__main__":
    gmail_service = gmail_authenticate()
    for index, row in records_df.iterrows():
        #Skip if already sent to them
        if str(row.get("Sent", "")).strip().lower() == "true":
            continue


        name = row['Name']
        email = row['Email']
        role = row['Role']
        pain_point = row['Pain point']

        sub, msg_body = craft_email(name, role, pain_point)
        send_mail(gmail_service, email, name, sub, msg_body)
   
        headers = worksheet.row_values(1)  # Get header row
        sent_col = headers.index("Sent") + 1  # Sheet columns start at 1
        worksheet.update_cell(index + 2, sent_col, "TRUE")
    print("All emails processed!")

       





