# 📘 **roo_extractor**
### Automated Extraction of Rules of Origin (RoO) from the EU–Vietnam Free Trade Agreement (EVFTA)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📐 **Architecture Overview**

```
PDF → Poppler (image conversion) → Tesseract OCR → Text
       ↓
 Document Splitter → Articles Parser
       ↓
  PSR Table Rebuilder → Rule Type Classifier
       ↓
          JSON Output
```

---

## **Overview**
`roo_extractor` is a Python-based extraction pipeline designed to convert the EU–Vietnam Free Trade Agreement (EVFTA) PDF into a structured machine-readable representation of legal articles and product‑specific rules of origin.

---

## **Key Features**
- High‑quality OCR using Poppler + Tesseract  
- Automatic segmentation into Articles & PSR Annex  
- Reconstruction of semi‑structured PSR tables  
- Rule classification (WO, CTH, RVC, OTHER)  
- Clean, structured JSON output  

---

## **Methodology Summary**
1. OCR preprocessing  
2. Document segmentation  
3. Regex‑based article parsing  
4. PSR table reconstruction  
5. Rule inference  

---

# ⚙️ **Environment Setup (PowerShell – Windows)**

## 1. Create a virtual environment
```powershell
python -m venv .venv
```

## 2. Activate it
```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 3. Install dependencies
```powershell
pip install -r requirements.txt
```

---

# 🔧 **Install Required External Tools**

## ✅ Poppler (required for pdf2image)
1. Download from GitHub:  
   https://github.com/oschwartz10612/poppler-windows/releases  
2. Extract to:  
   `C:\\poppler`  
3. Ensure this directory exists:  
   `C:\\poppler\\poppler-XX.XX.XX\\Library\\bin`

Your script uses:
```python
POPPLER_PATH = r"C:\\poppler\\poppler-XX.XX.XX\\Library\\bin"
```

---

## ✅ Tesseract OCR
Download (Windows):  
https://github.com/UB-Mannheim/tesseract/wiki

Install to:
```
C:\\Program Files\\Tesseract-OCR
```

The script automatically points to it.

---

# ▶️ **Usage (PowerShell)**

### Activate environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### Run extractor
```powershell
python scripts\preprocess_evfta.py
```

---

# 📁 **Repository Structure**

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

# 🛠 **Troubleshooting**

### ❗ Poppler not found (`PDFInfoNotInstalledError`)
Ensure:
```
C:\poppler\poppler-XX.XX.XX\Library\bin
```
contains:
- pdfinfo.exe  
- pdftoppm.exe  

And update script path accordingly.

---

### ❗ Tesseract not found
Check:
```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

### ❗ Virtual environment not activating
Run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

# 📚 **Citation**

### Plain-Text
Kqiraj, Kened. *roo_extractor: Automated Extraction of RoO from the EVFTA.* GitHub Repository, 2025.

### BibTeX
```bibtex
@misc{roo_extractor2025,
  author       = {Kened Kqiraj},
  title        = {roo_extractor: Automated Extraction of Rules of Origin (RoO)},
  year         = {2025},
  howpublished = {\url{https://github.com/kennedkqiraj/roo_extractor}},
}
```

### APA
Kqiraj, K. (2025). *roo_extractor: Automated extraction of Rules of Origin.* GitHub repository.

