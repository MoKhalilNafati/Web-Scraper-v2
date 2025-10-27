# DAAD Program Scraper
This project is an asynchronous web scraper built with Python to gather information about university degree programs from the DAAD (German Academic Exchange Service) website.

The script starts from a pre-filtered DAAD search results page, extracts the list of all programs, and then concurrently fetches and parses the detail page for each program. All collected data is then saved into a single CSV file.

## 🚀 Features
Asynchronous: Uses asyncio and aiohttp to fetch program detail pages in parallel, making it much faster than a traditional synchronous scraper.

Detailed Parsing: Uses BeautifulSoup (with lxml) to parse and extract specific, valuable information from each program page.

Structured Output: Saves all data into a clean, well-structured programs.csv file for easy analysis in Excel, Google Sheets, or with other scripts.

## ⚙️ Installation
Clone or download this project's script.

Install the required Python libraries. This script relies on a few external packages.

Bash

pip install beautifulsoup4 aiohttp lxml
(Note: asyncio and csv are part of the standard Python library.)

## ▶️ How to Use
(Optional) Customize the Search URL Inside the script, you can change the BASE_URL variable to match your own DAAD search filters (e.g., different subjects, language, deadlines, etc.).

Python

BASE_URL = "https://www.daad.de/en/studying-in-germany/universities/all-degree-programmes/?hec-degreeProgrammeType=w&hec-teachingLanguage=2&..."
(Recommended) Update the Output Path The script currently saves the CSV file to a hardcoded path. It's better to save it in the same directory as the script.

Find this line in the main() function:

Python

## Original line:
with open("C:/Users/Khalil/Documents/VS/Web Scraping v2/programs.csv", "w", newline="") as f:
And change it to this (adding encoding="utf-8" is also good practice to handle special characters):

Python

## Recommended change:
with open("programs.csv", "w", newline="", encoding="utf-8") as f:
Run the script From your terminal, simply execute the Python file.

Bash

python your_script_name.py
Get Your Data The script will run for a moment (fetching all pages) and then create a programs.csv file in the location you specified.

📊 Output
The script generates a programs.csv file with the following columns:

Program

University/Hochschule

Location

Period Of Study

Area Of Study

Focus

Deadlines

Admission Semester

Annotation

Admission Modus

Admission requirements

Lecture period

Find Student advisory service (Email | Web)

Links (A direct link to the program's detail page)
