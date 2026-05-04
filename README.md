Batch screen multiple PDF resumes against a Job Description using Claude Sonnet 4.5 — and get a clean, visual HTML report with scores, insights, and hiring recommendations.

✨ Features
📄 Batch Resume Screening — Process multiple PDFs at once
🎯 Match Scoring (0–100) — Quickly identify top candidates
🧠 AI-Powered Insights — Summary, strengths, gaps, missing skills
📊 Score Breakdown — Skills · Experience · Education · Fit
🏷 Clear Verdicts — Strong Match → Reject
🌐 Beautiful HTML Reports — No setup required, open in browser
⚡ Fast & Automated — From resumes → decision-ready insights
---

ai_resume_screener/
│
├── screener.py           # 🚀 Main entry point
├── report_generator.py   # 📊 HTML report builder
├── requirements.txt      # 📦 Dependencies
├── sample_jd.txt         # 📝 Sample Job Description
│
├── resumes/              # 📂 Drop resumes here
│   ├── candidate1.pdf
│   └── candidate2.pdf
│
└── reports/              # 📂 Generated reports
    └── screening_report_YYYYMMDD_HHMMSS.html
---

## ⚙️ Setup
**1. Clone the repo**
git clone https://github.com/your-username/ai-resume-screener.git
cd ai-resume-screener

**2. Install dependencies**
pip install -r requirements.txt

**3. Set your API key**
macOS / Linux
export ANTRHOPIC_KEY="your-api-key"

Windows (CMD)
set ANTRHOPIC_KEY=your-api-key

Windows (PowerShell)
$env:ANTRHOPIC_KEY="your-api-key"

## 🚀 Usage

### Basic Run

```bash
python screener.py --jd sample_jd.txt
```
## 📊 Output
### Terminal (live progress)

```
============================================================
  AI Resume Screener — Claude Sonnet 4.5
============================================================
  Found 3 resume(s) to screen.

[1/3] Screening: john_doe.pdf
  ✓ Extracted 3241 characters from resume
  ⏳ Sending to CLAUDE for analysis...
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
              Claude Sonnet (AI analysis)
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
MODEL_NAME = "claude-sonnet-4.5"
```
### Adjust the Screening Prompt

Edit `SCREENING_PROMPT` in `screener.py` to customize what the AI looks for, scoring criteria, output fields, etc.

---

## ⚠️ Notes

- **Scanned PDFs** (image-only) may produce empty text extraction. Use text-based PDFs for best results.
- Reports are self-contained HTML files — no server needed, just open in any browser.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `pdfplumber` | PDF text extraction |
| `google-generativeai` | Gemini AI API client |
| `jinja2` | (Available for future template use) |

---
