# 🤖 AI Resume Screener

> Batch screen multiple PDF resumes against a Job Description using **Google Gemini 2.5 Flash**.
> Outputs: Match Score · Candidate Summary · Verdict · Missing Skills — all in a beautiful HTML report.

---

## 📁 Project Structure

```
ai_resume_screener/
│
├── screener.py           # Main entry point — run this
├── report_generator.py   # HTML report builder
├── requirements.txt      # Python dependencies
├── sample_jd.txt         # Example Job Description
│
├── resumes/              # 📂 Drop your PDF resumes here
│   └── candidate1.pdf
│   └── candidate2.pdf
│
└── reports/              # 📂 HTML reports are saved here (auto-created)
    └── screening_report_20250101_120000.html
```

---

## ⚙️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a free API key
3. Set it as an environment variable:

```bash
# macOS / Linux
export GEMINI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"
```

Or pass it directly via `--api-key` flag (see below).

---

## 🚀 Usage

### Basic Run

```bash
python screener.py --jd sample_jd.txt
```

This will:
- Read all `.pdf` files from the `resumes/` folder
- Screen each resume against `sample_jd.txt`
- Save an HTML report to the `reports/` folder

---

### Full Command Options

```bash
python screener.py \
  --resumes  ./resumes      \   # Folder with PDF resumes (default: ./resumes)
  --jd       ./sample_jd.txt\   # Path to JD text file (required)
  --output   ./reports      \   # Output folder for HTML report (default: ./reports)
  --api-key  YOUR_KEY           # Gemini API key (or use env var)
```

### Example with Custom Paths

```bash
python screener.py \
  --resumes ./candidates \
  --jd ./jobs/swe_senior.txt \
  --output ./screening_results \
  --api-key AIza...
```

---

## 📊 Output

### Terminal (live progress)

```
============================================================
  AI Resume Screener — Gemini 2.5 Flash
============================================================
  Found 3 resume(s) to screen.

[1/3] Screening: john_doe.pdf
  ✓ Extracted 3241 characters from resume
  ⏳ Sending to Gemini for analysis...
  ✅ John Doe | Score: 87/100 | Verdict: Strong Match

...

  RANK  CANDIDATE                      SCORE    VERDICT              RECOMMEND
  ────────────────────────────────────────────────────────────────────────────
  1     John Doe                       87       Strong Match         Shortlist
  2     Jane Smith                     71       Good Match           Consider
  3     Bob Johnson                    42       Weak Match           Reject
```

### HTML Report (saved to `reports/`)

Each report includes:
- **Stats dashboard** — Total screened, avg score, shortlisted, considered, rejected
- **Ranked summary table** — All candidates at a glance
- **Detailed candidate cards** with:
  - 🎯 Visual match score ring (0–100)
  - 📝 Professional candidate summary
  - ✅ Key strengths
  - ❌ Missing skills
  - ⚠ Gaps / concerns
  - Score breakdown bars (Skills, Experience, Education, Overall Fit)
  - Verdict badge + Recommendation badge
- **JD reference section**

---

## 🧠 How It Works

```
PDF Resumes  ──►  pdfplumber (text extraction)
                       │
                       ▼
              Gemini 2.5 Flash (AI analysis)
              ┌─────────────────────────────┐
              │  Resume + JD → structured   │
              │  JSON with score, verdict,  │
              │  strengths, missing skills  │
              └─────────────────────────────┘
                       │
                       ▼
              HTML Report Generator
              (ranked, visual, downloadable)
```

---

## 📋 Screening Outputs (per candidate)

| Output | Description |
|--------|-------------|
| **Match Score** | 0–100 integer representing how well the resume fits the JD |
| **Score Breakdown** | Sub-scores for Skills, Experience, Education, Overall Fit |
| **Summary** | 2–3 sentence professional profile of the candidate |
| **Strengths** | Key matching points between resume and JD |
| **Missing Skills** | JD requirements not found in the resume |
| **Gaps / Concerns** | Experience gaps, role mismatches, or red flags |
| **Verdict** | Strong Match / Good Match / Moderate Match / Weak Match / Not Suitable |
| **Recommendation** | Shortlist / Consider / Reject |

---

## 🔧 Customization

### Change the AI Model

In `screener.py`, update:
```python
MODEL_NAME = "gemini-2.5-flash-preview-04-17"
```

Available Gemini models: `gemini-2.5-pro`, `gemini-1.5-flash`, etc.

### Adjust the Screening Prompt

Edit `SCREENING_PROMPT` in `screener.py` to customize what the AI looks for, scoring criteria, output fields, etc.

---

## ⚠️ Notes

- **Scanned PDFs** (image-only) may produce empty text extraction. Use text-based PDFs for best results.
- **Gemini API rate limits** apply — for large batches (50+ resumes), add a `time.sleep(1)` between calls.
- Reports are self-contained HTML files — no server needed, just open in any browser.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `pdfplumber` | PDF text extraction |
| `google-generativeai` | Gemini AI API client |
| `jinja2` | (Available for future template use) |

---

*Built with ❤️ using Gemini 2.5 Flash*
