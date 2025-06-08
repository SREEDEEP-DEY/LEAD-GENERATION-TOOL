import streamlit as st
import pandas as pd
import requests

# Helper Functions
def fetch_domain(company_name):
    # Example using Clearbit API (replace `your_api_key`)
    api_key = "your_api_key"
    response = requests.get(
        f"https://company.clearbit.com/v1/domains/find?name={company_name}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    if response.status_code == 200:
        return response.json().get("domain", "Not Found")
    return "Not Found"

def validate_email(email):
    # Example using Hunter.io API (replace `your_api_key`)
    api_key = "your_api_key"
    response = requests.get(
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    )
    if response.status_code == 200:
        return response.json()["data"].get("status", "Invalid")
    return "Invalid"

def enrich_data(df):
    enriched_data = []
    for _, row in df.iterrows():
        company_name = row.get("Company", "")
        first_name = row.get("First Name", "")
        last_name = row.get("Last Name", "")

        domain = fetch_domain(company_name)
        email_guess = f"{first_name.lower()}.{last_name.lower()}@{domain}" if domain != "Not Found" else ""
        email_status = validate_email(email_guess) if email_guess else ""

        enriched_data.append({
            "Company": company_name,
            "Domain": domain,
            "Guessed Email": email_guess,
            "Validation Status": email_status
        })
    return pd.DataFrame(enriched_data)

# Streamlit App
st.title("CSV Enrichment + Export Tool")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview:")
    st.dataframe(df.head())

    # Enrichment
    if st.button("Enrich Data"):
        with st.spinner("Enriching data..."):
            enriched_df = enrich_data(df)
        st.success("Data enrichment complete!")
        st.write("### Enriched Data Preview:")
        st.dataframe(enriched_df.head())

        # Export
        csv = enriched_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Enriched CSV",
            data=csv,
            file_name="enriched_data.csv",
            mime="text/csv"
        )
