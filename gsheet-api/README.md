

# Automated Lead Emailer

This Streamlit app automatically sends personalized emails to new leads using data from a Google Sheet. 
It integrates the **OpenAI API** for AI-generated content, **Gmail API** for sending emails, and **Google Sheets API** for tracking and updating lead statuses.

---

##  Features

* Pulls lead data (name, email, role, pain point) from a Google Sheet
* Uses OpenAI to generate personalized email content
* Sends emails automatically via Gmail API
* Marks each lead as "Sent" in the sheet to prevent duplicates
* Includes a Streamlit interface to test email generation manually

## Try it now:
[Try this tool on Streamlit](https://lead-email-automation.streamlit.app/)


## Tech Stack

* **Streamlit** – Web interface
* **OpenAI API** – For generating personalized email content
* **Gmail API** – To send emails from your Gmail account
* **Google Sheets API** – For reading/writing lead data
* **Python** – Core programming language


## How It Works

1. The app loads leads from your Google Sheet.
2. It checks if an email has already been sent (based on the `Sent` column).
3. For new leads:

   * Generates a personalized message using OpenAI.
   * Sends the email using Gmail API.
   * Marks the lead as `TRUE` in the "Sent" column.


## Use Cases

* Cold outreach automation
* SaaS product onboarding
* Newsletter personalization
* Lead nurturing

