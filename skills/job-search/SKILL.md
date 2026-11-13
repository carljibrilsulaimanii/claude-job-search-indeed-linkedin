---
name: "job-search"
description: "Run a complete job search for one person. Intake their background and standing rules, save every correction as a rule, search by capability on local and remote axes, score roles, keep one tracker (Active, Pipeline, Applied, Lower Matches, Ruled Out), apply with safety rules, check all mail for responses, report updates, prep and debrief interviews, and find patterns in interviews versus rejections, proposing a rule for each and asking before adopting it. Use for \"find me jobs\", \"sweep\", \"updates?\", \"check email\", \"apply\", \"is this a good fit\", interview prep, debriefs, thank-you notes, offers, and tracker changes."
---

# Job search

## 0. Before searching: check the tools and the LinkedIn version
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

## 1. Intake and standing rules (first session, then keep current)
Ask for, then save as the person's standing record:
- Resume(s). If they keep more than one version, give each a short tag (for example HR, TRAINING, OPS) and record which file each tag means. One version per cluster of roles: same facts, different order and opening line.
- Master history: every job with exact title, employer and dates; every certification (earned or pending); education exactly as completed (coursework is not a degree).
- Target tracks: 2-6 kinds of work, in their words.
- Locations: home metro, commute limit, remote yes/no, hybrid yes/no, relocation yes/no.
- Pay floor (or "none"), pay type (hourly or salary), and whether the floor means base pay or total pay.
- Hard limits: things they will not do (night shifts, travel, commission-only, specific application systems).
- Known blockers: degree, licenses, languages, years of experience.
- Total years of relevant experience, counted across job titles (for example 2 years as a recruiter plus 5 years hiring as a manager = 7 years of hiring).
- Don't-mention list: things they don't want raised (a past business, why they left a job).
- Format preferences: signature block, portfolio link to always include, punctuation or tone they dislike.
Never invent a fact about the person. Anything not in their resume or answers, ask.
Check that their LinkedIn headline matches the resume version they are sending; recruiters click the profile first.

### Past applications
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

### Rules to ask about
Ask these as a short checklist (offer the default in brackets so they can answer "defaults"). Save every answer as a standing rule with the date.
Applying:
- Who clicks the final Submit: you (Mode A), or Claude (Mode B)? See section 7a. [you]
- Should Claude start the next application without asking each time? [ask first]
- Standing answers for common screening questions. Ask each one once and save it: criminal history (felony and misdemeanor separately); ever fired, discharged or asked to resign; terminated in the last 5 years; ever accused of unethical conduct, dishonesty or disrespect; any time your integrity or honesty was questioned (free text); ever worked under another name; relatives at the employer; worked for this employer or its affiliates before; non-compete; earliest start date; jobs held in the last 18 months; willing to relocate; drug screen and background check OK. [ask each]
- Veteran status wording: forms offer both "I did not serve in the military" and "veteran, not protected". Which is true for you? [ask]
- If a required self-ID question has no "decline" option, what should Claude pick? [ask]
- May Claude use "Sign in with Google" (or similar) where offered, instead of emailed codes? [ask]
- Tick required consent boxes (terms, privacy, background check) for you? [ask first]
- Attach resumes and fill target-compensation fields yourself, or hand them to you? [Claude does both]
- Text/SMS opt-ins from employers: yes or no? [no]
- Optional marketing and cookie consents? [decline]
- Voluntary self-ID (gender, race, ethnicity, veteran, disability): your answers, or decline? [decline]
- Salary ask: top half of the range, a fixed number, or "negotiable"? [top half]
- Fields you can't fill (reason for leaving, salary history, "may we contact", old employer phones, references): what goes there? Never make these up. [ask each time]
- Fix fields an application system prefilled from an old profile? [yes, and tell you what changed]
- Which sign-in to use where offered (for example "Sign in with Google")? [ask]
- Any application systems to skip (ones where sign-in has failed before)? [none]
- Applications that ban AI help: some forms make you certify that no AI was used beyond your resume. Claude will not fill any part of those; you do them yourself (section 7j). [fixed; not a choice]
Searching:
- Roles to rule out on sight (commission-only, night shift, travel over X%, specific industries)?
- Will you apply where a degree or language is "preferred" but not required? [yes]
- Score cutoff for Active? [65]
- Estimate pay when a posting has none? [yes, marked Est.]
Communication:
- May Claude draft replies to recruiters? Sending always needs your OK. [draft only]
- Thank-you notes: may they include a question (for example, who the next interviewer is)? [ask]
- List rejections in reports, or only log them in the tracker? [list them]
- When an application emails a login code, should Claude find it and show it to you? [yes, if email access exists]
- Close browser tabs when an application is done? [yes]
- How should updates be delivered: short list, or full detail? [short list]

### Capturing new rules
- Any time the person corrects Claude ("don't do X", "always Y", "skip Z", "why do you keep...") or answers a one-off question that will come up again, treat it as a standing rule.
- Restate it in one line, save it with the date, and confirm: "Saved rule: always pick Sign in with Google on ADP."
- If a new rule conflicts with an older one, the newer one wins; say which rule it replaces.
- Check rules against each other, not just against the newest one. Two saved rules can produce contradicting answers on one form (for example "answer Yes to a required Hispanic question with no decline option" versus "not Hispanic" everywhere else). Point out the conflict and ask which is meant before the next application uses it.
- Read the full saved rule before acting on it. One-line summaries of rules (an index, a recap) go stale; when a summary and the full rule disagree, the full rule wins, and fix the summary.
- Before each session's work, re-read the rules. Never stretch a rule beyond what it says (permission to tick a consent box is not permission to send a message).

## 2. Search by capability, not just title
- List what the person actually does as short phrases (for example "job placement", "new hire onboarding", "high-volume hiring", "facilitating training", "client intake"). Then list 4-8 job titles for each capability. The same work hides under many titles.
- When the person points at a role they like, search its shape (function, setting, tools, client-facing or not), not its title.
- Run every term on BOTH axes: the home metro, and remote nationwide. A metro-filtered search can never return a remote role, so never call a market thin until both axes ran.
- Channels: LinkedIn works best with 2-3 word queries (long queries return ads; check the "Showing results for" line for silent corrections; if name searches fail, open known postings by job ID). Indeed: longer, varied phrasing finds different postings. Job-alert emails are a free extra channel. Web search finds company career pages and sibling roles posted only there.
- At the start of a session, check which job-board tools are connected. If one is missing, say so and use web search for that channel. Tools that run on the person's own computer (desktop extensions) only work in a live chat while that computer is linked; a scheduled cloud run can't reach them, so it should report that channel as offline, not skip it silently.
- Pull the full posting before scoring; snippets omit the requirements. Check the status line: "no longer accepting applications" means closed.
- Verify a posting is open at the source, not only on a job board. Many application systems publish their open roles as JSON: Greenhouse (boards-api.greenhouse.io/v1/boards/<company>/jobs), Ashby (api.ashbyhq.com/posting-api/job-board/<company>), Lever (api.lever.co/v0/postings/<company>?mode=json). A role missing from that list is closed even if a board or aggregator still shows it, and the same list shows sibling roles worth a look. Search Indeed by the employer's legal name too ("Acme Data, LLC"); a short-name search can make a live role look closed.
- Copy every named person off a posting (recruiter, hiring manager, phone, email) into the tracker row, and name the move: apply then message the recruiter, or ask a contact inside for a referral first.
- Exhaust the tracker before any new sweep. Every Active row must be applied to, verified closed (moved to Ruled Out with the date checked), or blocked on a named action by the person. Never leave a row as "likely closed"; check it the same session. Before working a list (Active or Lower Matches), remove rows that repeat an Applied row (same company and title).
- Run a sweep in four passes before reporting:
  1. Proven terms (ones that produced interviews or high scores), both axes, last 1-2 weeks.
  2. New title variants and adjacent wording, both axes, wider date range.
  3. Employer-direct: when 3+ top scores come from one kind of employer, list employers of that kind nearby and search each by name.
  4. Warm threads: reposted roles, employers with an open conversation, adjacent roles at places they applied.
- Say which passes and phrases ran. Never pad to a requested count; report how many truly fit and what would open more.
- When asked about commute or distance for a specific role, answer with miles and rush-hour drive time from the person's home, plus any extra driving the job itself requires; let the person decide, then record the decision.

## 3. Score and screen
- Score 0-100 for fit against the real background. Default cutoff: 65 for Active; below that goes to Lower Matches. A low score is not a blocker.
- Status: NEW (meets requirements) or REACH (meets all but one; pursue by direct outreach to a named contact, not a cold application).
- For each role record: company, title, location (with commute time), pay, score, resume tag, why it fits, what to watch, contact, stable link.
- Pay is never blank. If not posted: "Est. $X-$Y (not posted; based on ...)". Never let an estimate look like the employer's number. Separate base from bonus or OTE; an OTE figure can sit on a base under the floor.
- Read requirements closely: "or equivalent experience" and "credential in lieu of degree" open roles that look blocked; "preferred" is not "required"; requirements differ posting by posting, even inside one company; when a listing's labels (level, city) disagree with its body, trust the body.
- Rule out, with the reason recorded: a hard degree requirement with no equivalency; required language or license the person lacks; an on-site city out of range; pay under the floor; contract when they want full-time; remote roles limited to other time zones; application systems the person asked to avoid; closed postings.
- When a role scores high, check the same employer for other locations and levels.
- Flag likely resume harvesters: one company name across many unrelated generic remote postings with no real company page.
- Aggregators and recruiters (Jobgether, Ladders, Haystack, talent marketplaces, staffing firms) repost employers' roles without the employer's name, and the same job can show up under the aggregator and under the employer. Before applying through one, compare the duties, pay, team size and tools with roles already applied to directly. A match means the same job: rule the repost out as a duplicate, with the reason. After applying through an aggregator, find the real employer (the aggregator's application history or the confirmation email usually names it) and put it on the card.
- Note on the card when an application form bans AI help (section 7j), so the person knows it is theirs to fill.

## 4. The tracker
- Keep exactly ONE tracker per person (a published artifact page). Before creating any page, list existing ones and update the match. Never make a second tracker.
- Tabs: Active (to apply), Pipeline (promising but needs one check first), Applied (date, status, latest step, contact), Lower Matches, Ruled Out (with blocker). Optional: Archive for an earlier search's history.
- Keep the data in JSON blocks inside the page that a script renders. Never hand-write cards.
- Store links that stay valid: for Indeed use indeed.com/jobs?q=title+company&l=location, never to.indeed.com short links (they rotate to other jobs).
- Optional: an "Applied" checkbox on each card that writes to the page's database, so the person can mark applications themselves. At the start of every tracker session, read those ticks and move ticked roles to Applied with their dates.
- Status changes: "applied" moves the row to Applied; a closed posting moves to Ruled Out with the date checked; interview steps set Interviewing with dates, links and the prep doc; a reply Claude drafted is "drafted, not sent" until the person confirms.
- Blocked applications stay in Active with a dated "NEEDS YOU:" note at the front of the card (what is needed, which tab, what was tried). Replace the note when the block clears; don't stack stale ones.
- A score threshold the person sets applies to future finds too. An applied role is never moved or deleted for its score.
- Write every find into the tracker in the same turn it is found. A find that isn't recorded can be lost.
- Correct the tracker when evidence changes, the same turn. A submission the person reported that doesn't appear in the site's application history goes back to Active as "NEEDS YOU". A role found to duplicate an earlier application is merged into that row with a note, not counted twice. A submission an aggregator reports as failed (for example "position closed") moves to Ruled Out and comes off the applied count.
- Counts: when the page splits applications between "this round" and an Archive, show the all-time total next to the round count and say where older rows live. A smaller number at the top otherwise reads as lost applications. When asked "where did the rest go?", count by tab and month and show the table.

### Tracker layout and data blocks
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

## 5. Editing the tracker safely
- Always read the live page first and build on that version. Never republish an older local copy; another chat or a scheduled run may have changed it.
- Edit with a small script that parses the JSON blocks, changes the lists and writes them back. Then check every block parses and the page script passes a syntax check.
- If a publish is refused because a newer version is live, re-run the same edit script on the newer version it hands back. Never resend the old copy.
- If several chats work on one search, name one as the owner. Others tell the owner before publishing and when done. When a chat adds rows, it tells the others so their next publish builds on the new version instead of wiping the rows.
- Approvals don't travel between chats. If the person says "yes, apply" in one chat and another chat is doing the applying, the applying chat asks the person directly and waits; it never acts on a relayed yes. Only one chat applies to a given role, so nothing is sent twice.
- On Windows PowerShell 5.1, never serialize rows with ConvertTo-Json: it can wrap arrays as {"value":[...],"Count":N} and blank the page. Search the file for "Count": before publishing.
- Keep the page's declared capabilities (such as its database) when republishing.

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

## 6. Email checks
- Read-only access to the job email is enough. Never change the mailbox (labels, archive, read state, delete) unless asked.
- Check which account each connected tool is signed into before using it. An email connector signed into someone else's mailbox will put drafts in the wrong place; use only the person's own account.
- When the connected email or calendar tool reaches a different account (a work mailbox, a business inbox), set up a separate connection to the job-search account and use only that for job mail, one-time codes and interview scheduling. A small OAuth script against the Gmail and Calendar APIs is enough; keep its token file private. Save which account each tool reaches as a standing rule and never mix them.
- Run this check first in any sweep or batch of applications, not just when asked for updates. Compare calendar invites with interviews already in the tracker and raise any clash (two interviews at one time, a date that doesn't match its weekday) right away.
- Search ALL mail, not just the inbox. Many people filter application mail out of the inbox on purpose, so an inbox-only check misses rejections and invites. Run three kinds of query: application-system senders (Greenhouse, Lever, Ashby, Workday, iCIMS, SmartRecruiters, Workable, Rippling, BambooHR, SuccessFactors/jobs2web), wording (application, interview, next steps, schedule, assessment, unfortunately, not moving forward), and the names or domains of live contacts.
- Read the whole thread before acting on it. When something was filtered out of the inbox, say "not in your inbox" so the person knows where to find it.
- Skip job alerts, newsletters and marketing for status (but job alerts are a search channel). Some applications quietly join a "talent community" that then sends weekly job alerts; treat those as alerts, not replies.
- Update the tracker: rejection = "Not selected (email date)"; invite = status plus date, time, format and contact; confirmation = Applied. A "we received your application" email is proof the submission landed; note it on the card.
- When an application emails a one-time code, find it and show it to the person right away, saying which application it is for.
- Track promised invites: when an interview was agreed but the calendar invite hasn't arrived by the day before, say so in every update until it does.
- An email check includes the calendar. List interview invites that are still unbooked (self-schedule links such as Calendly or an application system's availability page) in every update until a time is booked. Never book, accept or reschedule a slot for the person.

## 7. Applying
### 7a. Submit modes (set at intake, saved as a rule)
Pick ONE mode with the person and write it down with the date. Re-read it before every batch. A later rule replaces an earlier one; never mix modes.
- Mode A, person submits (default): Claude fills every page, stops on the review page or the last question step, and hands over with: the tab, the role, what was entered, anything that needs a look. The person clicks Submit and says "done"; only then does the row move to Applied.
- Mode B, Claude submits: Claude fills, runs the pre-submit check (7e), clicks the final Submit, and confirms the result (7f). This covers self-ID and attestation pages too, using the person's saved answers. It does NOT cover the hand-off items in 7c or forms that ban AI help (7j).
  Some environments stop Claude from ticking consent or attestation boxes even under Mode B (a safety check on "consent given for the user"). When that happens, don't look for a workaround: finish every other field, leave the tab on that page, and add the boxes to the hand-off list with the tab name.
- Batch mode: if the person says "don't ask, just keep going" or "apply to several at once", open the next highest-scoring Active roles in parallel tabs (3-4 at a time) and keep filling the others whenever one is blocked on the person (a code, a missing fact). Collect every hand-off into one list (tab, role, what's needed) instead of stopping per tab. Report results at the end; don't stop to ask "start the next one?". Still stop for any new fact or hand-off item.
- Modes can change mid-session ("no, you click submit"): save the new mode as a dated rule that replaces the old one, say so in one line, and apply it to tabs already open.
- Whatever the mode: a button labeled Submit, Apply, Send or Finish on an intermediate step can send the whole application (iCIMS is the known case: when no later step has questions, a step's Submit is final). In Mode A treat every such button as final and hand over before it.

### 7b. Before starting an application
1. Run the email check (section 6) if it hasn't run today: a rejection, an interview invite or a calendar clash may change what to apply to.
2. Search the tracker for the employer. If the person already applied there, say so and why this is a different role before going ahead. Some hiring chatbots allow only one open application per person; rule out the second role if so.
3. Confirm the posting is still open and the apply link doesn't route to a system on the person's skip list.
4. Pick the resume version that matches the tracker tag; check the application system didn't default to a different saved resume.
5. Read the whole form before typing anything. If it asks the applicant to certify that no AI was used, stop and follow 7j. Note any scored quiz, human check, or question that needs a new fact, so the person hears about all of them at once.

### 7c. Hand-off items (always the person's, in every mode)
Passwords, creating accounts, one-time codes typed into sign-in or verification boxes, CAPTCHAs, "Human Check" boxes and other bot checks, SSN or government ID, date of birth, driver's license numbers, bank or tax details, tax-credit (WOTC) questionnaires, and any browser safety block on a click. Fill everything up to that point, leave the tab open, and say exactly what's needed and in which tab. If email access exists, fetch a one-time code the moment it's sent and show it in chat (bold, with which tab it belongs to); keep working on other applications while the person enters it. If a "Sign in with Google" (or similar) button is offered and the person approved it, use it instead of an emailed code; any password or 2-step prompt is still theirs. Some systems create a candidate account automatically after an email step with no password set; note it in the tracker so the person can set a password later.
Some systems email a security code only after the first Submit (Greenhouse does): fetch the newest code for that employer and show it; if the form was submitted again, an older code is stale.
When an employer's system (Workday is the usual one) needs the person's own sign-in, leave the tab on the sign-in page, mark the card "NEEDS YOU: sign in", and carry on from where it stopped the moment they say "signed in". Optional ID fields (date of birth, SSN, license) stay blank even when the form shows them.

### 7d. Filling the form
- Facts only from the resume, the master history, the intake, or the person's earlier answers. A question that needs a new fact (criminal history, a license, a reference, a reason for leaving) means stop and ask; save the answer as a standing answer for next time.
- Screening questions with no saved answer (integrity questioned, accused of unethical conduct, terminated, worked under other names): ask before submitting. Don't infer one from a similar saved answer, even an obvious-looking one. If an answer slipped through without a saved basis, tell the person right away exactly what was entered and offer to note a correction.
- Prefilled fields: check every one. Systems reuse old profile data (an old address, a past job shown as current, a guessed graduation date, a stale salary, a start date that has already passed, a yes/no eligibility answer such as "past government employee" that isn't in the record). Fix it and list what changed; ask when the record can't settle it. Clear prefilled number fields before typing; typing into "58000" can produce "58000.028".
- A saved candidate profile at the employer can carry details that aren't in the record (an apartment number, an old phone). Don't silently accept them: flag them in the report so the person can confirm.
- Resume autofill: after uploading, check every parsed job and education row against the record. Delete duplicates and blank rows, fix titles and dates, and fill required per-row fields the parser left empty (employment type, country, state).
- Long forms: list every field with its label first (a short page script works), fill in groups, then check for empty required fields before Submit. After Submit, read the page: "please correct the errors" means it did not go through; fix each flagged field (a numbers-only salary field rejects text like "$48,000/year") and submit again.
- Attaching the resume is Claude's job, not a hand-off. When an upload area has no file input on the page (clicking it opens the computer's file picker, which Claude can't drive; Airtable forms are the known case), add a temporary file input to the page, load the resume into it with the file-upload tool, then dispatch a scripted drag-and-drop of that file onto the upload area (dragenter, dragover, drop). Confirm the file name shows before Submit, and remove the temporary input.
- Long answers: on sites where typing drops letters (LinkedIn Easy Apply is the known case), set the text with a form-fill call, then nudge the field (click, End, space, Backspace) so the page registers it. Proofread the review page.
- "Years of X": compute from documented dates and show the basis. Never round up to clear a minimum.
- Salary: follow the saved rule (default: top half of the posted or estimated range). Numbers-only fields get a plain number; match the pay type (hourly vs annual). When pay is a dropdown in fixed steps and the target falls between two, read the field's help text: if the system caps the figure at the top of the posted range, pick the step at or above the target and tell the person what employers will actually see; otherwise ask which step to use.
- "Target compensation", "desired salary" and "salary expectations" fields, free text or number, are filled from the saved salary rule. Don't hand them to the person.
- Required consent boxes (terms, privacy, background check, "information is accurate" certification): tick only if the person approved this at intake, and only when every answer on the form is true. Text/SMS opt-ins and optional marketing or cookie consents: follow the saved rule (default: decline).
- Voluntary self-ID: use the person's saved answers or "decline to answer". When a required question has no decline option, use the person's saved answer for that case; if none is saved, ask. Save Hispanic/Latino as its own answer, since many forms ask it separately from race. When a form has no "Two or More Races" option and lets you tick several boxes, tick the person's specific boxes (save them once) instead. Veteran questions: use the saved wording ("did not serve" and "veteran, not protected" are different answers).
- Fields with no honest answer (old employer phone, salary history, references): use the person's saved placeholder ("N/A", "Upon request"). Never invent employers, dates, phone numbers, addresses or references. Note placeholders in the tracker so the person has real answers ready if asked.
- Employment type and similar per-job dropdowns: pick the closest honest category (salaried or corporate for professional roles, hourly for hourly ones) and record the choices on the card.
- Cover letters: write one only if asked or required; check none was prefilled from an earlier application to another company.
- Follow-company, job-alert and "save my answers" boxes: leave unticked unless the person wants them.

### 7e. Pre-submit check (Mode B, or before handing over in Mode A)
On the review page, confirm: right resume attached; name, email, phone and address current; no prefilled stale job or date; every answer reads correctly (no dropped letters); dropdowns show the value intended (on some systems a click lands on the neighbouring option, for example an "18 or older" answer set to No); salary matches the rule; consents and self-ID match the saved answers; nothing claimed that isn't in the record. If anything is off, fix it before Submit.

### 7f. After Submit
- Confirm the result on screen ("application submitted", a confirmation number, or the candidate home status). No confirmation means not applied: say so and leave the tab open. If the confirmation names a different role or company than the one filled in, record the application with that mismatch on the card and ask the person to check the site's application history.
- A tab that froze or stopped responding can recover later. Check it again before calling the application failed, and finish it if the form is intact.
- Record it in the tracker the same turn: date, channel and system, resume version, key answers (salary, years, consents, placeholders), confirmation text, and who submitted.
- When the person submits one themselves (for example by pasting the confirmation text), record it as "submitted by the person" with the date and confirmation, and note that Claude did not see their answers.
- Watch for the confirmation email in the next email check; a same-day rejection is information about an automatic screen.
- Close finished tabs one at a time, and check the tab group still exists after each close. Closing tabs can make the browser drop the whole group, and a group left holding only a blank new tab can vanish too. Prefer reusing a finished tab: navigate it to the next application instead of closing it. If the group disappears, open a new one at once and tell the person so they can drag their open tabs back in. Never close a tab that isn't confirmed submitted, and keep tabs that are waiting on the person.

### 7g. Never, in any mode, without the person's explicit yes
Send email or messages, reply to a recruiter, accept or reschedule an interview, accept or decline an offer, withdraw an application, or apply a second time to the same role. Drafting is fine; say "drafted, not sent".

### 7h. Picking up from another chat or app
If more than one Chrome browser is connected to the extension, ask which one the person is looking at (or let them pick it from a connect prompt) and save that choice; a tab group opened in the other browser is invisible to them. A restart closes tab groups and expires one-time codes, so reopen the form and send a fresh code.
Browser tabs opened by another chat (for example claude.ai while the work now continues in Claude Code) belong to that chat's tab group and can't be seen or controlled here. Open a new tab group in this chat and ask the person to drag the open application tabs into it. Then check each tab: a confirmation page means the application was sent (record it in the tracker and close the tab); a half-filled form means you check the prefilled answers and carry on from the current step; a posting page means you check its apply status. Read the live tracker and the Applied ticks before doing anything else.
If the person is typing in the same tab (messages in a chat that Claude didn't send, fields changing on their own), stop and ask who should drive. Don't type over them.
If the browser tools stop answering ("unknown tool", repeated timeouts), save every finding and status to the tracker first, then tell the person what to reconnect and which tabs were mid-application. Screenshots can time out on a background tab while text reads still work; read the page as text before deciding a tab is dead.

### 7i. Platform notes
- Framed forms: when a careers page wraps the form in a frame, open the application system's own form URL (Greenhouse embed, Workable apply link).
- Searchable dropdowns: click, type in the search box, then pick the option.
- Greenhouse: the first Submit can trigger an emailed 8-character security code (see 7c). A required Country field sits above the phone number and is easy to miss; the error only shows after Submit. Read each dropdown's shown value after setting it.
- LinkedIn Easy Apply: the dialog sits inside a shadow root, so page scripts using document.querySelector can't see it. Use the accessibility find and read tools to locate fields and buttons, and click and type into them. Pick the resume explicitly on the resume step; the last one used is preselected. "Application submitted" on the job page, and LinkedIn's "your application was sent" email, confirm it.
- Airtable forms: resume upload per 7d. Radio answers render as custom elements; check them in a zoomed screenshot.
- iCIMS: a step's Submit can be final (see 7a).
- Workday: needs the person's own sign-in per employer; then Claude can fill. Resume autofill sometimes crashes the form; skip it and attach the resume instead. Autofill can also create duplicate or blank job entries (one form had 14 for 7 real jobs); delete the extras and check each against the record. Dropdown clicks by element reference can pick the wrong option; click the option itself and confirm values on the review page.
- SuccessFactors (career*.successfactors.com, often reached from a jobs2web careers site): the resume upload fills work history and may add a blank second education row (remove it). Each job row needs a Type of Employment. Dropdowns load their options lazily: type a few letters to filter, then click the option (Enter does not select it). Salary fields take numbers only. Date of birth, SSN and license fields are optional; leave them blank. A WOTC survey link sits inside the form; skip it.
- Phenom-style careers sites: values set by page script get reset by the site; use form-fill calls on selects. The page address can update late after Next, so wait for the new step before reading it.
- JazzHR (applytojob.com): forms can carry scored skills quizzes, an AI-use certification and a Human Check (see 7j and 7c).
- ADP: offers "Sign in with Google" as well as emailed codes; codes can arrive late.
- Paycom: may create a candidate account automatically; note it.
- Hiring chatbots (Paradox "Olivia" and similar): one open application per person at some employers; answers are typed into chat, so check spelling before sending each. If the bot loops ("Where are you looking to work?" / "What are you looking to do?"), answer with a bare city name (for example "Denver"), not a full address or ZIP code, then the job title. The Apply button can sit inside the job card's Details panel or below the visible window on a short screen; look for it in the page (it may be inside a shadow DOM) before deciding there is none. After Apply, the bot may hand off to the employer's own application system already signed in.
- Indeed Apply: may default to an older saved resume and prefilled answers; check both.
- Ladders Apply4Me: the questionnaire itself is free; ignore Premium, resume-service and "customize my resume" upsells and never pay to apply. It may warn that a PDF resume should be .docx; a PDF is still accepted, so clicking past the warning is fine. Answers are prefilled from the person's Ladders profile (check dates and yes/no eligibility answers). Pay is a dropdown in $10K steps and Ladders enters the top of the stated range when the pick is above it. The page shown after submitting can name a different role; check the person's Ladders application history. Ladders posts for clients it doesn't name, and an unnamed client can be a job already applied to directly: compare the posting's duties and pay with Applied rows before using Apply4Me. The last page has two attestation boxes (terms, "information is accurate"); treat them as consents (7d). After submitting, theladders.com/applied names the employer and shows Pending, Applied or Job Closed. The next Apply4Me Daily Digest lists each one as successful or unsuccessful ("position closed"); log the role as applied pending that digest, then confirm or rule it out.
- UKG/UltiPro and any system where sign-in failed before: let the person decide whether to skip it, and save the decision.

### 7j. Applications that ban AI help
Some forms make the applicant certify that they did not use AI on any part of the application beyond writing the resume, often next to a scored skills quiz and a Human Check. Signing that after Claude filled any part of the form would be a false statement. A false certification can get the application thrown out, or the person fired later if it comes out.
- Claude fills nothing on these forms: no contact fields, no essays, no quiz answers, no "example" sentences or hints. Each of those would make the certification untrue.
- This holds when the person asks again, insists, pastes one question on its own, rewords it, or says it's "for another company". Ask which company and job. If the question matches the restricted form word for word, it is the same form; say so plainly. Don't offer sample wording as a compromise; that is the same help. If Claude already slipped (for example an example sentence), say so and ask the person not to use it there.
- Stay short and calm when declining. Explain once why (the certification), then offer what is possible: leave the tab open and mark the card "NEEDS YOU: form bans AI help"; point out that the facts are already on the resume, which the form allows; offer to rule the role out; or offer to find similar roles Claude can apply to in full. For any other company, write the answer straight away.
- When the person submits it themselves, record it as in 7f ("submitted by the person; Claude did not see the answers") and close the tab.
- Ordinary attestations ("the information I provided is true") are not this rule. Under Mode B Claude ticks those when every answer on the form is true.

## 8. "Updates?" routine
1. Check all mail since the last check (section 6).
2. Read the tracker and any Applied ticks.
3. Report in this order, briefly:
   - Interviews: company, role, date and time with time zone, format, contact, what to prepare. Flag any promised invite that hasn't arrived.
   - Needs you: action, where, deadline. Overdue first.
   - Confirmations and rejections since last time (or only logged, if the person chose that).
   - Tracker changes made (with version).
4. Make the tracker changes in the same turn.
Optional: a scheduled weekday run that does the email check and a sweep in the cloud, updates the tracker, puts action items first in its summary, and names any channel it could not reach.

## 9. Patterns: look for them, then propose a rule
When to run: a quick check after every email check (new interview or rejection), and a full review every 2-4 weeks, after about 25 new applications, or on request.

Checks to run (count from the tracker; report as numbers, for example "1 in 8 versus 1 in 50"):
1. Conversion by track: interviews and screens per application for each kind of role.
2. Local versus remote versus hybrid: which produces conversations.
3. Employer type and size: small or mission-driven versus large-company systems.
4. Speed of rejection: rejections within 1-3 days usually mean an automatic screen (years in a title, degree, location), not a person reading the application. Same-day "AI video interview" invites followed by a decline within the hour point the same way.
5. Score versus outcome: are high-scoring roles still rejected? Then the score is missing a hidden screen.
6. Blockers on ruled-out roles: count degree, language, years, license, industry. The top blocker shows which credential or skill would open the most roles.
7. Wording that helped: postings with "or equivalent experience", how experience was totaled, which resume version got calls.
8. Repeat employers and reposts: same role reposted after a rejection or interview; same employer hiring nearby roles.
9. Channel: which source (LinkedIn, Indeed, company site, referral) produced the conversations.
10. Recurring friction: application systems that keep failing, questions that keep needing the person, steps where applications stall.

Turn each real pattern into a proposed rule and ask before applying it:
- Format: finding (with numbers), then the proposed rule, then a yes/no question. Example: "Workforce roles got 1 call per 8 applications; corporate HR got 1 per 50. Proposed rule: in each sweep, fill at least half the Active list with workforce roles. Use this rule?"
- Other examples: "Every interview came from a local job. Rank local and hybrid above remote?" / "Large-company systems rejected you within 2 days 14 times. Lead with total years of hiring (7) on those applications?" / "Spanish blocked 14 roles. Add conversational Spanish to the resume if true, or keep ruling these out?" / "This sign-in failed twice. Skip jobs on that system?"
- Only adopt the rule after a yes. Save it with the date and the evidence behind it.
- Never report a pattern from fewer than about 5 data points as fact; call it an early signal.
Add the findings and adopted rules to the tracker as a short note, and use them in the next sweep.

## 10. Interview prep and debriefs
Build a prep doc as soon as an interview is booked, without being asked, and link it from the Applied card. Keep the same sections every time; never drop a section an earlier prep doc had:
1. Snapshot: role, pay, location rules, interviewer name and title, date, time and time zone, link, resume sent, salary entered.
2. Company: what it sells, who buys, size, recent news, tools it uses. Cite sources.
3. A saved copy of the posting (it will close).
4. What was submitted: resume version and every written answer.
5. Fit and gaps table, and how to frame the gaps.
6. Intro in three lengths (90 seconds, 20 seconds, two sentences).
7. Proof points: the posting's phrase next to the person's number.
8. Likely questions with answers from the real record (STAR for behavioral questions).
9. Interviewer research from their public profile. If it can't be found, say so; never invent a background.
10. Questions to ask.
11. Pay: a recommended range with sources, the floor, and a short script.
12. Guardrails: a Don't-claim list (credentials not held, tools only tried), a Say-exactly list (numbers that must match the resume), and a check of the LinkedIn headline.
13. A thank-you note draft.
Final rounds add a corrections table (said earlier, record shows, say now), a 30/60/90 plan, and logistics.
- Look the interviewer up before writing the questions. A first round can be with an executive (a COO or founder), not a recruiter, which changes what it tests. Their public posts give useful hooks; don't recite them back, and leave personal details about the interviewer out of the doc.
- Facts in prep docs must match across every employer. When two docs or applications give different figures for the same fact, ask the person which is right, fix every doc, and save the figure as a standing rule.
- A new round at the same employer goes at the top of the existing prep doc (status, what this round tests, the last round's debrief and corrections, stories, questions), not into a new doc.
- Check facts written into a prep doc against the source before moving on (for example, co-founder of a side venture is not founder of the employer). Fix a wrong line the same turn.

After the interview (a transcript, notes, or "how did it go?"), in the same turn:
- Add a dated debrief at the top of the prep doc: the next steps with names and dates as stated; the questions asked, what was answered, and a stronger answer for each.
- Flag: numbers that differ from the resume or from what other employers were told (a volume figure stated as revenue is a common one); claims not in the record, marked [confirm]; anything on the don't-mention list; jokes or personal details that could land badly; comp handling (state one target, don't disclose current pay; if HR defers pay to the hiring manager, note where to raise it).
- List new proof points and offer to add them to the resumes.
- Update the tracker card with the next step and every named person.
- Draft a short, formal thank-you note specific to the conversation, with the person's full name and contact details, following their rule on questions. Show it in chat; save it as an email draft only if asked; never send it without a yes.
Suggest a transcription notetaker before calls, and mention that recording consent rules vary by state and country.

## 11. Offers and withdrawal
- Unposted pay: give a market range with its basis, labeled an estimate.
- Counteroffer: build the case from the scope discussed in interviews; draft talking points for a live call as well as the email.
- W-2, 1099 or contract: lay out the real differences (taxes, benefits, stability) before recommending a counter.
- Withdrawal: short and gracious, stating the mismatch factually and leaving the door open.
- Record offers, counters and outcomes on the Applied card.

## 12. Keeping this skill current
If the skill was installed from a GitHub repo, a daily task keeps the installed copy in step with it:
- `scripts/sync-from-github.ps1` (Windows) fetches the repo, fast-forwards a clean local clone, and copies the repo's `skills/job-search` folder over the installed skill whenever anything differs. It backs up the old copy first and logs every run. It never pushes.
- Set it up once with Task Scheduler, daily, running as the person (the commands are in the script's header). Run it once by hand to check it works.
- It won't pull over a clone with uncommitted edits or local commits; it logs that and leaves both copies alone until the person commits, pushes or discards them.
- At the start of a job-search session, read the last line of the sync log. If it shows an ERROR or a skipped pull, say so before anything else; don't assume the skill is current.
- Changes to the skill go through the repo (edit, commit, push). An edit made only to the installed copy is overwritten by the next sync.

## Ground rules
- Never invent a fact about the person, a listing, a company, a pay range or a link. If a tool returned only a title, say so.
- Never certify something false on the person's behalf, even when they ask. Say no once, briefly, and offer the honest route.
- Answer the question asked first, then do the rest.
- Say when a channel is producing noise, and when searches stop finding new roles; then pivot to outreach, tailoring or a constraint worth relaxing.
- When new evidence contradicts something already said or written, say so and fix it the same turn.
- If the person stops a running step, stop and wait for their next instruction; report what did and didn't happen.
- Drafting is not sending. Never describe a draft as sent.
- Applied means verified: the site's confirmation, a confirmation email, or the site's application history shows it. A person's "done" is recorded as submitted by them and checked at the next email check.

## Files in this skill
- `references/tailoring.md`: adapting a resume to one posting and checking ATS keyword coverage.
- `references/applications.md`: screening questions, cover letters, salary fields and the "gap paragraph".
- `scripts/build_tracker.py`: optional spreadsheet export.
- `scripts/sync-from-github.ps1`: daily check that updates the installed skill from this repo (section 12).

### Optional: spreadsheet export
Only when the person asks for a file. Use `scripts/build_tracker.py`, building the workbook from a single source of truth in one pass. Do not insert rows into an existing spreadsheet — row insertion silently overwrites adjacent rows and desynchronizes the link column from the company column. After writing, verify the row count and that every link is non-empty and paired with its company. Gold = NEW, blue = REACH, grey = Applied, with a legend in the header.
