---
name: "job-search"
description: "Run a capability-based job search across Indeed, LinkedIn, and the web, score each role against the person's real background, and keep a persistent Job Search Tracker artifact (Active, Applied, Pipeline, Lower Matches, Archive, Ruled Out). Use for finding jobs, matching roles to a resume, career pivots, fit checks on a named role, stalled searches, interview prep, post-interview debriefs and thank-you notes, and whenever the person reports applying, pastes a closed posting or an interview transcript, or asks to update or clean the tracker."
---

# Job Search

A capability-based job search that finds roles a title search would miss, scores them honestly, and keeps everything in one live tracker the person can act on.

## The core idea

**Search what the person can DO, not what they've been CALLED.**

This is the whole skill. Title searches surface the jobs someone already knows about and hit the same walls repeatedly. Capability searches surface the jobs written for their skills under names they've never held.

A real example: forty title-based searches for a peer specialist ("peer specialist," "case manager," "outreach coordinator") suggested a hard ceiling around $45K, blocked everywhere by degree requirements. Searching capability language instead — "group facilitation," "harm reduction," "provider relations," "motivational interviewing" — surfaced a $52K fully-remote role where the person's certification *was* the requirement, and a $70–80K role where their lived experience and public speaking were the product. Those existed the entire time. The search design was hiding them.

A second real example: a revenue-systems candidate asked for roles "like" a consulting-firm Solutions Architect interview he was in. Searching the *shape* of that job (client-facing consultant who architects and builds CRM systems and trains the client, at a firm serving many clients, with AI in delivery) instead of its title surfaced a cluster of boutique HubSpot/Salesforce implementation firms that scored higher than the original role.

When a search stalls, the instinct is to conclude the market is empty. Usually the queries are wrong.

## Workflow

### Before searching: check the tools and the LinkedIn version

Do this once per session, before the first search.

**1. Confirm which channels are connected.** Look for the Indeed tools (`search_jobs`, `get_job_details`, `get_company_data`, `get_resume` from the Indeed connector) and the LinkedIn tools (`search_jobs`, `get_job_details`, `get_saved_jobs` and the rest from the "MCP Server for LinkedIn" extension). If one is missing, tell the person how to add it and fall back to web search for that channel. Don't fail silently:

- **Indeed:** Customize → Connectors → add **Indeed** and sign in.
- **LinkedIn:** download the `.mcpb` from https://github.com/stickerdaniel/linkedin-mcp-server/releases/latest and install it in Claude Desktop under Settings → Extensions. Double-clicking the file usually does nothing on Windows.

**2. Check the LinkedIn extension's version before relying on it.** The `.mcpb` bundle never updates itself, and LinkedIn page changes break older versions of a scraper. Results can come back empty or partial with no clear error.

- **Latest version:** the server checks PyPI, so use the same source: `https://pypi.org/pypi/mcp-server-linkedin/json` → `info.version`. If that's unreachable, use GitHub. Its API without a login is often rate-limited, so treat a "rate limit exceeded" reply as unavailable, not as a version: `https://api.github.com/repos/stickerdaniel/linkedin-mcp-server/releases/latest` → `tag_name`, without the leading `v`.
- **Installed version:** if you can read the person's files (Claude Code), read `"version"` from the extension's `manifest.json`:
  - Windows: `%APPDATA%\Claude\Claude Extensions\local.mcpb.daniel-sticker.linkedin-mcp-server\manifest.json`
  - macOS: `~/Library/Application Support/Claude/Claude Extensions/local.mcpb.daniel-sticker.linkedin-mcp-server/manifest.json`

  Otherwise, ask them to open Customize → Connectors → MCP Server for LinkedIn → **View details** and read the version. While they're there, check that the toggle says **Enabled**. A **Disabled** extension is the usual reason the LinkedIn tools are missing.
- **The server's own notice:** when it's a minor version or more behind (or two or more patch releases), the server adds a line to the first LinkedIn tool result of a session: *"Update available: mcp-server-linkedin X is out (you are on Y)…"*. If you see it, relay it. Don't drop it.

**If they're behind:** before searching, tell them both version numbers and how to update: download the latest `.mcpb` from the releases link above, install it under Settings → Extensions, then quit Claude Desktop from the tray icon and reopen it. Then let them choose to update first or continue on the old version. Don't download or install anything for them. If they continue and LinkedIn results look thin or broken, say the old version is the likely cause rather than concluding the market is empty.

If both version checks are unavailable (no network, no file access), say so in one line and continue.

### Load the person's standing record and preferences

Over a long search, people end up repeating the same corrections dozens of times: "include my certifications," "you left out that job," "that role has an end date," "don't use em dashes." Each repeat is a failure. Keep a **standing record** and apply it to every resume, answer and email without being asked again:

- **Master history:** every role with the exact title, employer, dates and how it should be described (a DBA name, sub-projects that belong under a parent company, a pivot inside one company), plus every certification (marked earned or pending) and all education.
- **Standing facts:** relocation stance, work-mode limits (remote only, no on-site), portfolio link to always include, salary floor, whether they do pre-recorded video interviews.
- **Don't-mention list:** things they don't want raised in answers (a business they owned, a side project, why they really left).
- **Format preferences:** see the list in `references/tailoring.md`.

Ask for anything missing once, near the start. Save it to memory if memory is available, and say what you saved. When the person corrects something, update the record in the same turn so the correction holds next time. Those repeated corrections are the main thing this section exists to prevent.

**Answer the question asked, first.** If the person asks a direct factual question ("does this company use HubSpot?"), answer it or say you don't know before doing anything else. Don't substitute a different, more convenient answer.

**Be fast.** Deliver the draft in the same turn. Don't announce a long "in-depth review" and come back later; that read as stalling and the person had to ask again.

### 0. Ingest what they've already applied to

Ask early whether they've been applying already, and how many. If yes, get the history before searching — most job boards can export it (Indeed's "My Jobs" page saves as .mhtml; LinkedIn has "My Items"), and confirmation emails in their inbox work too. Parse it into the tracker's **Archive** tab (prior search) and **Already Applied** tab (current round).

Two reasons this matters more than it sounds:

**It prevents duplicate applications.** Re-applying to a role someone already submitted to reads as disorganized and wastes a slot.

**The history is diagnostic.** Count the title words across everything they've applied to. If one term dominates, that channel is saturated and new searches on it will return the same postings:

```python
from collections import Counter
import re
words = Counter()
for t in applied_titles:
    for w in re.findall(r"[A-Za-z']+", t.lower()):
        if w not in {"and","of","the","in","for","a","to","i","ii"}:
            words[w] += 1
print(words.most_common(20))
```

A real result: 173 applications, 51 containing "coordinator," 26 "recruiter," 25 "specialist" — and zero interviews. That isn't a bad-luck problem or a resume problem, it's a targeting problem, and the counts prove it in a way an opinion can't. The two best roles found afterward came from searching "job placement" and "outreach specialist," terms describing the *outcome* and the *activity* rather than any title.

Also capture the status of each past application (submitted / viewed / rejected). A rejection that predates a resume improvement is worth re-applying to if the role reposts — note it.

### 1. Extract capabilities before searching

Read the resume and pull out the *verbs and skills*, not the job titles. Build a list of 15–25 search terms across these categories:

- **Hard skills**: the actual activities (group facilitation, budget management, curriculum design, crisis intervention)
- **Credentials**: certifications, licenses, instructor status — these are often the key that unlocks degree-walled roles
- **Populations/domains**: who or what they work with (justice-involved, pediatric, SMB, enterprise)
- **Tools/systems**: named platforms, methodologies, frameworks
- **Transferable achievements**: raised money, built a team, ran a territory, trained N people

Then search the language a *job description* would use for each, which is often different from resume language. "Coordinated with agencies" in a resume is "stakeholder management" or "provider relations" in a posting.

Confirm the capability list with the person before running 40 searches on the wrong terms. When they point at a specific role they liked ("find roles like this one"), extract that role's shape — function, setting, stack, client-facing or not, delivery motion — and search the shape.

### 2. Search broadly across channels

Cover these locations unless told otherwise: home city, commutable metros within an hour, fully remote, and any city they'd relocate to. Ask about relocation early — it changes the whole search.

**Channel behavior differs and matters:**

- **Indeed** handles local and metro searches well. Keyword matching is loose, so vary phrasing aggressively — different wordings surface genuinely different postings from the same pool.
- **LinkedIn** rewards *short* queries. Two- or three-word searches ("recovery coach", "Revenue Systems") return clean results; long keyword strings return almost pure promoted-ad inventory. If results come back as high-ticket closers, voice actors, and AI trainers, the query is too long. LinkedIn also silently "corrects" niche terms ("RevOps consultant" became "devops consultant") — check the "Showing results for" line. Search snippets often show pay; use that to triage before pulling details.
- **Job alert emails**: if the person has an email connector, their Indeed and LinkedIn job alerts and "jobs you may be interested in" digests are a free extra channel that needs no scraping. Pull the roles from them, pull full details where a tool allows, and score them like any other find. Never scrape a job board outside its official connector or tools; that breaks the board's terms.
- **Web search** works when platform tools are unavailable or rate-limited, and is good for finding company career pages directly. Boutique firms often list sibling roles (a junior and senior version of the same seat) only on their own careers page.

Expect rate limits. When one channel throttles, switch rather than stall. Two practical hazards: loading a new tool mid-session can silently unload the one already in use, so re-check what's available after switching; and when every channel is throttled, stop and give the person a concrete wait time rather than continuing to retry.

**Save findings to the tracker before the tools break, not after.** Republishing costs one call; re-running twenty searches to recover lost results costs the session.

### 3. Pull full details before scoring

Never score from a search snippet. Snippets omit the requirements that decide everything. Pull the full posting for anything promising. Check the posting's status line while you're there: "No longer accepting applications" or "Not currently accepting applications" means it's closed, whatever the snippet suggested.

**Exception:** skip the detail pull for roles blocked by title alone (a "Licensed Therapist" posting for someone without a license), or where a hard blocker is already recorded. Rule those out and move on — don't spend a call confirming the obvious.

### 4. Score honestly, 0–100

Score against what the person actually has, not a generous reading. Weight:
- Do they meet the stated requirements? (heaviest)
- Does the day-to-day work match their real experience?
- Is the level and pay a step forward, sideways, or back?
- Is it reachable — location, schedule, licensure?

**Three statuses:**

| Status | Meaning |
|---|---|
| **NEW** | Meets requirements, ready to apply |
| **REACH** | Strong fit, one requirement unmet — pursue via direct outreach, not a cold application |
| **Applied** | Already submitted, kept for reference |

**REACH is the highest-value category.** A posting where someone meets everything but one requirement, and the hiring manager is visible on the listing, is worth a direct message far more than an application that a filter will reject. Always name the specific outreach move.

When a posting lists several valid "expertise areas" (e.g., "Salesforce, HubSpot, AI, or Clay"), the person qualifies through whichever one they genuinely have. Score on that door, and name the area they'd be ramping on as the gap.

### 5. Read requirements carefully — the details are where opportunities hide

These patterns turn "blocked" into "eligible," and they are easy to miss:

- **Equivalency clauses**: "Bachelor's degree *or equivalent combination of education, training, and experience*" means experience substitutes.
- **Credential-in-lieu-of-degree**: "Bachelor's degree OR Certified Peer Recovery Specialist" — the certification *is* the qualification.
- **Alternate qualification paths**: buried options like "Case Worker with a minimum of 6 years experience" alongside the degree/license routes.
- **Preferred vs. required**: "Bachelor's preferred" is not a wall. "Bachelor's required" is.
- **National-credential acceptance**: a posting naming a state certification may accept an equivalent national one. Worth asking.
- **Mislabeled postings**: LinkedIn sometimes tags a senior role "Internship" or shows a city that differs from the body. Trust the body text, and note the mislabel.

**When a role scores high, search that employer for other locations and levels.** Large employers post the same job as separate requisitions per site, and boutique firms post a junior and senior version of one seat. Point the person at the level that matches where they actually are.

**Requirements are posting-specific, not company-wide.** The same employer, same job title, same pay band can have different requirements in different cities. Never generalize a requirement from one posting to a whole company — check each.

### 6. Name hard blockers in one line and move on

A hard blocker is a requirement that can't be argued around: a completed degree with no equivalency, a clinical license, a board certification, state residency, a language, a required on-site city, pay under the person's floor, a contract when they want full-time, or a closed posting.

Put these on the Ruled Out tab with the blocker named. Don't write a full analysis of a job the person can't get — that's wasted reading. But do name the blocker precisely so they don't re-evaluate the same posting in three weeks, and keep any warm contact in the blocker text in case it changes.

A low score is not a blocker. An open role the person could apply to that simply scores under their threshold goes to **Lower Matches**, not Ruled Out.

### 7. Find warm leads and harvest named contacts

Check whether former employers, organizations they've partnered with, or places they have relationships are hiring. **A former employer hiring for a role the person previously held beats every cold application on the list**, regardless of score. Flag these prominently and recommend direct contact over the application portal.

**Pull any human's name off every posting you read.** Job descriptions routinely carry a recruiter's name, a hiring manager's LinkedIn profile, a direct phone number, or an application email — and these are invisible in search snippets. LinkedIn's "Meet the hiring team" and "People you can reach out to" blocks also show 1st/2nd-degree connections and school alumni at the company. Put the contact in the tracker row.

**When a contact is named, tell them the specific move** — apply first, then message the recruiter referencing the application; or get the referral before applying when the contact is a 1st-degree connection inside the company. Referral notes work best short: a warm one-line opener, one line of context in plain language (no jargon), a soft ask ("would you mind pointing me to whoever's handling that hire?"), a light sign-off. Look the contact up first so the opener is accurate.

### 8. Verify pay when it isn't posted

Search public salary data (Indeed salary pages, Glassdoor, employer-provided ranges on other postings for the same role). Distinguish a *range* from a *flat rate*, and **base from OTE** — a "$160–180K OTE" figure may sit on a base under the person's floor. Label every estimate "est." and every unknown "Not posted"; never present an estimate as the posted pay.

## Output: the Job Search Tracker artifact

The deliverable is one persistent, published HTML page: **"<Name> — Job Search Tracker."** It is the system of record for the whole search. Build it with the Artifact tool once (load the artifact-design skill before the first build), then keep updating the **same URL** for the rest of the search. Never create a second tracker. If the person already has one (a pasted claude.ai/artifact link, or one published earlier), read it with the Artifact tool's `read` action and edit that one. A spreadsheet is an optional export, not the main output (see below).

### Layout

- Dark navy masthead with the title and a one-line subtitle computed from the data (counts of NEW, REACH, applied, interviewing, archived rows).
- A stat rail: Active, Pipeline, Lower Matches, Applied (this round), Ruled Out, Interviews.
- Pill tabs, each with a live count: **Active Targets · Already Applied · Pipeline · Lower Matches · Archive · Ruled Out.**
- Light and dark theme tokens; works at phone width.

### Data lives in JSON blocks

All content sits in `<script type="application/json">` blocks that the page's script reads and renders. These blocks are the single source of truth; never hand-write cards as HTML.

| Block id | Fields |
|---|---|
| `active-data` | company, title, location, pay, posted, found, tag, status (NEW / REACH), score, why, gap, resume, contact, url |
| `lowmatch-data` | same fields as `active-data` |
| `applied-data` | company, title, location, pay, tag, status (Applied / Interviewing / Offer / Rejected), applied_date, milestone, contact, found_via |
| `pipeline-data` | company, title, track, location, pay, verify, url |
| `ruledout-data` | company, title, location, pay, posted, found, blocker, url |
| `archive-data` | `{headers, rows}` for the prior search (email or job-board history) |

Rendering rules:

- **Active card**: company and title; score badge (85+ green, 70–84 amber, under 70 grey); tags for location, pay, track (`tag`, e.g. REVOPS, SOLUTIONS ENG, ENGINEERING, with a fallback color for unknown tags) and status (NEW gold, REACH blue); a "Posted · Found" line; a collapsible "Why it fits & what to watch" holding why, gap, and resume-to-use; the contact line; an "Open posting" button. Sort by score, highest first.
- **Lower Matches card**: identical to the Active card, rendered by the same function (give each list its own id prefix for the collapsible bodies). Sort by score, highest first. The notes box says these are open roles under the cutoff with no hard blocker, and when one moves (score revised to the threshold or higher → Active; posting closes → Ruled Out).
- **Applied card**: status pill (Interviewing green, Rejected red), applied date and source, a "Latest:" milestone box (next step, assignment, deadline, video link, link to the interview prep doc), contact. Compute the Applied notes box from the data (who is interviewing, who declined) rather than hard-coding names.
- **Pipeline row**: company, title, track and location, pay, and an amber "Verify:" line naming the one thing to confirm.
- **Ruled Out row**: company, pay, title, location, dates, a red blocker box, "View posting" link.
- **Archive**: a searchable, sortable table with filters by account and status, and a flag style for suspicious rows (recruiting-scam outreach that was never a real application).
- Each tab gets a short notes box. The Active note says what the search found or the board's current state; it must never name a role that has since moved tabs.

Links are full URLs taken from the tool results. If no real link exists, put a literal search string ("SEARCH LINKEDIN: <company> <title>") and say so; never invent one.

## Maintaining the tracker

**Everything found goes into the tracker the same turn.** Don't hold found roles in chat waiting for permission to add them; the person expects the record to be complete. Where each assessed role goes:

- At or above the threshold, open, no blocker → **Active**.
- Needs one check before it can be scored (pay unposted, status unclear) → **Pipeline**.
- Open, no hard blocker, but scores under the threshold → **Lower Matches**.
- Hard blocker or closed posting → **Ruled Out** with the specific reason.

**Status changes the person reports:**

- "Applied" (in words, or a confirmation screen or email) → move the row to Already Applied from whichever tab it sat on, with the date, a milestone, and the contact. A LinkedIn "apply now to your saved job" reminder is not an application.
- A posting showing "No longer / Not currently accepting applications" → Ruled Out with "Posting closed (checked <date>)", the match score, and the contact, so a repost is recognized.
- Interview steps (calls, screens, assignments, submissions) → status Interviewing, update the milestone with dates and links, and build the interview prep doc (see Interview prep).
- A completed interview (a pasted transcript, notes, or "how did it go?") → run the debrief (see After each interview) and update the milestone and contact fields with the next step, its date, and every named person.
- A reply you drafted for the person (to a recruiter, a scheduler, a hiring manager) is **not sent** until the person says it is. Record it on the card as "reply drafted, not sent" and change it only when they confirm or the next email or invite arrives.

**Thresholds the person sets** ("remove everything under 75") apply to Active and to every future addition. Open roles under the threshold move to Lower Matches; they are not deleted. An applied role is never moved or deleted for its score. If a threshold empties the Active tab, say so plainly and point to the best live Lower Matches.

**Triaging Pipeline** means pulling every posting: closed → Ruled Out; scores at or above threshold → Active; open and under threshold → Lower Matches; hard blocker → Ruled Out with the reason. Rule out without a pull only when the Pipeline note already names a hard blocker. Leave a dated note on the emptied Pipeline tab.

**Re-check Lower Matches** when the person wants more options: a revised score (new info on pay, a warm contact, a waived requirement) can promote a row to Active, and closed postings move to Ruled Out.

**Postings close fast**, often within two to four weeks. Re-check status before recommending an older row.

### Edit mechanics

1. **Get the current HTML.** Use the Artifact tool's `read` action; it saves the full page to a local file. The live version may have been edited from another session, so always start from a fresh read rather than an older local copy. Session workspaces reset, so if the local copy is missing, re-read rather than rebuild.
2. **Edit with a script that parses the JSON blocks**, changes the lists, and writes them back. Never hand-edit the long JSON lines, and never regex-replace JavaScript strings that may contain semicolons; replace note text by a unique literal substring (assert exactly one match) or by a quote-aware scan of the whole assignment. If an older tracker lacks a block or tab (for example `lowmatch-data`), add the block, tab button, panel, count, stat tile, and render call in the same edit.

```python
import re, json
def block(h, sid):
    m = re.search(r'(<script id="%s" type="application/json">)(.*?)(</script>)' % sid, h, re.S)
    return m, json.loads(m.group(2))
def put(h, sid, obj):
    m, _ = block(h, sid)
    return h[:m.start(2)] + json.dumps(obj, ensure_ascii=False) + h[m.end(2):]
```

3. **Validate before publishing**: every block passes `json.loads`; extract the main `<script>` and run `node --check`; dedupe rows by URL. For structural changes (a new tab), render the page headlessly and confirm tab counts and that the cards and toggles work.
4. **Strip the skeleton.** The published page includes a wrapper the Artifact tool adds. Republish only the authored content: `h[h.find('<title>'):h.rfind('</body></html>')]`.
5. **Publish to the same URL** (pass `file_path` and `url`; omit the favicon on republish).
6. **If the publish is refused because a newer version is live**, the refusal saves that version to a local file. Re-run the same edit script against that saved file (never resend your old copy, never rebuild from memory), strip the skeleton, validate, and publish again.
7. **Report in a line or two**: what moved where and the new tab counts. Don't re-describe the page.

## Optional: spreadsheet export

Only when the person asks for a file. Use `scripts/build_tracker.py`, building the workbook from a single source of truth in one pass. Do not insert rows into an existing spreadsheet — row insertion silently overwrites adjacent rows and desynchronizes the link column from the company column. After writing, verify the row count and that every link is non-empty and paired with its company. Gold = NEW, blue = REACH, grey = Applied, with a legend in the header.

## Standing resume versions

Most people with a varied background need **two or three standing resumes**, not one tailored per application. The role families that emerge from the search usually cluster into a small number of framings, and each cluster qualifies the person through a different door.

A real example: one person's search produced three clusters — HR operations roles (qualified by recruiting volume and HRIS systems), workforce development roles (qualified by a "three years of counseling or instruction" alternate path), and training roles (qualified by curriculum design). The same facts, ordered differently, with a different opening line. Sending the operations resume to a workforce development posting buried the exact experience the reviewer was checking for.

Build the versions once, then fill the **resume** field on every tracker row so each says which to send. Name them plainly — the person will be picking files under time pressure. A useful rule of thumb: "own and build the systems" → the engineering-first version; "client-facing, demo and design" → the solutions version; "run the revenue engine and the numbers" → the operations version.

**Do not resubmit a second version to a role they already applied to.** Two resumes for one candidate in one ATS reads as indecisive and can confuse a reviewer.

**Check the LinkedIn profile matches the resume they're now sending.** A recruiter who likes an application clicks the profile immediately. If the resume says one thing and the profile something else, that gap does real damage — and it's invisible to the person. Update the headline first; it's what shows in recruiter search results.

## Application forms

When the person pastes or screenshots application questions, answer each field in their voice. For numeric "years of X" fields, compute from dates in their documented record and show the basis. If the record can't support a number (for example, years on a specific platform before the earliest documented role), say what you can document and let the person supply the figure. Never round up to clear a stated minimum; if an honest number will likely trip a screen, say so and offer the direct-outreach route instead. "Why us?" answers: specific to the company's actual work, built from real numbers in the record, honest about the area the person is ramping on.

Never claim experience in the employer's own industry, product or platform unless it's in the record. Pasting a job description doesn't mean the person worked there, and a role in one sector isn't experience in another. If the person says an answer is wrong, drop the claim entirely rather than rewording it. Follow the default answer format and the other rules in `references/applications.md`.

## Interview prep

**Whenever an interview or recruiter screen is scheduled, build the prep doc automatically**; don't wait to be asked. Make it a living doc (Claude Docs when available), link it from the Applied card's milestone, and build it to the standard below.

### The prep doc standard

Every prep doc carries the same sections, in this order. People compare one prep doc with the last one they used, and a section that was there before and is missing now reads as a mistake ("you're missing info included in the previous prep"). **Start each new doc from the section list of the most recent prior prep doc and never drop a section it had.** If the person adds a section to one doc, it becomes part of the standard for every doc after it.

1. **Debrief** (later rounds only): a dated debrief of the previous round at the top. See After each interview.
2. **Call snapshot**: a table with role, posted pay (base, bonus, equity, OTE), location and in-office rules, the interviewer's name and title, the applied date and which resume was sent, and the date, time, format and link or address. Add any clash that week (another interview the same day). Then one line on what this interviewer is checking.
3. **About the company**: what it sells, who buys, the business model, named customers, leadership, funding, recent news and stack signals (a HubSpot meetings link, the forms on its site). Put any multi-product or multi-motion split in a small table. End with one line on why it matters for this person. Cite every fact.
4. **Original job**: the link, pay and benefits, then a close paraphrase of every responsibility, requirement and nice-to-have, with the posting's own key phrases in quotes. The posting will close, so this is the person's only copy.
5. **Original application**: a table of every field the person submitted: resume version, years-of-experience answers, salary entered, and the written answers. Add "things to be ready for" wherever a submitted answer differs from the record. If the exact text isn't available, say so, list the questions, and name the strongest story for each.
6. **Where this role overlaps existing jobs**: a drawn diagram, never a list. The role sits in the center and each job it folds in is a box around it, showing what that job does, the person's evidence, and a fit marker (strong, partial or gap, in status colors). Under it, one sentence on the gap and how to lead around it. Include it in every prep doc. For a later round, copy the earlier doc's diagram rather than leaving it out. The diagram also feeds two questions (which parts already have an owner, and is this one builder or the first hire of a team) and the pay argument in section 13.
7. **Fit and gaps**: a table of requirement, evidence and fit (strong, meets, partial, gap), then how to frame the gaps in the person's own words.
8. **Intro in three lengths**: a 60 to 90 second intro, a 20-second version, and "background in two sentences". When the person supplies their own intro, keep their voice and structure, tie it to the posting's top asks, and put their strongest numbers in it.
9. **Proof points**: a table of the posting's own phrase or KPI, the person's number, and where it happened.
10. **20 role questions**, each with an answer in the person's voice built only from their real record. Follow them with a **Gap to handle honestly** note: the one weakness they should name first.
11. **20 interviewer-side questions**, based on the interviewer's LinkedIn profile, with answers. Look the interviewer up by name first (the posting or the scheduling email usually names them); someone who built training programs probes differently than someone who came up through sales. If the profile can't be found, say so in the doc and base the questions on the interviewer's title, never an invented background. When the person later supplies the profile (a LinkedIn PDF export or a screenshot), rebuild this section the same turn: open it with a "From their profile | What it means for you" table (current role and tenure, prior companies and what those businesses do, recruiting or technical depth, how long they stayed places, listed skills), then rewrite the 20 questions to that background and suggest a rapport opener drawn from it. Update the interviewer's line in the call snapshot too.
12. **My 3 questions**, each with why to ask it and what a good answer sounds like. Then **Additional questions** numbered from 4, for later rounds. Fold in any questions the person adds.
13. **What this role should pay**: lead with a recommended base range in one sentence, then:
    - A benchmark table (title, base, source with date) built from pages actually opened, never search snippets.
    - The jobs from the overlap diagram priced one by one with sources, and what they would cost combined.
    - How to use this: employers pay one person at the level of the hardest part, plus a premium for range, not the sum of the jobs.
    - A short negotiation script and the person's floor.
    - When no pay is posted, label every figure an estimate.
14. **Logistics and guardrails**:
    - The salary already entered on the application, and whether to hold it.
    - A **Don't claim** list: credentials not held, tools only trialed, projects never launched, the employer's own industry.
    - A **Say exactly** list of numbers that must match the resume.
    - A **Check before the call** list: LinkedIn headline against the resume sent, which name to use, and that public portfolio or GitHub items don't expose another employer's interview assignment or client data.
    - Bracketed items only the person can answer.
15. **Before and after**: a task list (accept the invite, research the interviewer, reread the application answers), then a thank-you note draft with the person's full name and contact info in the signature.
16. **Sources**: every page opened, with dates.

**Onsite, final and hiring-manager rounds add:**
- A **corrections table**: what the person said earlier, what the record shows, and what to say now.
- An interviewer research table with sources, plus the interviewer's public talks or podcasts and the time stamps worth hearing.
- A drawn 30/60/90 plan with a checkpoint for each phase.
- Logistics: the address, when to leave, and what to bring (printed resumes, a one-page plan, work samples).

Use plain language when the interviewer isn't technical. For a short interview, say a 15-minute screen, mark the four or five questions most likely to actually come up. Mark anything only the person can confirm with a bracketed note ([confirm: ...]) rather than guessing. If the company bans AI help during live interviews, say so in the call snapshot: read the doc beforehand, keep it closed during the call. Log every interview step and take-home assignment on the Applied card's milestone.

Add answers to the questions that come up in almost every process, written to respect the don't-mention list: "Why are you leaving?" (honest, without what they keep private), "Are you interviewing elsewhere?", a weakness, and any requirement they don't meet. For scenario questions, give a short story with the key numbers itemized as bullets.

**Find the people.** Postings often name the hiring manager by title only ("reports to our Chief Business Officer"). Check the company's leadership or about page, which often links LinkedIn profiles, then confirm on LinkedIn. To see who already owns adjacent work, run LinkedIn people searches filtered to the company's numeric URN (from its company profile) with short keywords ("lifecycle", "marketing", "operations", "revenue operations"). The company people page's keyword filter does not filter reliably, so don't rely on it. Report only the first page of results as checked, and say so. Ashby, Greenhouse and Lever boards expose public JSON APIs (for example `api.ashbyhq.com/posting-api/job-board/<board>`) that return the full posting when the careers page renders only with JavaScript.

**Verify experience claims before writing them into answers.** When the person says they have used a tool or done a kind of work that is not in their resume, search their connected mailboxes and drive (all accounts they name) for welcome, trial, receipt, invoice, cancellation, and support emails, and for screenshots or working docs. Label each finding plainly: paid plan, trial only, used in production, studied, or not found. A free trial or a newsletter is not production use. Write the doc to the evidence, mark the rest for confirmation, and tell the person kindly where their memory and the records differ. If the search finds nothing, say so and note the tool may have lived on a work account the connectors can't see. Then write the claim exactly at the level the person stated it ("Coupler.io pipelines into Looker Studio" is pipeline and BI work, not warehouse work) and ask the one question that would raise it ("did any flow load into BigQuery or Snowflake?"). Update every place the doc touched the old claim: the don't-claim list, the fit table, the overlap diagram's fit marker, and any scripted answer. Also catch anything sensitive found along the way, such as plaintext passwords in a shared sheet, and recommend rotating them without repeating them.

### Recruiter messages before the interview

When the person pastes a recruiter email (scheduling link, a request for a recorded video intro, a salary question), draft the reply. Include the salary range from the standing record when asked. If the person doesn't do pre-recorded interviews, say so politely and offer a live call. For a video-intro request they accept, write a 2–3 minute script that answers exactly the prompts given.

### After each interview

**Recommend recording with Granola.** Granola is an AI notepad that transcribes calls from the computer's own audio, so no bot joins the meeting. Its Claude connector (`list_meetings`, `get_meeting_transcript`, `query_granola`) lets you read the transcript directly. When an interview is booked, suggest the person set it up before the call. Mention consent: recording and transcription rules vary by state and country, and some require everyone on the call to agree, so the person should tell the interviewer they're taking notes with a transcription tool. If the company says it records interviews with its own AI notetaker, note that in the prep doc.

**After the call, pull the transcript from Granola** (or use a pasted transcript, notes or a recording summary), then do all of this in the same turn:

1. **Add a dated debrief at the top of the prep doc** with: outcome; the next steps with names and dates as stated; what was learned (why they are hiring, the first focus, the hardest problem, team structure, growth plans, comp signals); the questions actually asked, what the person answered, and a stronger answer for each; fixes before the next round; and what to prepare next.
2. **Fixes worth flagging**:
   - Answers that wandered before reaching the strongest example. Lead with the most recent, numbered result.
   - Claims that go beyond the evidence, or conflict with the resume they sent. Offer the exact wording to use instead.
   - Anything on the don't-mention list.
   - Stories framed in a way that could hurt ("gray hat" methods, "I applied to test my tool").
   - Credentials cited that should be current and on the resume.
   - Comp handling. If the person disclosed current pay or called the top of the range their floor, coach them to state a target next time (top of the base range plus bonus and equity) rather than current pay. If they gave two numbers on one call, or the call and their portfolio or application disagree, flag it first: recommend one target with its basis (posted range, whether there's a bonus, benchmarks, any signal the recruiter will go above range), and leave the final number to them.
   - **Claims made on the call that aren't in the record** (direct reports, a compliance domain, a tool, a team size). Mark each [confirm]. If true, offer to add it to the resumes before the next round; if not, give the exact correction to make next time.
   - **Numbers that differ across processes.** Compare every figure said on the call (budgets, attendance, revenue, team size, ranks) against the record and against what the person told other companies, using earlier debriefs and prep docs. One metric stated three ways to three employers is a reference-check risk. Name the figure to standardize on.
   - Name slips or likely transcription errors on company and employer names, so the person says them clearly next time.
   - **New proof points that surfaced** (a process cut from hours to minutes, a fast rebuild). List them and offer to add them to the resumes and the next prep doc.
3. **Prepare the next round**: build the next prep doc to the full standard, including the overlap diagram and the pay section. Lay out the process the recruiter described as a table (step, who, format) with the expected decision date. Check the likely dates for the next round against the person's other scheduled interviews and work constraints, and flag any clash. Look up the named next interviewers and current team members in the role. Draft answers for the problem the interviewer said is hardest, and outline a 30/60/90 plan in the interviewer's own framing. Get ready for any take-home or presentation they described, and for any promise the person made to follow up.
4. **Update the tracker**: milestone (screen done, next step and date, key intel, link to the doc) and contact (recruiter, hiring manager by name, next interviewers).
5. **Draft a thank-you note to send the same day**: formal and short. Address the interviewer by name and cite one or two specific points from the conversation. Include one useful ask (for example, the name of a next-round interviewer) and the person's full name and contact info in the signature. It's also the place to correct anything misstated on the call; when comp came out muddled, offer an optional one-line restatement of the single target, marked as optional and the person's decision. Show it in chat first, then offer to save it as a draft in their email, asking which address to send from.

### Offer, negotiation and withdrawal

- **Unposted pay:** give a market range with its basis (title, level, location, comparable postings). Label it as an estimate.
- **Counteroffer:** build the case from the actual scope discussed in interviews. If the job grew past its title, or overlaps a more senior posting, name that with the numbers. Draft talking points for a live conversation as well as the email.
- **Employment type:** when W-2, 1099 or C2C is on the table, lay out the real difference (taxes, benefits, stability) before recommending a counter.
- **Withdrawal:** if scope and pay don't match, draft a short, gracious withdrawal that states the mismatch factually and leaves the door open.
- Record offers, counters and outcomes on the Applied card (status **Offer**, or **Rejected** with the reason if known).

## Closing analysis

End by telling them what the search revealed, not just what it found:

- **What's actually gating the search** — a credential? geography? a title mismatch? Name it.
- **Which capability opens the most doors** — usually one credential or skill unlocks a disproportionate share of the matches.
- **What would unlock the most additional roles** — finishing a degree, a reciprocity check, a short certification, willingness to relocate.
- **Where the ceiling really is.** If the direct-service roles cap at $25/hr but the commercial side of the same industry pays $70K+, say so. People often don't know an adjacent track exists.

## Ground rules

**Never invent facts about someone's background.** If a number, credential, or date isn't in what they gave you, ask or leave it out. A fabricated detail on a resume, a form, or in a match rationale can end a candidacy in a reference check.

**Never invent a job listing, and never invent a link.** If a tool returns only a page title, or a fetch comes back empty, say so. Do not fill the gap with plausible company names, pay ranges, or URLs — they will be acted on.

**Don't pad to hit a requested count.** If the person asks for N roles above a pay floor and a score floor, deliver what genuinely clears both, then a clearly labeled "close" tier (pay unposted, OTE only, or one negotiation away), and name the lever that would open more (a lower floor, counting OTE, including unposted pay). Ask which rule to use before searching further.

**Say when a channel is producing noise.** If LinkedIn returns only promoted ads, report that rather than padding the list with irrelevant roles.

**Report saturation honestly.** When additional searches stop producing new matches, say so and pivot to higher-value actions — outreach, resume tailoring, credential questions — rather than performing more searching.

**Don't overstate a finding.** If one posting has an unusual qualification path, verify before claiming it's a company-wide pattern.

**Correct your own statements when new evidence arrives.** If a later search contradicts something already said or written in a doc ("no evidence of X"), say so plainly and fix the doc the same turn.

**Never send on the person's behalf without a clear yes.** Drafting a reply is not sending it. Don't send, schedule, or create email drafts unless asked, and never describe a draft as sent.

## Related work

Once matches exist, the natural next steps are tailoring a resume to a specific posting, answering the application's own questions, and preparing for interviews.

- `references/tailoring.md` — adapting a resume to a job description and passing ATS screening.
- `references/applications.md` — screening questions, "why this company," salary-expectation fields, and postings that require a short written response.