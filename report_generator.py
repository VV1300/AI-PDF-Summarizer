"""
report_generator.py
Generates a beautiful, self-contained HTML screening report.
"""

from datetime import datetime


def score_color(score: int) -> str:
    if score >= 85:
        return "#22c55e"   # green
    elif score >= 70:
        return "#84cc16"   # lime
    elif score >= 50:
        return "#f59e0b"   # amber
    elif score >= 30:
        return "#f97316"   # orange
    else:
        return "#ef4444"   # red


def verdict_badge(verdict: str) -> str:
    colors = {
        "Strong Match":   ("#dcfce7", "#166534"),
        "Good Match":     ("#d9f99d", "#3f6212"),
        "Moderate Match": ("#fef9c3", "#854d0e"),
        "Weak Match":     ("#ffedd5", "#9a3412"),
        "Not Suitable":   ("#fee2e2", "#991b1b"),
    }
    bg, fg = colors.get(verdict, ("#f3f4f6", "#374151"))
    return f'<span style="background:{bg};color:{fg};padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600;">{verdict}</span>'


def rec_badge(rec: str) -> str:
    colors = {
        "Shortlist": ("#dcfce7", "#166534"),
        "Consider":  ("#fef9c3", "#854d0e"),
        "Reject":    ("#fee2e2", "#991b1b"),
    }
    bg, fg = colors.get(rec, ("#f3f4f6", "#374151"))
    return f'<span style="background:{bg};color:{fg};padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600;">{rec}</span>'


def build_score_ring(score: int) -> str:
    color = score_color(score)
    pct = score  # 0-100 maps to stroke dashoffset
    circumference = 2 * 3.14159 * 45
    offset = circumference - (pct / 100) * circumference
    return f"""
    <svg width="110" height="110" viewBox="0 0 110 110">
      <circle cx="55" cy="55" r="45" fill="none" stroke="#e5e7eb" stroke-width="10"/>
      <circle cx="55" cy="55" r="45" fill="none" stroke="{color}" stroke-width="10"
        stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
        stroke-linecap="round" transform="rotate(-90 55 55)"/>
      <text x="55" y="60" text-anchor="middle" font-size="22" font-weight="700" fill="{color}">{score}</text>
    </svg>
    """


def build_mini_bar(label: str, value: int) -> str:
    color = score_color(value)
    return f"""
    <div style="margin-bottom:6px;">
      <div style="display:flex;justify-content:space-between;font-size:12px;color:#6b7280;margin-bottom:2px;">
        <span>{label}</span><span style="font-weight:600;color:{color};">{value}</span>
      </div>
      <div style="background:#e5e7eb;border-radius:4px;height:6px;">
        <div style="background:{color};width:{value}%;height:6px;border-radius:4px;transition:width 0.3s;"></div>
      </div>
    </div>
    """


def build_candidate_card(rank: int, r: dict) -> str:
    name = r.get("candidate_name", "Unknown Candidate")
    score = r.get("match_score", 0)
    file_name = r.get("file_name", "")
    summary = r.get("summary", "No summary available.")
    verdict = r.get("verdict", "N/A")
    rec = r.get("recommendation", "N/A")
    verdict_reason = r.get("verdict_reason", "")
    strengths = r.get("strengths", [])
    missing = r.get("missing_skills", [])
    gaps = r.get("gaps", [])
    breakdown = r.get("score_breakdown", {})

    strengths_html = "".join(
        f'<span style="background:#dcfce7;color:#166534;padding:3px 10px;border-radius:20px;font-size:12px;margin:2px;display:inline-block;">✓ {s}</span>'
        for s in strengths
    )
    missing_html = "".join(
        f'<span style="background:#fee2e2;color:#991b1b;padding:3px 10px;border-radius:20px;font-size:12px;margin:2px;display:inline-block;">✗ {m}</span>'
        for m in missing
    )
    gaps_html = "".join(
        f'<span style="background:#fef9c3;color:#854d0e;padding:3px 10px;border-radius:20px;font-size:12px;margin:2px;display:inline-block;">⚠ {g}</span>'
        for g in gaps
    )

    breakdown_html = ""
    for key, label in [("skills_match","Skills"), ("experience_match","Experience"),
                        ("education_match","Education"), ("overall_fit","Overall Fit")]:
        breakdown_html += build_mini_bar(label, breakdown.get(key, 0))

    border_color = score_color(score)

    return f"""
    <div style="background:#fff;border-radius:12px;border-left:5px solid {border_color};
         box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-bottom:24px;overflow:hidden;">

      <!-- Header -->
      <div style="padding:20px 24px;display:flex;align-items:center;gap:20px;border-bottom:1px solid #f3f4f6;">
        <div style="background:#f9fafb;border-radius:50%;width:36px;height:36px;display:flex;
             align-items:center;justify-content:center;font-weight:700;color:#6b7280;font-size:14px;">
          #{rank}
        </div>
        <div style="flex:1;">
          <div style="font-size:18px;font-weight:700;color:#111827;">{name}</div>
          <div style="font-size:12px;color:#9ca3af;margin-top:2px;">📄 {file_name}</div>
        </div>
        <div style="text-align:center;">
          {build_score_ring(score)}
          <div style="font-size:11px;color:#6b7280;margin-top:-4px;">Match Score</div>
        </div>
      </div>

      <!-- Body -->
      <div style="padding:20px 24px;display:grid;grid-template-columns:1fr 1fr;gap:24px;">

        <!-- Left column -->
        <div>
          <div style="margin-bottom:12px;">
            <div style="font-size:12px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">Summary</div>
            <p style="font-size:14px;color:#374151;line-height:1.6;margin:0;">{summary}</p>
          </div>

          <div style="margin-bottom:12px;">
            <div style="font-size:12px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">Verdict</div>
            <div style="margin-bottom:6px;">{verdict_badge(verdict)} &nbsp; {rec_badge(rec)}</div>
            <p style="font-size:13px;color:#6b7280;margin:6px 0 0;line-height:1.5;">{verdict_reason}</p>
          </div>

          <div>
            <div style="font-size:12px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">Score Breakdown</div>
            {breakdown_html}
          </div>
        </div>

        <!-- Right column -->
        <div>
          <div style="margin-bottom:14px;">
            <div style="font-size:12px;font-weight:600;color:#166534;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">✅ Strengths</div>
            <div>{strengths_html if strengths_html else '<span style="color:#9ca3af;font-size:13px;">None identified</span>'}</div>
          </div>

          <div style="margin-bottom:14px;">
            <div style="font-size:12px;font-weight:600;color:#991b1b;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">❌ Missing Skills</div>
            <div>{missing_html if missing_html else '<span style="color:#9ca3af;font-size:13px;">None — full match!</span>'}</div>
          </div>

          <div>
            <div style="font-size:12px;font-weight:600;color:#854d0e;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">⚠ Gaps / Concerns</div>
            <div>{gaps_html if gaps_html else '<span style="color:#9ca3af;font-size:13px;">No major gaps</span>'}</div>
          </div>
        </div>

      </div>
    </div>
    """


def generate_html_report(results: list, jd_text: str, output_path: str, jd_filename: str):
    """Generate a complete self-contained HTML screening report."""
    total = len(results)
    shortlisted = sum(1 for r in results if r.get("recommendation") == "Shortlist")
    consider = sum(1 for r in results if r.get("recommendation") == "Consider")
    rejected = sum(1 for r in results if r.get("recommendation") == "Reject")
    avg_score = round(sum(r.get("match_score", 0) for r in results) / total) if total else 0
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Build candidate cards
    cards_html = ""
    for rank, r in enumerate(results, 1):
        cards_html += build_candidate_card(rank, r)

    # Build summary table
    table_rows = ""
    for rank, r in enumerate(results, 1):
        name = r.get("candidate_name", "Unknown")
        score = r.get("match_score", 0)
        verdict = r.get("verdict", "N/A")
        rec = r.get("recommendation", "N/A")
        file_name = r.get("file_name", "")
        color = score_color(score)
        table_rows += f"""
        <tr style="border-bottom:1px solid #f3f4f6;">
          <td style="padding:10px 16px;color:#6b7280;font-size:13px;">#{rank}</td>
          <td style="padding:10px 16px;font-weight:600;font-size:13px;">{name}</td>
          <td style="padding:10px 16px;font-size:12px;color:#9ca3af;">{file_name}</td>
          <td style="padding:10px 16px;">
            <span style="color:{color};font-weight:700;font-size:14px;">{score}</span>
            <span style="color:#9ca3af;font-size:11px;">/100</span>
          </td>
          <td style="padding:10px 16px;">{verdict_badge(verdict)}</td>
          <td style="padding:10px 16px;">{rec_badge(rec)}</td>
        </tr>
        """

    jd_preview = jd_text[:600].replace("<", "&lt;").replace(">", "&gt;")
    if len(jd_text) > 600:
        jd_preview += "..."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Resume Screening Report</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f9fafb; color: #111827; }}
    .container {{ max-width: 960px; margin: 0 auto; padding: 32px 16px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th {{ text-align:left; padding: 10px 16px; font-size:11px; font-weight:600;
          text-transform:uppercase; letter-spacing:0.05em; color:#6b7280;
          background:#f9fafb; border-bottom:2px solid #e5e7eb; }}
    @media print {{
      body {{ background: white; }}
      .no-print {{ display: none; }}
    }}
  </style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div style="background:linear-gradient(135deg,#1e40af,#7c3aed);border-radius:16px;
       padding:36px;color:white;margin-bottom:28px;">
    <div style="font-size:13px;opacity:0.75;margin-bottom:8px;">🤖 Powered by Gemini 2.5 Flash</div>
    <h1 style="font-size:28px;font-weight:800;margin-bottom:8px;">AI Resume Screening Report</h1>
    <div style="font-size:14px;opacity:0.85;">📋 JD: {jd_filename} &nbsp;|&nbsp; 🕒 {timestamp}</div>
  </div>

  <!-- Stats -->
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:28px;">
    {"".join(f'''
    <div style="background:#fff;border-radius:10px;padding:16px;text-align:center;box-shadow:0 1px 6px rgba(0,0,0,0.06);">
      <div style="font-size:24px;font-weight:800;color:{c};">{v}</div>
      <div style="font-size:12px;color:#6b7280;margin-top:4px;">{l}</div>
    </div>''' for v, l, c in [
        (total, "Total Screened", "#1e40af"),
        (avg_score, "Avg Score", score_color(avg_score)),
        (shortlisted, "Shortlisted", "#16a34a"),
        (consider, "Consider", "#d97706"),
        (rejected, "Rejected", "#dc2626"),
    ])}
  </div>

  <!-- Summary Table -->
  <div style="background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-bottom:28px;overflow:hidden;">
    <div style="padding:16px 20px;border-bottom:1px solid #f3f4f6;">
      <h2 style="font-size:16px;font-weight:700;">📊 Candidate Rankings</h2>
    </div>
    <table>
      <thead>
        <tr>
          <th>Rank</th><th>Candidate</th><th>File</th><th>Score</th><th>Verdict</th><th>Recommendation</th>
        </tr>
      </thead>
      <tbody>{table_rows}</tbody>
    </table>
  </div>

  <!-- Detailed Cards -->
  <h2 style="font-size:18px;font-weight:700;margin-bottom:16px;">🔍 Detailed Analysis</h2>
  {cards_html}

  <!-- JD Reference -->
  <div style="background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-top:28px;">
    <div style="padding:16px 20px;border-bottom:1px solid #f3f4f6;">
      <h2 style="font-size:16px;font-weight:700;">📋 Job Description Reference</h2>
    </div>
    <div style="padding:20px;font-size:13px;color:#374151;line-height:1.7;white-space:pre-wrap;max-height:300px;overflow-y:auto;">{jd_preview}</div>
  </div>

  <div style="text-align:center;color:#9ca3af;font-size:12px;margin-top:28px;padding-bottom:16px;">
    Generated by AI Resume Screener · Gemini 2.5 Flash · {timestamp}
  </div>

</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  📄 HTML report saved to: {output_path}")
