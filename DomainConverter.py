# Company Name to Domain Converter (Streamlit + Clearbit + LinkedIn + Confidence)

import streamlit as st
import requests
import pandas as pd
import time
from rapidfuzz import fuzz

# --- Helper Function: Clean company name ---
def clean_name(name):
    name = name.lower()
    remove_words = ["inc", "ltd", "llc", "corp", "co", "pvt", "gmbh", "sas"]
    for word in remove_words:
        name = name.replace(word, "")
    return name.strip()

# --- Helper Function: Call Clearbit API ---
def fetch_company_data(company_name):
    url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={company_name}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            if results:
                match = results[0]
                confidence = fuzz.ratio(company_name.lower(), match['name'].lower())
                domain = match.get('domain')
                name = match.get('name')
                logo = match.get('logo')
                linkedin = match.get('linkedin') if 'linkedin' in match else f"https://www.linkedin.com/search/results/all/?keywords={name}"
                twitter = match.get('twitter') if 'twitter' in match else ""
                facebook = match.get('facebook') if 'facebook' in match else ""
                return domain, name, logo, confidence, linkedin, twitter, facebook
        return None, None, None, 0, None, None, None
    except Exception as e:
        return None, None, None, 0, None, None, None

# --- Streamlit UI ---
st.set_page_config(page_title="Company → Domain Converter", layout="centered")
st.title("🏢 Company Name → 🌐 Domain Converter")
st.write("Convert company names into official domains using Clearbit, with confidence scoring, logo preview, and social links.")

# --- Input Section ---
option = st.radio("Choose input method:", ("Single Company", "Upload CSV"))

results = []

if option == "Single Company":
    company = st.text_input("Enter Company Name:")
    if st.button("Convert") and company:
        with st.spinner("Fetching domain..."):
            clean_company = clean_name(company)
            domain, name, logo, score, linkedin, twitter, facebook = fetch_company_data(clean_company)
            if domain:
                st.success(f"Domain for '{name}': {domain} (Confidence: {score}%)")
                st.image(logo, width=50)
                st.markdown(f"🔗 [LinkedIn]({linkedin})")
                if twitter:
                    st.markdown(f"🐦 [Twitter]({twitter})")
                if facebook:
                    st.markdown(f"📘 [Facebook]({facebook})")
                results.append({
                    "Company": name,
                    "Domain": domain,
                    "Confidence %": score,
                    "LinkedIn": linkedin,
                    "Twitter": twitter,
                    "Facebook": facebook
                })
            else:
                st.error("Domain not found.")

elif option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV file with 'Company' column:", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "Company" not in df.columns:
            st.error("CSV must contain a 'Company' column.")
        else:
            if st.button("Convert All"):
                with st.spinner("Processing..."):
                    for idx, row in df.iterrows():
                        raw_company = str(row['Company'])
                        clean_company = clean_name(raw_company)
                        domain, name, _, score, linkedin, twitter, facebook = fetch_company_data(clean_company)
                        results.append({
                            "Company": name or raw_company,
                            "Domain": domain or "Not Found",
                            "Confidence %": score,
                            "LinkedIn": linkedin or "",
                            "Twitter": twitter or "",
                            "Facebook": facebook or ""
                        })
                        time.sleep(0.3)  # Rate limit
                st.success("Done!")
                result_df = pd.DataFrame(results)
                st.dataframe(result_df)

                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", data=csv, file_name="company_domains_enriched.csv", mime='text/csv')
