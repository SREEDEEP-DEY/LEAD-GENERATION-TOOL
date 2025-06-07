import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define common email patterns
email_patterns = [
    "{firstname}@{domain}",
    "{lastname}@{domain}",
    "{firstname}.{lastname}@{domain}",
    "{firstname}{lastname}@{domain}",
    "{firstinitial}{lastname}@{domain}",
    "{lastname}{firstinitial}@{domain}"
]

def extract_name_from_linkedin(url):
    """Extract first and last name from LinkedIn profile URL."""
    try:
        parts = url.split("/")[-1].split("-")
        first_name = parts[0].capitalize()
        last_name = parts[1].capitalize() if len(parts) > 1 else ""
        return first_name, last_name
    except Exception:
        return "", ""

def scrape_company_from_linkedin(linkedin_url, headers):
    """Scrape current company name from LinkedIn profile page."""
    try:
        response = requests.get(linkedin_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        company_tag = soup.find("span", class_="text-body-medium")
        if company_tag:
            return company_tag.text.strip()
        return ""
    except Exception as e:
        return ""

def fetch_company_domain(company_name, api_key):
    """Fetch company domain using Clearbit API."""
    try:
        response = requests.get(
            f"https://company.clearbit.com/v2/companies/find?name={company_name}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 200:
            return response.json().get("domain", "")
        return ""
    except Exception:
        return ""

def generate_email_guesses(domain, first_name, last_name):
    """Generate email guesses based on patterns."""
    guesses = []
    for pattern in email_patterns:
        email = pattern.format(
            firstname=first_name.lower(),
            lastname=last_name.lower(),
            firstinitial=first_name[0].lower(),
            domain=domain
        )
        guesses.append(email)
    return guesses

def validate_email(email, api_key):
    """Validate email using Hunter.io API."""
    try:
        response = requests.get(
            f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("status", "invalid")
        return "invalid"
    except Exception:
        return "invalid"

# Streamlit UI
st.title("LinkedIn Profile → Email Guesser")

# LinkedIn Scraping Settings
st.sidebar.header("Scraping Settings")
headers = {
    "User-Agent": st.sidebar.text_input(
        "User-Agent Header", placeholder="Enter your browser's User-Agent"
    ),
    "Cookie": st.sidebar.text_area(
        "LinkedIn Cookies", placeholder="Paste your LinkedIn cookies here"
    )
}

hunter_api_key = st.sidebar.text_input("Hunter.io API Key", type="password")
clearbit_api_key = st.sidebar.text_input("Clearbit API Key", type="password")

# Single Input Mode
st.header("Single Email Guessing")
linkedin_url = st.text_input("LinkedIn Profile URL", placeholder="e.g., https://www.linkedin.com/in/john-doe/")
if st.button("Generate Emails"):
    first_name, last_name = extract_name_from_linkedin(linkedin_url)
    company_name = scrape_company_from_linkedin(linkedin_url, headers)
    domain = fetch_company_domain(company_name, clearbit_api_key)

    if first_name and last_name and domain:
        emails = generate_email_guesses(domain, first_name, last_name)
        results = []
        for email in emails:
            validation_status = validate_email(email, hunter_api_key)
            results.append({"Email": email, "Validation": validation_status})
        result_df = pd.DataFrame(results)
        st.write(result_df)
    else:
        st.error("Failed to scrape LinkedIn or fetch domain. Check your inputs or API keys.")

# Bulk Processing
st.header("Bulk Email Guessing")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file and st.button("Process Bulk Data"):
    input_data = pd.read_csv(uploaded_file)
    results = []

    for _, row in input_data.iterrows():
        linkedin_url = row.get("LinkedIn URL", "")
        first_name, last_name = extract_name_from_linkedin(linkedin_url)
        company_name = scrape_company_from_linkedin(linkedin_url, headers)
        domain = fetch_company_domain(company_name, clearbit_api_key)

        if first_name and last_name and domain:
            emails = generate_email_guesses(domain, first_name, last_name)
            for email in emails:
                validation_status = validate_email(email, hunter_api_key)
                results.append({
                    "LinkedIn URL": linkedin_url,
                    "Email": email,
                    "Validation": validation_status
                })

    result_df = pd.DataFrame(results)
    st.write(result_df)

    # Download Results
    csv = result_df.to_csv(index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="email_guesses.csv",
        mime="text/csv"
    )
