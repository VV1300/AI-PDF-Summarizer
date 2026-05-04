"""
AI Resume Screener — powered by Claude (Anthropic)
Batch screens multiple PDF resumes against a Job Description (JD).
Outputs: Match Score | Summary | Verdict | Missing Skills
API key is loaded from .env file (ANTHROPIC_API_KEY).
"""

import os
import sys
import json
import argparse
import pdfplumber
import anthropic
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from report_generator import generate_html_report

# ── Load .env file ──────────────────────────────────────────────────────────────
load_dotenv()

# ── Configuration ──────────────────────────────────────────────────────────────

MODEL_NAME = "claude-sonnet-4-5"

SCREENING_PROMPT = """
You are an expert HR recruiter and talent acquisition specialist.
Analyze the resume below against the provided Job Description (JD) and return a structured JSON response.

JOB DESCRIPTION:
{jd}

RESUME:
{resume}

Return ONLY a valid JSON object with this exact structure (no markdown, no extra text):
{{
  "candidate_name": "Full name extracted from resume, or 'Unknown Candidate' if not found",
  "match_score": <integer 0-100>,
  "score_breakdown": {{
    "skills_match": <integer 0-100>,
    "experience_match": <integer 0-100>,
    "education_match": <integer 0-100>,
    "overall_fit": <integer 0-100>
  }},
  "summary": "<2-3 sentence professional summary of the candidate based on their resume>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "missing_skills": ["<missing skill/requirement 1>", "<missing skill 2>"],
  "gaps": ["<gap 1>", "<gap 2>"],
  "verdict": "<one of: Strong Match | Good Match | Moderate Match | Weak Match | Not Suitable>",
  "verdict_reason": "<1-2 sentences explaining the verdict>",
  "recommendation": "<Shortlist | Consider | Reject>"
}}

Scoring guide:
- 85-100: Strong Match
- 70-84: Good Match
- 50-69: Moderate Match
- 30-49: Weak Match
- 0-29: Not Suitable
"""


# ── PDF Extraction ──────────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF resume using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"  [ERROR] Could not read {pdf_path}: {e}")
        return ""
    return text.strip()


# ── Claude AI Analysis ──────────────────────────────────────────────────────────

def analyze_resume(resume_text: str, jd_text: str, api_key: str) -> dict:
    """Send resume + JD to Claude and get structured screening result."""
    client = anthropic.Anthropic(api_key=api_key)
    prompt = SCREENING_PROMPT.format(jd=jd_text, resume=resume_text)

    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        raw = response.content[0].text.strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        return result

    except json.JSONDecodeError as e:
        print(f"  [WARN] JSON parse error: {e}")
        return {"error": str(e), "raw_response": response.content[0].text}
    except anthropic.AuthenticationError:
        print("  [ERROR] Invalid API key. Check your ANTHROPIC_API_KEY in the .env file.")
        sys.exit(1)
    except anthropic.RateLimitError:
        print("  [ERROR] Rate limit hit. Please wait a moment and try again.")
        return {"error": "Rate limit exceeded"}
    except Exception as e:
        print(f"  [ERROR] Claude API call failed: {e}")
        return {"error": str(e)}


# ── Batch Screener ──────────────────────────────────────────────────────────────

def screen_resumes(resume_dir: str, jd_text: str, api_key: str) -> list:
    """Screen all PDF resumes in the given directory."""
    resume_paths = sorted(Path(resume_dir).glob("*.pdf"))

    if not resume_paths:
        print(f"[!] No PDF files found in: {resume_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  AI Resume Screener — Claude (Anthropic)")
    print(f"  Model: {MODEL_NAME}")
    print(f"{'='*60}")
    print(f"  Found {len(resume_paths)} resume(s) to screen.\n")

    results = []

    for i, pdf_path in enumerate(resume_paths, 1):
        print(f"[{i}/{len(resume_paths)}] Screening: {pdf_path.name}")

        # Extract text
        resume_text = extract_text_from_pdf(str(pdf_path))
        if not resume_text:
            print(f"  [SKIP] Could not extract text from {pdf_path.name}\n")
            continue
        print(f"  ✓ Extracted {len(resume_text)} characters from resume")

        # AI Analysis
        print(f"  ⏳ Sending to Claude for analysis...")
        analysis = analyze_resume(resume_text, jd_text, api_key)

        if "error" in analysis:
            print(f"  [FAIL] Analysis failed: {analysis['error']}\n")
            continue

        # Attach metadata
        analysis["file_name"] = pdf_path.name
        results.append(analysis)

        # Quick terminal preview
        score = analysis.get("match_score", "N/A")
        verdict = analysis.get("verdict", "N/A")
        name = analysis.get("candidate_name", pdf_path.stem)
        print(f"  ✅ {name} | Score: {score}/100 | Verdict: {verdict}\n")

    # Sort by match score descending
    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return results


# ── CLI Entry Point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AI Resume Screener — Batch screen PDF resumes against a JD using Claude (Anthropic)"
    )
    parser.add_argument(
        "--resumes", "-r",
        default="resumes",
        help="Path to folder containing PDF resumes (default: ./resumes)"
    )
    parser.add_argument(
        "--jd", "-j",
        required=True,
        help="Path to a .txt file containing the Job Description"
    )
    parser.add_argument(
        "--output", "-o",
        default="reports",
        help="Output folder for HTML report (default: ./reports)"
    )

    args = parser.parse_args()

    # Load API key strictly from .env / environment — no CLI flag allowed
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("\n[ERROR] ANTHROPIC_API_KEY not found.")
        print("  → Create a .env file in this folder with:")
        print("      ANTHROPIC_API_KEY=your-key-here")
        print("  → Get your key at: https://console.anthropic.com/\n")
        sys.exit(1)

    print(f"  🔑 API key loaded from .env ✓")

    # Read JD
    jd_path = Path(args.jd)
    if not jd_path.exists():
        print(f"[ERROR] JD file not found: {args.jd}")
        sys.exit(1)
    jd_text = jd_path.read_text(encoding="utf-8").strip()
    print(f"  📋 Job Description loaded: {jd_path.name} ({len(jd_text)} chars)")

    # Screen resumes
    results = screen_resumes(args.resumes, jd_text, api_key)

    if not results:
        print("\n[!] No results generated. Check your resume PDFs and API key.")
        sys.exit(1)

    # Generate HTML report
    os.makedirs(args.output, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(args.output, f"screening_report_{timestamp}.html")

    generate_html_report(results, jd_text, report_path, jd_path.name)

    print(f"\n{'='*60}")
    print(f"  ✅ Screening Complete!")
    print(f"  📊 Screened : {len(results)} candidates")
    print(f"  📁 Report   : {report_path}")
    print(f"{'='*60}\n")

    # Print ranked summary table in terminal
    print(f"  {'RANK':<5} {'CANDIDATE':<30} {'SCORE':<8} {'VERDICT':<20} {'RECOMMEND'}")
    print(f"  {'-'*80}")
    for rank, r in enumerate(results, 1):
        name = r.get("candidate_name", "Unknown")[:28]
        score = r.get("match_score", 0)
        verdict = r.get("verdict", "N/A")
        rec = r.get("recommendation", "N/A")
        print(f"  {rank:<5} {name:<30} {score:<8} {verdict:<20} {rec}")
    print()


if __name__ == "__main__":
    main()