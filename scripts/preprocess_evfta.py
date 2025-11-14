import json
import re
from pdf2image import convert_from_path
import pytesseract

# Force Tesseract path on Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Tesseract config (more stable lines; keeps spaces; good for tables)
TESS_CFG = r"--psm 6 -c preserve_interword_spaces=1"

def clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# ---------------------------
# ARTICLES (pages before PSR)
# ---------------------------
def extract_articles_from_text(full_text: str):
    # Capture: "Article <num>\n<title>\n<body...> until next Article or the PSR list"
    pattern = r"(Article\s+\d+)\s*\n([^\n]+)\n(.*?)(?=\nArticle\s+\d+\s*\n|LIST OF REQUIRED WORKING|ANNEX|$)"
    matches = re.findall(pattern, full_text, flags=re.IGNORECASE | re.DOTALL)

    articles = []
    for art, title, body in matches:
        num = art.split()[-1]
        articles.append({
            "article_number": num,
            "article_title": clean_text(title),
            "text": clean_text(body)
        })
    return articles

# ----------------------------------------
# PSR TABLE (pages from PSR start onward)
# ----------------------------------------
def classify_psr_rule(text: str) -> str:
    t = text.lower()
    if "wholly obtained" in t:
        return "WO"
    if "%" in t or "percent" in t or "value" in t:
        return "RVC"
    if "change" in t and "heading" in t:
        return "CTH"
    return "OTHER"

# Left cell parser: split into heading + description
LEFT_SPLIT_RE = re.compile(
    r"^(?P<head>(?:ex\s+)?(?:Chapter\s+\d+|(?:ex\s*)?\d{4}(?:\s\d{2})?))\s*(?P<desc>.*)$",
    flags=re.IGNORECASE,
)

CHAPTER_RE = re.compile(r"^(?:ex\s+)?Chapter\s+\d+", flags=re.IGNORECASE)
HEADING_RE = re.compile(r"^(?:ex\s*)?\d{4}(?:\s\d{2})?$", flags=re.IGNORECASE)

def extract_psr_from_text(psr_text: str):
    """
    Parse table-like lines. We rely on '|' as a divider when present.
    We:
      - keep current chapter from lines like 'ex Chapter 3 ... | ...'
      - start a new row when left cell begins with Chapter or HS code (ex 0306 / 0306 / 0511 91)
      - accumulate continuation lines (where left doesn't start with a heading/chapter) into description/right
    """
    rows = []
    current_chapter = None
    current = None

    lines = [ln for ln in (ln.strip() for ln in psr_text.splitlines()) if ln]

    for ln in lines:
        if "|" not in ln:
            # If no divider, treat as continuation to whichever side makes sense
            if current:
                # Heuristic: short fragments -> description; otherwise -> required_processing
                if len(ln) < 80:
                    current["description"] = clean_text(current["description"] + " " + ln)
                else:
                    current["required_processing"] = clean_text(current["required_processing"] + " " + ln)
            continue

        left, right = ln.split("|", 1)
        left = left.strip()
        right = right.strip()

        m = LEFT_SPLIT_RE.match(left)
        if m:
            head = clean_text(m.group("head"))
            desc = clean_text(m.group("desc"))

            # If this starts a new logical row, flush previous
            if current:
                rows.append(current)
                current = None

            if CHAPTER_RE.match(head):
                # This is a Chapter line. It can be a row itself (Chapter rule) AND sets context.
                current_chapter = head
                current = {
                    "chapter": head,            # chapter row
                    "heading": head,            # keep for completeness
                    "description": desc,
                    "required_processing": right,
                }
            else:
                # HS heading row under the latest chapter
                current = {
                    "chapter": current_chapter,
                    "heading": head,
                    "description": desc,
                    "required_processing": right,
                }
        else:
            # Continuation row (left cell has no heading at start)
            if current:
                if left:
                    current["description"] = clean_text(current["description"] + " " + left)
                if right:
                    current["required_processing"] = clean_text(current["required_processing"] + " " + right)
            else:
                # No active row -> skip
                continue

    if current:
        rows.append(current)

    # Post-clean + rule typing; keep only sane rows (must have heading)
    cleaned = []
    for r in rows:
        if not r.get("heading"):
            continue
        r["description"] = clean_text(r.get("description", ""))
        r["required_processing"] = clean_text(r.get("required_processing", ""))
        r["rule_type"] = classify_psr_rule(r["required_processing"])
        cleaned.append(r)

    return cleaned

# -------------------------
# MAIN OCR + SPLITTING
# -------------------------
def main(pdf_path: str, output_path: str):
    print("📄 Converting PDF to images (300 dpi)…")
    pages = convert_from_path(pdf_path, dpi=300)

    print(f"🔍 OCR {len(pages)} pages…")
    page_texts = []
    for i, pg in enumerate(pages, 1):
        txt = pytesseract.image_to_string(pg, lang="eng", config=TESS_CFG)
        page_texts.append(txt)

    # Find PSR start page by phrase; fallback to index 22 (page 23) if not found
    psr_start_idx = None
    for i, t in enumerate(page_texts):
        if re.search(r"LIST OF REQUIRED WORKING OR PROCESSING", t, flags=re.IGNORECASE):
            psr_start_idx = i
            break
    if psr_start_idx is None:
        psr_start_idx = 22  # fallback

    # Articles: everything before PSR start
    articles_text = "\n".join(page_texts[:psr_start_idx])
    articles = extract_articles_from_text(articles_text)

    # PSR pages: from start to end
    psr_text = "\n".join(page_texts[psr_start_idx:])
    product_specific_rules = extract_psr_from_text(psr_text)

    out = {
        "articles": articles,
        "product_specific_rules": product_specific_rules,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved structured output to: {output_path}")
    print(f"🧾 Articles: {len(articles)} | PSR rows: {len(product_specific_rules)}")

if __name__ == "__main__":
    main(pdf_path="data/evfta.pdf", output_path="data/evfta_full_clean.json")
