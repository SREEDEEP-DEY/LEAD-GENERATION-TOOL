# 🔗 AI Lead Generation Toolkit  
*A submission for Caprae Capital's AI Internship Challenge*

---

## 🚀 Overview

This project is a **lightweight, modular tool suite** built in under 5 hours to support AI-enhanced **lead generation** and **email enrichment** workflows. The tools are designed for speed, business impact, and scalability. 👨‍💻📈

---

## 🧰 Features Breakdown

---
### 1️⃣ **Company → Domain Converter**
🔍 Converts company names into official domains using Clearbit  
✨ Adds logo, LinkedIn, Twitter, and Facebook links  
📊 Includes confidence scoring via `rapidfuzz`

📄 **File**: `DomainConverter.py`

---

### 2️⃣ **Domain → Email Pattern Guesser**
📬 Predicts professional email addresses using `First Name + Last Name + Domain`  
🔄 Supports **bulk CSV input**  
📁 Outputs a downloadable CSV of email guesses  

📄 **File**: `EmailGuesser.py`

---

### 3️⃣ **LinkedIn → Email Guesser**
🕵️ Extracts **names and company** from a LinkedIn URL  
📡 Uses **Clearbit** to find domains  
✅ Validates each guessed email using **Hunter.io**  
💾 Works with **single URLs** and **bulk CSV uploads**

📄 **File**: `LinkedinEmailGuesser.py`

---

### 4️⃣ **CSV Enrichment & Export**
📁 Uploads a raw CSV with basic lead info  
⚙️ Enriches data with **company domain** and **guessed emails**  
📮 Validates email guesses using Hunter API  
📥 Download enriched & validated dataset as a CSV

📄 **File**: `CSVEnrichment.py`

---

## 🛠️ Technologies Used

- **Language**: Python 🐍  
- **Framework**: Streamlit for rapid UI development  
- **APIs**:
  - 🔍 Clearbit — domain + company enrichment
  - 📬 Hunter.io — email validation  
- **Libraries**:
  - `requests` for API calls  
  - `pandas` for data processing  
  - `beautifulsoup4` for scraping LinkedIn  
  - `rapidfuzz` for fuzzy matching company names  

---

## 🚀 How to Run Locally

### 📦 Install Dependencies:
```bash
pip install streamlit pandas requests beautifulsoup4 rapidfuzz
