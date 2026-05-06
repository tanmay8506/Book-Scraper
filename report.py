def generate_html(books, ai_summary):
    rows = ""
    for b in books:
        stars = "★" * b["rating"] + "☆" * (5 - b["rating"])
        avail_class = "avail-yes" if "In stock" in b["availability"] else "avail-no"
        rows += f"""
        <tr>
            <td class="book-title">{b['title']}</td>
            <td class="price">{b['price']}</td>
            <td class="stars" title="{b['rating']}/5">{stars}</td>
            <td class="{avail_class}">{b['availability']}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Book Scraper</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Code+Pro:wght@400;600&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink:     #1a1208;
    --parchment: #f5efe0;
    --cream:   #fffdf7;
    --gold:    #c8922a;
    --rust:    #a63d2f;
    --sage:    #4a7c59;
    --border:  #d4c5a0;
    --shadow:  rgba(26,18,8,0.12);
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: var(--parchment);
    color: var(--ink);
    font-family: 'Lato', sans-serif;
    min-height: 100vh;
  }}

  header {{
    background: var(--ink);
    color: var(--cream);
    padding: 3rem 2rem 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }}
  header::before {{
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(
      45deg,
      transparent, transparent 40px,
      rgba(200,146,42,.04) 40px, rgba(200,146,42,.04) 80px
    );
  }}
  .badge {{
    display: inline-block;
    background: var(--gold);
    color: var(--ink);
    font-family: 'Source Code Pro', monospace;
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .15em;
    text-transform: uppercase;
    padding: .3rem .8rem;
    border-radius: 2px;
    margin-bottom: 1rem;
  }}
  h1 {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -.01em;
  }}
  h1 span {{ color: var(--gold); }}
  .subtitle {{
    margin-top: .6rem;
    font-size: .95rem;
    font-weight: 300;
    opacity: .65;
    letter-spacing: .05em;
  }}

  .stats-bar {{
    display: flex;
    justify-content: center;
    gap: 0;
    border-top: 1px solid rgba(255,255,255,.1);
    margin-top: 2rem;
  }}
  .stat {{
    flex: 1; max-width: 160px;
    padding: 1rem .5rem;
    border-right: 1px solid rgba(255,255,255,.08);
  }}
  .stat:last-child {{ border-right: none; }}
  .stat-val {{
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: var(--gold);
    display: block;
  }}
  .stat-lbl {{
    font-size: .7rem;
    font-weight: 300;
    letter-spacing: .12em;
    text-transform: uppercase;
    opacity: .55;
  }}

  .ai-section {{
    max-width: 860px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
  }}
  .ai-card {{
    background: var(--cream);
    border: 1px solid var(--border);
    border-left: 4px solid var(--gold);
    border-radius: 6px;
    padding: 1.8rem 2rem;
    box-shadow: 0 2px 20px var(--shadow);
  }}
  .ai-label {{
    display: flex;
    align-items: center;
    gap: .5rem;
    font-family: 'Source Code Pro', monospace;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: .9rem;
  }}
  .ai-label::before {{
    content: '';
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--sage);
    box-shadow: 0 0 6px var(--sage);
  }}
  .ai-card p {{
    line-height: 1.75;
    font-size: .97rem;
    color: #3a2e1a;
    white-space: pre-wrap;
  }}

  .table-section {{
    max-width: 1100px;
    margin: 0 auto 3rem;
    padding: 0 1.5rem;
  }}
  .section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 1rem;
    padding-bottom: .5rem;
    border-bottom: 2px solid var(--border);
    display: flex;
    align-items: baseline;
    gap: .8rem;
  }}
  .section-title small {{
    font-family: 'Source Code Pro', monospace;
    font-size: .7rem;
    font-weight: 400;
    color: #8a7a5a;
    letter-spacing: .1em;
  }}

  .search-bar {{
    width: 100%;
    padding: .6rem 1rem;
    margin-bottom: 1rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--cream);
    font-family: 'Source Code Pro', monospace;
    font-size: .85rem;
    color: var(--ink);
    outline: none;
    transition: border-color .2s;
  }}
  .search-bar:focus {{ border-color: var(--gold); }}

  .table-wrap {{
    overflow-x: auto;
    border-radius: 6px;
    box-shadow: 0 2px 20px var(--shadow);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--cream);
    font-size: .9rem;
  }}
  thead tr {{
    background: var(--ink);
    color: var(--cream);
  }}
  thead th {{
    padding: .85rem 1rem;
    text-align: left;
    font-family: 'Source Code Pro', monospace;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
  }}
  thead th:hover {{ color: var(--gold); }}
  tbody tr {{ border-bottom: 1px solid var(--border); transition: background .15s; }}
  tbody tr:hover {{ background: #f0e8d0; }}
  tbody td {{ padding: .75rem 1rem; vertical-align: middle; }}

  .book-title {{ font-weight: 700; max-width: 380px; }}
  .price {{
    font-family: 'Source Code Pro', monospace;
    font-weight: 600;
    color: var(--rust);
    white-space: nowrap;
  }}
  .stars {{ color: var(--gold); letter-spacing: .05em; white-space: nowrap; }}
  .avail-yes {{ color: var(--sage); font-size: .82rem; font-weight: 700; }}
  .avail-no  {{ color: var(--rust); font-size: .82rem; font-weight: 700; }}

  footer {{
    text-align: center;
    padding: 2rem;
    font-family: 'Source Code Pro', monospace;
    font-size: .72rem;
    letter-spacing: .1em;
    color: #9a8a6a;
    border-top: 1px solid var(--border);
  }}
</style>
</head>
<body>

<header>
  <div class="badge">Portfolio Project</div>
  <h1>The <span>Book</span> Scraper</h1>
  <p class="subtitle">100 Days of Code  ·  Angela Yu  ·  Powered by Groq AI</p>

  <div class="stats-bar"> 
    <div class="stat">
      <span class="stat-val">{len(books)}</span>
      <span class="stat-lbl">Books</span>
    </div>
    <div class="stat">
      <span class="stat-val">{len(set(b['price'] for b in books))}</span>
      <span class="stat-lbl">Price Points</span>
    </div>
    <div class="stat">
      <span class="stat-val">{sum(1 for b in books if b['rating'] >= 4)}</span>
      <span class="stat-lbl">Rated 4★+</span>
    </div>
    <div class="stat">
      <span class="stat-val">{sum(1 for b in books if 'In stock' in b['availability'])}</span>
      <span class="stat-lbl">In Stock</span>
    </div>
  </div>
</header>

<section class="ai-section">
  <div class="ai-card">
    <div class="ai-label">AI Summary</div>
    <p>{ai_summary}</p>
  </div>
</section>

<section class="table-section">
  <div class="section-title">
    All Books <small>CLICK HEADERS TO SORT</small>
  </div>
  <input class="search-bar" type="text" id="searchInput" placeholder="🔍  Filter by title..." oninput="filterTable()">
  <div class="table-wrap">
    <table id="bookTable">
      <thead>
        <tr>
          <th onclick="sortTable(0)">Title ↕</th>
          <th onclick="sortTable(1)">Price ↕</th>
          <th onclick="sortTable(2)">Rating ↕</th>
          <th onclick="sortTable(3)">Availability ↕</th>
        </tr>
      </thead>
      <tbody id="tableBody">
        {rows}
      </tbody>
    </table>
  </div>
</section>

<footer>books.toscrape.com &nbsp;·&nbsp; scraped with BeautifulSoup4</footer>

<script>
function filterTable() {{
  const q = document.getElementById('searchInput').value.toLowerCase();
  document.querySelectorAll('#tableBody tr').forEach(row => {{
    const title = row.cells[0].textContent.toLowerCase();
    row.style.display = title.includes(q) ? '' : 'none';
  }});
}}

let sortDir = {{}};
function sortTable(col) {{
  const tbody = document.getElementById('tableBody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  const dir = (sortDir[col] = !(sortDir[col] || false));
  rows.sort((a, b) => {{
    let av = a.cells[col].textContent.trim();
    let bv = b.cells[col].textContent.trim();
    const an = parseFloat(av.replace(/[^0-9.]/g, ''));
    const bn = parseFloat(bv.replace(/[^0-9.]/g, ''));
    if (!isNaN(an) && !isNaN(bn)) return dir ? an - bn : bn - an;
    return dir ? av.localeCompare(bv) : bv.localeCompare(av);
  }});
  rows.forEach(r => tbody.appendChild(r));
}}
</script>
</body>
</html>"""