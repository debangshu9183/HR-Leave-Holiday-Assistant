# 🤖 HR AI Assistant — Hybrid RAG + Text-to-SQL

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama--3-F55036?style=for-the-badge&logo=meta&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Text--to--SQL-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

**An intelligent HR assistant that answers employee questions by combining document understanding with live SQL data analysis — no hallucinations, no guesswork.**

</div>

---

## ✨ Overview

HR AI Assistant is a terminal-based chatbot that answers HR-related queries using two real data sources:

- 📄 **Leave Policy PDF** — parsed and injected into the LLM's context
- 📊 **Holiday Calendar CSV** — converted to a SQLite database and queried via generated SQL

Instead of letting the model guess, every factual answer is grounded in actual data retrieved through structured SQL queries — making this a **reliable, hallucination-resistant assistant**.

---

## 🏗️ Architecture

```
User Question
      ↓
LLM generates SQL query (Text-to-SQL)
      ↓
SQL executed on SQLite database
      ↓
Results converted to Pandas DataFrame
      ↓
Structured summary prompt built
      ↓
LLM explains results using real data
```

> This design ensures the model **analyzes actual data** rather than relying on memorized patterns or making things up.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📄 PDF Understanding | Reads HR Leave Policy and injects it as context |
| 📊 CSV → SQL Pipeline | Converts Holiday Calendar to queryable SQLite DB |
| 🧠 Text-to-SQL Reasoning | LLM writes SQL; SQL fetches facts; LLM explains |
| 🔎 Hallucination Prevention | Answers are always grounded in SQL query results |
| 💬 Interactive Chat | Terminal-based conversational interface |
| ⚡ Groq LLM | Powered by Llama-3 via Groq for fast inference |

---

## 🧠 Data Sources

### 1️⃣ Leave Policy — `Leave_Details.pdf`

Contains official HR rules including:
- Leave entitlements during probation
- Quarterly leave credit schedule
- Leave usage and carry-forward policies

This text is extracted using **PDFPlumber** and injected directly into the system prompt.

### 2️⃣ Holiday Calendar — `Holiday_List_2026.csv`

| Column | Description |
|---|---|
| `Name` | Festival / holiday name |
| `start_date` | Holiday start date |
| `end_date` | Holiday end date |
| `Locations` | Applicable office locations |
| `Shifts` | Applicable work shifts |
| `Holiday_Classification` | `Holiday` or `Restricted Holiday` |

This CSV is loaded into a **SQLite database** at runtime and queried dynamically via LLM-generated SQL.

---

## 📁 Project Structure

```
HR_chatbot/
│
├── data/
│   ├── Leave_Details.pdf          # HR leave policy document
│   └── Holiday_List_2026.csv      # Company holiday calendar
│
├── src/
│   ├── chatbot.py                 # Main chat loop and orchestration
│   ├── csv_database.py            # CSV → SQLite loader
│   ├── groq_client.py             # Groq LLM API wrapper
│   ├── pdf_loader.py              # PDF text extraction
│   ├── prompt.py                  # Prompt templates
│   └── sql_helper.py              # SQL generation & execution helpers
│
├── main.py                        # Entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/hr-ai-assistant.git
cd hr-ai-assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv hr_bot

# Windows
hr_bot\Scripts\activate

# Mac / Linux
source hr_bot/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

> Get your free API key at [console.groq.com](https://console.groq.com)

---

## ▶️ Running the Chatbot

```bash
python main.py
```

```
🤖 HR Assistant ready! Ask me anything about leaves or holidays.

You: List all holidays in October 2026
Assistant: There are 2 holidays in October 2026...

You: How many restricted holidays are there in total?
Assistant: Based on the holiday calendar, there are 14 restricted holidays...
```

---

## 💬 Example Questions

**Holiday Queries (Text-to-SQL)**
- *How many restricted holidays are there?*
- *Which month has the most holidays?*
- *Are there any consecutive holidays in the calendar?*
- *Which festivals are classified as restricted holidays?*

**Leave Policy Queries (RAG)**
- *How many earned leaves are credited during probation?*
- *Can I carry forward unused leaves to the next quarter?*
- *What is the leave policy for new joiners?*

---

## 🧩 Tech Stack

- **Python 3.10+** — core language
- **Groq API (Llama-3)** — LLM inference
- **PDFPlumber** — PDF text extraction
- **Pandas** — CSV processing and data handling
- **SQLite** — in-memory relational database for SQL queries
- **python-dotenv** — environment variable management

---

## 📈 Roadmap

- [ ] 🔎 Vector database integration for semantic PDF search (true RAG)
- [ ] 🧠 Automatic query routing (PDF vs SQL vs hybrid)
- [ ] 🌐 Web interface with Streamlit or FastAPI
- [ ] 📊 Chart generation from SQL results
- [ ] 🧾 Source citation in responses
- [ ] 🗂️ Multi-document support

---

## 📚 What This Project Demonstrates

This project is a practical implementation of:

- **Text-to-SQL** — letting an LLM translate natural language into executable SQL
- **Hybrid RAG** — combining document retrieval (PDF) with structured data retrieval (SQL)
- **Grounded LLM reasoning** — using retrieved evidence to generate accurate, trustworthy answers
- **Reliable AI assistant design** — preventing hallucinations through structured pipelines

---

## 👨‍💻 Author

**Debangshu Sadhukhan**  
MSc Data Science Student

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/yourusername)

---

## ⭐ Support

If you found this project useful or learned something from it, consider giving it a **star** — it helps others discover it too!

---

<div align="center">
  <sub>Built with curiosity and structured reasoning 🧠</sub>
</div>
