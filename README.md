# 💬 Quotes App + Mood Chatbot

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![OpenAI](https://img.shields.io/badge/Azure-OpenAI-green.svg)

A **Streamlit web application** that combines:
- Quote discovery (API + database)
- Tag-based filtering system
- Data visualisation
- Web scraping validation
- AI-powered mood chatbot

---

## ✨ Features

### 🎲 Random Quote Generator
- Fetches quotes from an external API
- Allows users to refresh for new quotes
- Displays inspirational content dynamically

---

### 📊 Quote Explorer (Database Viewer)

Users can browse quotes in 3 modes:

- 🏷️ **Categorised Quotes**
  - Filter by tags (e.g. hope, life, courage)
- 📄 **Uncategorised Quotes**
  - View quotes without tags
- 🌐 **All Quotes**
  - Combined view of all sources

---

### 🏷️ Tag Management System
- Users can request new categories
- System validates tags using web scraping
- Prevents invalid or duplicate categories
- Automatically updates filtering options

---

### 📈 Tag Distribution Dashboard
- Interactive pie chart using Plotly
- Shows frequency of each tag
- Displays:
  - Most common tag
  - Count of top tag

---

### 🔎 Search by Author
- Search quotes by person’s name
- Works across both databases
- Clean tabular output

---

### 💬 Mood-Based Chatbot 🤖
- Detects user mood via keyword matching
- Selects relevant quotes:
  - 😔 Negative → hope quotes
  - 😊 Positive → happy quotes
  - ⚡ Default → inspirational quotes
- Uses Azure OpenAI to generate supportive responses
- Injects relevant quotes into AI response

---

## 🧠 System Architecture

```text
User Input
   ↓
Streamlit UI
   ↓
Mood Detection (keyword logic)
   ↓
Quote Database (SQLite)
   ↓
Fallback API (random quotes)
   ↓
Azure OpenAI (response generation)
   ↓
Final Chat Output
