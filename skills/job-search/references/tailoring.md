# Tailoring a Resume to a Posting

Read this when the person picks a specific role and wants their resume adapted to it.

## The reframe, not the rewrite

Keep every fact. Change the lens.

The same work described for a different audience is not dishonesty — it's translation. Someone who "coordinated with clinicians, caseworkers, and courts" has done **stakeholder management**. Someone who "served as community liaison with healthcare providers" has done **provider relations**. Use the posting's vocabulary for work they genuinely did.

What crosses the line: claiming systems they haven't used, inventing metrics, or implying a title they never held. If the reframing requires a fact that isn't true, stop.

Also over the line, and each one has happened in practice:

- **Placeholder or invented employers.** Every company on the resume must come from the record.
- **Certifications that aren't in the documents.** List earned ones as earned and in-progress ones as "pending" or "in progress." Never add a common credential because the posting wants it.
- **Duties borrowed from an unrelated industry.** Rephrase real duties toward the posting. Don't import the posting's industry into a job that had nothing to do with it.
- **Inflated scale.** If the work was small-scale, don't let it read as enterprise or large-infrastructure work.

## Completeness: never drop something silently

The most common complaint about generated resumes is "why did you leave out X?" Before writing, list everything in the standing record: roles, certifications and education. Then:

- Include every certification and all education unless the person says otherwise. Put the most relevant certification first.
- Cover the full span of history the person asks for (for example 10 years) as continuous experience, with no unexplained gaps.
- Use reverse chronological order. Ended roles get an end date; only a current role says "Present."
- Keep the person's own structure: DBA names, sub-projects nested under the parent company, merged date ranges for a pivot inside one company.
- If you leave anything out for length or relevance, say which items and why, in one line under the draft.
- When updating an existing version, add to that version. Don't start over and lose content.

## Format defaults: ask once, then always apply

Ask about these once, save the answers to the standing record, and apply them to every version without being reminded:

- Bullets per role (commonly 3–4) and bullet style (small Unicode bullets work in most ATS imports)
- No italics, em dashes, emojis or source citations in the document
- Summary as a short paragraph, followed by core competencies separated with `|`
- Core competencies and skills sections hold different items, with no overlap
- Certifications in their own section, separate from technical skills; skills last unless told otherwise
- Duties grouped under competency sub-headings ("sectioned bullets") when the person prefers it

Don't add sections the person didn't ask for.

## Find the hidden qualification

Before writing, look for experience the person doesn't think of as relevant:

- **Volunteer or campaign work** is often the best evidence of business development, territory building, and team management — and it's usually missing from the resume entirely.
- **Self-directed projects** (raising money, founding a program, producing something) demonstrate the closing and ownership that service roles don't show.
- **Side identities** that seem unrelated can be the strongest signal at a company whose leadership shares them.

## ATS optimization — measure, don't assume

Extract the posting's required-skills and responsibility language into a term list, then check the resume against it programmatically:

```python
import re
resume = open("resume.txt").read().lower().replace("\n", " ")
terms = ["account management", "provider relations", "stakeholder", ...]
missing = [t for t in terms if t not in resume]
print(f"coverage: {len(terms)-len(missing)}/{len(terms)}")
print("missing:", missing)
```

Convert the .docx to text first (`pdftotext -layout` on a PDF render, or python-docx) and normalize line breaks — a term split across two lines will read as missing when it isn't.

Aim for 90%+ coverage of terms the person can truthfully claim. Weave missing terms into the competencies section and the bullets where the work actually happened, not into a keyword dump.

**Test an actual import when the person applies through a parsing ATS** (Workday is common). Parsers can cut a bullet off at a special character (a bullet ending at an open parenthesis, for example) or fail to pull the company name. If the import truncates, simplify punctuation in the affected lines and put employer, title and dates on standard separate lines.

**Structural requirements:** no tables, no text boxes, no multi-column layouts, no headers/footers for contact info, standard section titles ("Professional Experience," not "Where I've Been"), real text rather than images, .docx format.

## Handling a requirement they don't meet

Do not fake it, and do not ignore it.

For a tool or system they lack: name the closest true analogue, then be explicit that they'll learn the specific platform. A resume line like "activity and follow-up tracking in EHR and case management systems; CRM-transferable pipeline tracking" gets the concept past a filter without claiming software they've never opened.

Flag the gap to the person directly so they can address it in the interview rather than being caught by it.

## Length and structure

Two pages maximum for most roles. If it runs over, cut the lowest-value bullets before shrinking margins or fonts.

Render and *look at it* before delivering — convert to PDF and view the pages. Tab stops fail, dates collide with employer names, and a single orphaned line on page three is common. These are invisible in the source and obvious on the page.

## Common structural fixes

- Right-align dates with an explicit tab stop position rather than a MAX constant, which can fail silently in some renderers.
- Group bullets under competency sub-headings within each job — it makes a dense resume scannable.
- Put the strongest evidence for *this specific role* on page one, even if chronology suggests otherwise.

## After tailoring

Roast the result before the person sends it. Read it as the hiring manager would and name what's actually weak — missing metrics, an unaddressed requirement, an identity conflict, an unexplained gap. It's more useful to hear it now than to lose the role and never learn why.
