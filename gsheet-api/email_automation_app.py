import streamlit as st
import gspread
from google.oauth2.service_account import Credentials as SheetsCredentials
from google.oauth2.credentials import Credentials as GmailCredentials
#from dotenv import load_dotenv
from openai import OpenAI
from utils import gmail_authenticate, send_mail, craft_email  # import from your existing file

# Load env variables (e.g., OpenAI key)
#load_dotenv()
#Use open ai key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Connect to Google Sheets
sheet_id = "1ZRiIvGx3sFngZL5eCvdejh-xO-sMaMPD0hDvYS0gn-4"
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = SheetsCredentials.from_service_account_info(st.secrets["gsheet_credentials"], scopes=scopes)
client_gs = gspread.authorize(creds)
sheet = client_gs.open_by_key(sheet_id).sheet1  # first worksheet

#Gmail setup
gmail_token = st.secrets["gmail_token"]
gmail_info = st.secrets["gmail_credentials"]

gmail_creds = GmailCredentials(
    token=gmail_token["token"],
    refresh_token=gmail_token["refresh_token"],
    token_uri=gmail_token["token_uri"],
    client_id=gmail_info["client_id"],
    client_secret=gmail_info["client_secret"],
    scopes=gmail_token["scopes"]
)

# Streamlit UI
st.title("📬 Try Your Personalized Email")

# Track usage attempts in this session
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if st.session_state.attempts >= 2:
    st.warning("⚠️ You've reached the maximum of 2 emails for this session.")
    st.stop()

with st.form("lead_form"):
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    role = st.text_input("Your role or title")
    company = st.text_input("Your company (or N/A if unemployed)")
    pain_point = st.text_area("What's your biggest pain point right now in your role?")

    submitted = st.form_submit_button("Generate & Send Email")

if submitted:
    if not all([name, email, role, company, pain_point]):
        st.error("Please fill in all the fields.")
    else:
        st.session_state.attempts += 1  # increment usage
        try:
            # 1. Append to Google Sheet
            #sheet.append_row([name, email, role, company, pain_point, "TRUE"])

            # 2. Generate and send the email
            subject, body = craft_email(name, role, pain_point)
            gmail_service = gmail_authenticate()
            send_mail(gmail_service, email, name, subject, body)

            # 3. Show preview
            st.success("✅ Email sent successfully!")
            st.subheader("📨 Email Preview")
            st.markdown(f"**Subject:** {subject}")
            st.text(body)

            # Show remaining attempts
            remaining = 2 - st.session_state.attempts
            st.info(f"You have {remaining} email generation attempt(s) left in this session.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
