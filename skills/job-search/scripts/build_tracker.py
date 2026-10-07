#!/usr/bin/env python3
"""
Build a two-tab job match spreadsheet from a single source of truth.

Why a script: appending rows to an existing workbook silently overwrites
adjacent rows and desynchronizes the link column from the company column.
Keep all data in MATCHES/RULED_OUT below and regenerate the whole file.

Usage:
    Edit MATCHES and RULED_OUT, then:
    python build_tracker.py output.xlsx
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ---- EDIT THESE -------------------------------------------------------------
# (region, status, company, title, pay, score, why_it_fits, gap_to_watch, resume, contact, url)
# status: "NEW" | "REACH" | "Applied"
# resume: which standing version to send, e.g. "STAFFING / HR"
# contact: named recruiter/manager/phone/email from the posting, or "" if none
MATCHES = [
    ("Remote (US)", "NEW", "Example Co", "Example Title", "$50,000/yr", 88,
     "Why this fits their specific background — requirements they meet, work that matches.",
     "The specific risk, and the action to take if there is one.",
     "STAFFING / HR", "Jane Doe, Recruiter (LinkedIn poster)",
     "https://example.com/job"),
]

# (date, status, company, title, location, note)
# status: "Applied" | "Application viewed" | "Not selected"
# Import from the person's existing application history so they don't re-apply.
ALREADY_APPLIED = [
    ("Jun 10", "Not selected", "Example Co", "Example Title", "Atlanta, GA",
     "Rejected before the resume was updated — worth re-applying if reposted."),
]

# (company, title, location, pay, hard_blocker, url)
RULED_OUT = [
    ("Example Co", "Licensed Role", "Anywhere", "$70,000/yr",
     "Requires clinical licensure (LCSW/LMHC).", "https://example.com/job2"),
]

TITLE = "Job Matches"
SUBTITLE = ("Scored against actual background. GOLD = NEW, ready to apply. "
            "BLUE = REACH, one requirement unmet, pursue via outreach. GREY = already applied.")
# -----------------------------------------------------------------------------

NAVY, RED, WHITE = "14242D", "C4122F", "FFFFFF"
FILLS = {"NEW": "FFF3D6", "REACH": "E4EEF8", "Applied": "ECECEC"}
STATUS_COLOR = {"NEW": "1E7A4D", "REACH": "1F4E79", "Applied": "888888"}

thin = Side(style="thin", color="D8D3C8")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
A = Font(name="Arial", size=10)
AB = Font(name="Arial", size=10, bold=True)
AH = Font(name="Arial", size=10, bold=True, color=WHITE)
AT = Font(name="Arial", size=14, bold=True, color=WHITE)
LINK = Font(name="Arial", size=9, color="0563C1", underline="single")
WRAP = Alignment(wrap_text=True, vertical="top")
CTR = Alignment(wrap_text=True, vertical="center", horizontal="center")
LEFT = Alignment(wrap_text=True, vertical="center", horizontal="left")


def header(ws, cols, widths, title, subtitle):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    last = get_column_letter(len(cols))
    ws.merge_cells(f"A1:{last}1")
    c = ws["A1"]
    c.value, c.fill, c.font = title, PatternFill("solid", fgColor=RED), AT
    c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[1].height = 30
    ws.merge_cells(f"A2:{last}2")
    c = ws["A2"]
    c.value = subtitle
    c.font = Font(name="Arial", size=9, italic=True, color="555555")
    c.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
    ws.row_dimensions[2].height = 30
    for i, h in enumerate(cols, 1):
        x = ws.cell(row=4, column=i, value=h)
        x.fill, x.font, x.alignment, x.border = PatternFill("solid", fgColor=NAVY), AH, CTR, BORDER
    ws.row_dimensions[4].height = 28
    ws.freeze_panes = "A5"


def build(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Matches (60+)"
    ws.sheet_view.showGridLines = False
    cols = ["#", "Region", "Status", "Company", "Title", "Pay",
            "Match /100", "Why it fits", "Gap to watch", "Resume to use",
            "Contact", "Apply link (clickable)"]
    header(ws, cols, [4, 15, 9, 24, 30, 20, 8, 40, 36, 16, 26, 42], TITLE, SUBTITLE)

    r = 5
    for i, (region, status, co, title, pay, score, why, gap, resume, contact, url) in enumerate(MATCHES, 1):
        fill = PatternFill("solid", fgColor=FILLS[status])
        for ci, v in enumerate([i, region, status, co, title, pay, score, why, gap, resume, contact], 1):
            x = ws.cell(row=r, column=ci, value=v)
            x.font = AB if ci in (1, 7) else A
            x.alignment = CTR if ci in (1, 2, 3, 7, 10) else WRAP
            x.border, x.fill = BORDER, fill
            if ci == 3:
                x.font = Font(name="Arial", size=9, bold=True, color=STATUS_COLOR[status])
            if ci == 11 and v:
                x.font = Font(name="Arial", size=9, bold=True, color="1F4E79")
        x = ws.cell(row=r, column=12, value=url)
        if url.startswith("http"):
            x.hyperlink, x.font = url, LINK
        else:
            x.font = Font(name="Arial", size=9, italic=True, color="808080")
        x.alignment, x.border, x.fill = LEFT, BORDER, fill
        ws.row_dimensions[r].height = max(84, (max(len(why), len(gap)) // 38 + 1) * 15)
        r += 1

    ws2 = wb.create_sheet("Ruled Out")
    ws2.sheet_view.showGridLines = False
    cols2 = ["Company", "Title", "Location", "Pay",
             "Hard blocker (why it's out)", "Job link (clickable)"]
    header(ws2, cols2, [25, 32, 22, 20, 50, 42], "Ruled Out — hard blocker named",
           "Each has a requirement that can't be argued around. Named so they aren't re-evaluated later.")

    r = 5
    for i, (co, title, loc, pay, blocker, url) in enumerate(RULED_OUT):
        fill = PatternFill("solid", fgColor="F5F5F5") if i % 2 else None
        for ci, v in enumerate([co, title, loc, pay, blocker], 1):
            x = ws2.cell(row=r, column=ci, value=v)
            x.font = AB if ci == 1 else A
            x.alignment, x.border = WRAP, BORDER
            if fill:
                x.fill = fill
        x = ws2.cell(row=r, column=6, value=url)
        x.hyperlink, x.font, x.alignment, x.border = url, LINK, LEFT, BORDER
        if fill:
            x.fill = fill
        ws2.row_dimensions[r].height = max(46, (len(blocker) // 50 + 1) * 15)
        r += 1

    if ALREADY_APPLIED:
        ws3 = wb.create_sheet("Already Applied")
        ws3.sheet_view.showGridLines = False
        cols3 = ["Date", "Status", "Company", "Title", "Location", "Note"]
        header(ws3, cols3, [10, 18, 30, 40, 22, 50], "Already Applied — do not re-apply",
               "Imported from their application history. Check here before adding anything to the Matches tab.")
        stat_fill = {"Not selected": "FFC7CE", "Application viewed": "FFEB9C", "Applied": "DDEBF7"}
        r = 5
        for (d, st, co, title, loc, note) in ALREADY_APPLIED:
            for ci, v in enumerate([d, st, co, title, loc, note], 1):
                x = ws3.cell(row=r, column=ci, value=v)
                x.font, x.alignment, x.border = A, WRAP, BORDER
                if ci == 2:
                    x.fill = PatternFill("solid", fgColor=stat_fill.get(st, "DDEBF7"))
                    x.alignment = CTR
            r += 1

    wb.save(path)

    # verify: links present and paired, and no match duplicates an applied role
    bad = [m[2] for m in MATCHES if not m[10].startswith("http")]
    applied_keys = {(a[2].lower(), a[3].lower()) for a in ALREADY_APPLIED}
    dupes = [m[2] for m in MATCHES if (m[2].lower(), m[3].lower()) in applied_keys]
    print(f"Wrote {path} — {len(MATCHES)} matches, {len(RULED_OUT)} ruled out, "
          f"{len(ALREADY_APPLIED)} already applied.")
    if bad:
        print("NOTE: rows without a URL (search-string placeholders):", bad)
    if dupes:
        print("WARNING: these matches were already applied to:", dupes)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "job_matches.xlsx")
