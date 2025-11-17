# 📘 **roo_extractor**
### Automated Extraction of Rules of Origin (RoO) from the EU–Vietnam Free Trade Agreement (EVFTA)

## **Overview**
`roo_extractor` is a Python-based extraction pipeline designed to convert the EU–Vietnam Free Trade Agreement (EVFTA) PDF into a structured machine-readable representation of:

- Legal Articles  
- Product-Specific Rules of Origin (PSR), including HS chapters/headings, descriptions, required processing, and inferred rule types  

The tool is part of a master thesis focused on automating origin assessments using NLP and LegalBERT fine-tuning.

---

## **Key Features**

### **1. OCR Processing**
- Converts EVFTA PDF pages to images (300 dpi)  
- Uses Tesseract OCR with configuration optimized for legal text and table-like structures

### **2. Legal Article Extraction**
- Extracts articles, titles, and full text before the PSR Annex

### **3. PSR Table Parsing**
- Rebuilds semi-structured OCR output into normalized table rows  
- Identifies chapters, HS headings, descriptions, and processing requirements  
- Automatically assigns rule types (WO, CTH, RVC, OTHER)

### **4. Structured JSON Output**
Output format:

```json
{
  "articles": [...],
  "product_specific_rules": [...]
}
```

---

## **Methodology Summary**
1. OCR preprocessing  
2. Document segmentation (Articles vs PSR Annex)  
3. Regex-based article parsing  
4. Heuristic PSR table reconstruction and rule-type inference  

---

# **Virtual Environment Setup (Windows, macOS, Linux)**

To ensure reproducible execution, use a Python virtual environment.

## **1. Create a Virtual Environment**

### Windows (CMD or PowerShell)
```cmd
python -m venv .venv
```

### macOS / Linux (bash / zsh)
```bash
python3 -m venv .venv
```

## **2. Activate the Virtual Environment**

### Windows CMD
```cmd
.\.venv\Scripts\Activate
```

### Windows PowerShell
```powershell
.\.venv\Scripts\Activate.ps1
```

If you see an execution policy error:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Git Bash (Windows)
```bash
source .venv/Scripts/activate
```

### macOS / Linux
```bash
source .venv/bin/activate
```

## **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pdf2image pytesseract pillow
```

## **4. Deactivate Environment**
```bash
deactivate
```

---

## **Usage**

### Install Dependencies
```bash
pip install pdf2image pytesseract pillow
```

### Run Extractor
```bash
python preprocessing_evfta.py
```

---

## **Repository Structure**
```
roo_extractor/
├─ data/
│  ├─ evfta.pdf
│  └─ evfta_full_clean.json
├─ scripts/
│  └─ preprocess_evfta.py
├─ ocr_articles_text.txt
├─ ocr_full_text.txt
├─ requirements.txt
└─ README.md

```

---

# 📚 **Citation**

### **Plain-Text Citation**
Kqiraj, Kened. *roo_extractor: Automated Extraction of Rules of Origin (RoO) from the EU–Vietnam Free Trade Agreement using OCR and Heuristic Parsing.* GitHub Repository, 2025. Available at: https://github.com/kennedkqiraj/roo_extractor.

### **BibTeX**
```bibtex
@misc{roo_extractor2025,
  author       = {Kened Kqiraj},
  title        = {roo\_extractor: Automated Extraction of Rules of Origin (RoO) from the EU--Vietnam Free Trade Agreement using OCR and Heuristic Parsing},
  year         = {2025},
  howpublished = {\url{https://github.com/kennedkqiraj/roo_extractor}},
  note         = {GitHub repository}
}
```

### **APA**
Kqiraj, K. (2025). *roo_extractor: Automated extraction of Rules of Origin (RoO) from the EU–Vietnam Free Trade Agreement using OCR and heuristic parsing.* GitHub repository. https://github.com/kennedkqiraj/roo_extractor
