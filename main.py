import os
import csv
import webbrowser
from groq import Groq
from dotenv import load_dotenv
from scraper import scrape_books
from report import generate_html

load_dotenv() 

MAX_PAGES   = 5          
OUTPUT_CSV  = "books.csv"
OUTPUT_HTML = "report.html"
MODEL       = "llama-3.3-70b-versatile"   

def save_csv(books: list[dict], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "availability"])
        writer.writeheader()
        writer.writerows(books)
    print(f"💾 Saved {len(books)} books → {path}")

def groq_summary(books: list[dict]) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "⚠️ GROQ_API_KEY not set in .env"

    client = Groq(api_key=api_key)

    top_rated   = sorted(books, key=lambda b: b["rating"], reverse=True)[:5]
    cheapest    = sorted(books, key=lambda b: float(b["price"].replace("£","").replace("Â","").strip()))[:5]
    avg_rating  = sum(b["rating"] for b in books) / len(books)
    in_stock    = sum(1 for b in books if "In stock" in b["availability"])

    snapshot = (
        f"Total books: {len(books)}\n"
        f"Avg rating: {avg_rating:.1f}/5\n"
        f"In stock: {in_stock}/{len(books)}\n\n"
        f"Top-rated:\n" +
        "\n".join(f"  - {b['title']} ({b['rating']}★)" for b in top_rated)
    )

    print("🤖 Sending data to Groq...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Summarize this book data in 3 sentences. Be conversational."
            },
            {"role": "user", "content": f"Data:\n\n{snapshot}"}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def main():
    print("📚 Day 92 Scraper")

    books = scrape_books(max_pages=MAX_PAGES)
    save_csv(books, OUTPUT_CSV)
    
    summary = groq_summary(books)
    print(f"\n💬 AI Summary:\n{summary}\n")

    html = generate_html(books, summary)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    
    webbrowser.open(OUTPUT_HTML)
    print("✅ Done!")

if __name__ == "__main__":
    main()