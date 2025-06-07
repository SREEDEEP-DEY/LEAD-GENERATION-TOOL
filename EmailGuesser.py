import streamlit as st
import pandas as pd

# Define common email patterns
email_patterns = [
    "{firstname}@{domain}",
    "{lastname}@{domain}",
    "{firstname}.{lastname}@{domain}",
    "{firstname}{lastname}@{domain}",
    "{firstinitial}{lastname}@{domain}",
    "{lastname}{firstinitial}@{domain}"
]

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

def process_bulk_data(uploaded_file):
    """Process uploaded CSV file for bulk email guesses."""
    df = pd.read_csv(uploaded_file)
    results = []

    for _, row in df.iterrows():
        domain = row.get('Domain', '')
        first_name = row.get('First Name', '')
        last_name = row.get('Last Name', '')
        
        if domain and first_name and last_name:
            guesses = generate_email_guesses(domain, first_name, last_name)
            for guess in guesses:
                results.append({
                    'Domain': domain,
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Guessed Email': guess
                })

    return pd.DataFrame(results)

# Streamlit UI
st.title("Domain → Email Pattern Guesser")

# Single input mode
st.header("Single Email Prediction")
domain = st.text_input("Domain", placeholder="e.g., google.com")
first_name = st.text_input("First Name", placeholder="e.g., John")
last_name = st.text_input("Last Name", placeholder="e.g., Doe")

if st.button("Generate Email Guesses"):
    if domain and first_name and last_name:
        guesses = generate_email_guesses(domain, first_name, last_name)
        st.write("### Predicted Emails:")
        st.write(guesses)
    else:
        st.error("Please fill in all fields (Domain, First Name, Last Name).")

# Bulk upload mode
st.header("Bulk Email Prediction")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    st.write("### Uploaded Data Preview:")
    input_data = pd.read_csv(uploaded_file)
    st.write(input_data.head())

    if st.button("Process Bulk Data"):
        result_df = process_bulk_data(uploaded_file)
        st.write("### Results:")
        st.write(result_df)

        # Download link
        csv = result_df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="email_guesses.csv",
            mime="text/csv"
        )