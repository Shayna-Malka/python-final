# 💬 Quotes App + Mood Chatbot

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![Azure OpenAI](https://img.shields.io/badge/OpenAI-Azure-green.svg)
![Status](https://img.shields.io/badge/Project-Active-brightgreen.svg)

---

## 📌 Overview

The Quotes App + Mood Chatbot is a Streamlit-based web application that integrates multiple data sources and AI capabilities to provide an interactive quote discovery and emotional support system.

It combines:
- SQLite databases (tagged + untagged quotes)
- External API (random quotes)
- Web scraping (tag validation)
- Data visualisation (Plotly)
- Azure OpenAI chatbot integration

---

## 🎯 Objectives

- Build an interactive data-driven web application
- Combine API, database, and scraping workflows
- Implement dynamic filtering and search
- Visualise quote tag distributions
- Create a mood-aware chatbot using AI

---

## 🧠 System Architecture

User Input (Streamlit UI)
        ↓
Mood Detection (Rule-based)
        ↓
Database Query (SQLite)
        ↓
Optional API / Scraping Layer
        ↓
Data Processing (Pandas)
        ↓
Azure OpenAI (Response Generation)
        ↓
Streamlit UI Output

---

## 📊 Features

---

### 🎲 Random Quote Generator
- Fetches quotes from external API
- Stored in session_state for performance
- Allows users to refresh for new quotes

---

### 📚 Quote Explorer

Three viewing modes:

**1. Categorised Quotes**
- Filter by tags
- Uses multi-select UI
- Queries tagged database

**2. Uncategorised Quotes**
- Displays quotes without tags
- User selects number of quotes

**3. All Quotes**
- Combines both datasets
- Provides full dataset view

---

### 🏷️ Tag Management System

Workflow:
- User submits new category
- System scrapes external source
- If valid:
  - category is added
  - database updated
  - UI refresh triggered
- If invalid:
  - error message shown

---

### 📈 Tag Distribution

- Plotly pie chart visualisation
- Shows frequency of tags
- Displays:
  - most common tag
  - count of most frequent tag

---

### 🔎 Author Search

- Search quotes by author name
- Queries both databases
- Displays results in table format

---

### 💬 Mood Chatbot 🤖

**Workflow:**

1. User enters mood
2. Keyword-based detection:
   - negative → hope quotes
   - positive → happy quotes
   - default → inspirational quotes
3. Quote is retrieved from database
4. Azure OpenAI generates response
5. Chat output displayed in Streamlit

---

## ⚙️ Design Decisions

### 📊 Limited Table Display
- Improves performance
- Avoids UI clutter
- Streamlit reruns make large datasets inefficient
- Encourages filtering instead of full dumps

---

### 🏷️ Tag Validation via Scraping
- Ensures category exists externally
- Prevents invalid tags
- Maintains dataset consistency

---

### 💬 Hybrid Chatbot Design
- Rules: fast mood detection
- Database: structured quote source
- AI: natural conversational response

---


## 🗄️ Database Schema

Tagged Quotes:
- quote (TEXT)
- author (TEXT)
- tags (TEXT)

Untagged Quotes:
- quote (TEXT)
- author (TEXT)

---

## 🔐 Environment Variables (Streamlit Secrets)

This project uses Streamlit Secrets to store API keys securely.

---

### 📁 1. Create folder structure

Create a folder named **`.streamlit`** in your project root:

---

### 🧾 2. Create `secrets.toml`

Inside `.streamlit/`, create a file called:

---


### 🔑 3. Add your keys

Paste this into `secrets.toml`:

```toml
AZURE_OPENAI_API_KEY = "your_key"
AZURE_OPENAI_ENDPOINT = "your_endpoint"

