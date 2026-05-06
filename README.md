Book Scraper + Groq AI Summary
A Python-based web scraper that extracts data from a book retail site and uses Groq's LLM to generate a conversational summary of the findings. The project concludes by generating a sortable HTML report with a custom UI.

Features
Automated Scraping: Extracts book titles, prices, star ratings, and stock status across multiple pages using BeautifulSoup.  

Data Export: Saves all scraped data into a structured books.csv file.  

AI Analysis: Sends a data snapshot to Groq (Llama 3.3) to generate a witty, human-like summary of the collection.  

Dynamic Report: Generates a polished HTML dashboard featuring CSS variables for styling and vanilla JavaScript for real-time table sorting.  

Project Structure
main.py: The entry point that orchestrates the scraping, saving, and AI summary process.  

scraper.py: Contains the logic for HTTP requests and HTML parsing.  

report.py: Holds the HTML template and CSS used to build the final report.  

.env: Stores your Groq API key securely.  

Setup
Install Dependencies:

Bash
pip install -r requirements.txt

Configure API Key:
Create a .env file in the root directory and add your key:
GROQ_API_KEY=your_api_key_here
Run the Program:

Bash
python main.py
Technical Details
Target Site: books.toscrape.com (a legal practice site).  

Tech Stack: Python, Requests, BeautifulSoup4, Groq SDK, and Dotenv.
