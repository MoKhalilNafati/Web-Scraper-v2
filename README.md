# 🎓 DAAD Programs Scraper (Async Version)

This project is an **asynchronous Python web scraper** that extracts detailed information about degree programs listed on the [DAAD website](https://www.daad.de/en/studying-in-germany/universities/all-degree-programmes/).

It uses `asyncio` and `aiohttp` to **concurrently fetch** all program detail pages for high speed, then parses the data and saves the results into a structured CSV file.

---

## 🚀 Features

The scraper extracts the following fields:

- **Program**
- **University / Hochschule**
- **Location**
- **Period of Study**
- **Area of Study**
- **Focus**
- **Deadlines** (for international students from non-EU countries)
- **Admission Semester**
- **Annotation**
- **Admission Modus**
- **Admission Requirements**
- **Lecture Period**
- **Student Advisory Service** (E-Mail | Website)
- **Detail Page Link**

---

## 📦 Requirements

Make sure you have Python 3.8+ installed and install the dependencies. (Note: `asyncio` and `csv` are part of the standard Python library).

```bash
pip install aiohttp
pip install beautifulsoup4
pip install lxml
```
## 📝 Usage

1. Open the script in your editor and adjust the ##BASE_URL## for your preferred programs filter.
2. Replace your with open(...) line: Find this line in your main function
```
with open("C:/Users/Khalil/Documents/VS/Web Scraping v2/programs.csv", "w", newline="") as f:
```
The results will be saved in programs.csv file.
