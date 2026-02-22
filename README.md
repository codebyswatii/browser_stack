# BrowserStack Parallel Automation Scraper 🚀

## 📌 Project Overview

This project demonstrates **parallel cross-browser testing using BrowserStack** combined with **Selenium automation** to scrape articles from the EL PAÍS opinion section.

The script:

- Runs tests in 5 parallel threads
- Executes across:
  - Windows (Chrome, Firefox)
  - macOS (Safari)
  - iOS
  - Android
- Extracts:
  - Article Titles
  - Article Content
  - Translated Titles (Spanish → English)
  - High-resolution Cover Images
- Uploads execution to BrowserStack for live monitoring

## 🔐 Environment Setup

Create a `.env` file:
- BROWSERSTACK_USERNAME=your_username
- BROWSERSTACK_ACCESS_KEY=your_access_key

---

## 🚀 Installation & Run

### 1. Create Virtual Environment

- python -m venv venv
- venv\Scripts\activate

### 2. Install Dependencies
- pip install -r requirements.txt

### 3. Run Parallel BrowserStack Tests
- python browser_stack.py

## 🌟 Features

- ✅ Parallel Cross-Browser Execution
- ✅ Automatic Cookie Handling
- ✅ Article Title Extraction
- ✅ Content Scraping with Fallbacks
- ✅ Automatic Translation via API
- ✅ High-Resolution Image Download
- ✅ Structured File Naming
- ✅ BrowserStack Cloud Execution