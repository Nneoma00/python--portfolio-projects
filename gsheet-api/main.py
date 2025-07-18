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


import pandas
from dotenv import load_dotenv
import os
from openai import OpenAI


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None

    # Load token if it exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If not, do the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('gmail-credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the token for future runs
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service

#Google Sheets API Scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = SheetsCredentials.from_service_account_file("gsheet-credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1ZRiIvGx3sFngZL5eCvdejh-xO-sMaMPD0hDvYS0gn-4"
spreadsheet = client.open_by_key(sheet_id)

worksheet = spreadsheet.get_worksheet(0)
sheet_records = worksheet.get_all_records()

#Convert the JSON records into a pandas DataFrame
records_df = pandas.DataFrame.from_dict(sheet_records)




#Generate and send email via OpenAI
#Install and import openai
load_dotenv()
#to check if dotenv works
#print("Email:", os.getenv("EMAIL"))

#api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

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
    print("All emails processed!")


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
#Up to here, code takes 23 seconds to run

        # OR:::
        # send_mail(
        #     service = gmail_service,
        #     email = email,
        #     name = name,
        #     sub = sub,
        #     msg_body = msg_body
        # )

    #to test if code logic works
    #print(f"\nTo: {to_email}\nSubject: {sub}\n\n{msg_body}")







#print(records_df) #this works and prints out the entire sheet.
# now how to get their emails and pain points as variables






#To print/view all the worksheets :LIST THEIR TITLES IN TERMINAL in the doc/gspread
# sheets = map(lambda x: x.title, workbook.worksheets())
# print(list(sheets))

#To select a particular worksheet:
# sheet = workbook.worksheet("Sheet1")
#update the title
#sheet.update_title("Hello World")

#get the valuue of a specific cell


#To check if all we;ve done above is working
# values_list = sheet.sheet1.row_values(1)
# print(values_list)
#The above prints out the column titles in row1 e.g: ['Name', 'Email', 'Role',...]

