# Secure Entity Extractor

A Streamlit web application for cybersecurity Named Entity Recognition (NER) powered by the **SecureBERT-NER** model. Upload any plain-text threat report and receive a structured, interactive intelligence report in seconds.

---

## Features

- **Drag & drop upload** — supports `.txt` files of any length (automatic chunking for long documents)
- **Entity table** — every detected entity with its class, human-readable description, and occurrence count; live search filter included
- **Distribution charts** — switchable bar chart and donut chart showing entity class frequencies
- **CSV export** — download the full report as a spreadsheet
- **GPU-aware** — automatically uses CUDA if available, falls back to CPU

---

## Project structure

```
app/
├── app.py               # Entry point — UI orchestration only
├── config.py            # All constants: model path, entity metadata, colors
├── styles.py            # Custom CSS (isolated; edit here to restyle the app)
├── ner_service.py       # Abstract NERProvider + SecureBertNERProvider
├── entity_processor.py  # Data aggregation and filtering (pure logic, no UI)
├── charts.py            # Plotly chart builders (bar + donut)
├── components.py        # HTML snippet builders for custom UI elements
├── SecureBert-NER/      # Symlink → ../NER/SecureBert-NER (model files)
└── README.md            # This file
```

The code follows **SOLID principles** — each module has a single, well-defined responsibility. Quick guide to where to look when making changes:

| What you want to change | File to edit |
|---|---|
| Model path or entity classes | `config.py` |
| Colors, fonts, layout | `styles.py` |
| Swap or add an NER model | `ner_service.py` |
| Aggregation / filtering logic | `entity_processor.py` |
| Chart types or styling | `charts.py` |
| HTML blocks (table, cards, header) | `components.py` |
| Page flow / Streamlit widgets | `app.py` |

---

## Requirements

- Python 3.10+
- The project virtual environment (located at `../venv/`) with the following packages installed:

```
streamlit
plotly
transformers
torch
pandas
```

> All dependencies are listed in `../requirements.txt`.

---

## Installation

### 1. Clone / open the project

```bash
cd /path/to/AssignmentNER
```

### 2. Create or activate the virtual environment

```bash
# Create (first time only)
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify the model symlink

The `app/SecureBert-NER/` directory should be a symlink pointing to `NER/SecureBert-NER/`. If it is missing, recreate it:

```bash
ln -sf ../NER/SecureBert-NER app/SecureBert-NER
```

---

## Running the app

```bash
# From the project root with the venv active:
streamlit run app/app.py
```

Streamlit will print the local URL (default: `http://localhost:8501`). Open it in your browser.

> **First run:** the model (~473 MB) is loaded into memory on the first "Analyse" click and then cached for the rest of the session. Subsequent analyses are fast.

---

## How to use

1. **Upload** a `.txt` file using the drag-and-drop zone or the file browser.
2. Click **⚡ Analyse**.
3. Review the report:
   - **Summary cards** — number of entity classes, unique entities, and total mentions.
   - **Entity Extraction Report** — searchable table of all found entities.
   - **Entity Distribution** — bar chart and donut chart of class frequencies.
4. Click **⬇ Download report as CSV** to export the results.

---

## Supported entity classes

| Class | Description |
|---|---|
| `APT` | Advanced Persistent Threat |
| `ACT` | Action / Activity |
| `DOM` | Domain |
| `EMAIL` | Email Address |
| `ENCR` | Encryption Method |
| `FILE` | File |
| `IDTY` | Identity / Person |
| `IP` | IP Address |
| `LOC` | Location |
| `MAL` | Malware |
| `MD5` | MD5 Hash |
| `OS` | Operating System |
| `PROT` | Protocol |
| `SECTEAM` | Security Team |
| `SHA1` | SHA-1 Hash |
| `SHA2` | SHA-256 Hash |
| `TIME` | Time Reference |
| `TOOL` | Tool / Software |
| `URL` | URL |
| `VULID` | Vulnerability ID |
| `VULNAME` | Vulnerability Name |

---

## Extending the app

### Add a new entity class
Edit `config.py` and add an entry to `ENTITY_META`:
```python
"NEWCLASS": {"label": "Human Readable Name", "color": "#hex"},
```
No other file needs to change.

### Swap the NER model
1. Update `MODEL_PATH` in `config.py`.
2. If the new model has different output keys, override only `extract()` in a new `NERProvider` subclass in `ner_service.py`.
3. Update `app.py` to instantiate the new provider.

### Add a new chart type
Add a function to `charts.py` that accepts a DataFrame and returns a `go.Figure`, then call it from `app.py` inside a new `st.tab`.
