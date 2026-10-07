# Claude job search with Indeed and LinkedIn

Connect Claude Desktop to **Indeed** and **LinkedIn**, then add a **job-search skill** that
uses both. Claude searches by what you can *do* rather than by the titles you've held,
reads each full posting, scores it 0–100 against your real background, and keeps
everything in one live **Job Search Tracker** artifact, with **Active Targets**,
**Already Applied**, **Pipeline**, **Lower Matches**, **Archive** and **Ruled Out** tabs,
that it updates whenever you report a change. When an interview is booked, it also builds
an interview prep doc.

Built by [Jibril Sulaiman](https://github.com/carljibrilsulaimanii).

> 🖥️ **Do all of this in the Claude Desktop app, not claude.ai in a web browser.**
> The LinkedIn extension only installs and runs in the desktop app, and the skill and
> connector steps below follow the desktop app's screens. The only time you'll see a web
> browser is when the app opens Indeed's or LinkedIn's sign-in page for you. Get the app
> at https://claude.ai/download.

> 🔄 **The skill checks for LinkedIn updates at the start of every job-search session.**
> The LinkedIn extension never updates itself, and an old version can quietly return empty
> results. So before the first search in each session, the job-search skill compares your
> installed version with the latest release. If you're behind, it shows you both numbers
> and how to update, then lets you choose to update first or carry on. It never installs
> anything itself.

> ⚡ **Quicker: let Claude Code set it up.** Copy this page's link, open the **Code** tab
> in Claude Desktop, and paste:
>
> ```text
> Set up the Indeed + LinkedIn job search from this guide: https://github.com/carljibrilsulaimanii/claude-job-search-indeed-linkedin
> ```
>
> Claude Code follows [Automated setup with Claude Code](#automated-setup-with-claude-code).
> It does the downloads, version checks and file work, and stops at each step only you can
> do: signing in, and the clicks inside Claude Desktop's own settings.

## Contents

- [Automated setup with Claude Code](#automated-setup-with-claude-code)
- [Why it exists](#why-it-exists)
- [What's in this repo](#whats-in-this-repo)
- [Before you start](#before-you-start)
- [Setup, step by step](#setup-step-by-step)
  - [Step 1. Connect Indeed](#step-1-connect-indeed)
  - [Optional: Connect Granola for interview transcripts](#optional-connect-granola-for-interview-transcripts)
  - [Step 2. Install the LinkedIn extension](#step-2-install-the-linkedin-extension)
  - [Step 3. Sign in to LinkedIn on the first tool call](#step-3-sign-in-to-linkedin-on-the-first-tool-call)
  - [Step 4. Add the job-search skill](#step-4-add-the-job-search-skill)
  - [Step 5. Run your first search](#step-5-run-your-first-search)
- [Troubleshooting](#troubleshooting)

## Automated setup with Claude Code

*For people:* paste this page's link into the **Code** tab of Claude Desktop (see the tip
at the top). The rest of this section is written for Claude Code to follow.

*For Claude Code:* the person wants this guide's setup done on their machine. Work through
the checklist in order and report after each item. Rules:

- **Never type the person's passwords, and never complete a sign-in, 2FA prompt or
  CAPTCHA for them.** When a step needs a sign-in, open the page if you can, then stop and
  ask them to do it.
- **Ask before each download** (name the file, its source and its size) and before
  changing anything in Claude's settings.
- You can't click inside Claude Desktop's own Settings or Customize screens. Tell the
  person exactly what to click, quoting the labels from the manual step, and wait until
  they say it's done.
- Confirm with them that they're in the Claude Desktop app. If they're in a web browser,
  stop and point them to https://claude.ai/download.

| # | What Claude Code does | What the person does | Manual step |
|---|---|---|---|
| 1 | Check whether the Indeed connector is already connected in this session (4 tools: `search_jobs`, `get_job_details`, `get_company_data`, `get_resume`) | If it isn't: **Customize → Connectors → Indeed → Connect**, sign in to Indeed, then **Continue connecting** | [Step 1](#step-1-connect-indeed) |
| 2 | Get the latest LinkedIn server version from `https://pypi.org/pypi/mcp-server-linkedin/json` (`info.version`). Read the installed version, if there is one, from `manifest.json` in `%APPDATA%\Claude\Claude Extensions\local.mcpb.daniel-sticker.linkedin-mcp-server\` (Windows) or `~/Library/Application Support/Claude/Claude Extensions/local.mcpb.daniel-sticker.linkedin-mcp-server/` (macOS). | — | [Step 2](#step-2-install-the-linkedin-extension) |
| 3 | If it's missing or older, ask, then download `linkedin-mcp-server-v<latest>.mcpb` from the GitHub release's **Assets** (`gh release download --repo stickerdaniel/linkedin-mcp-server --pattern "*.mcpb"`, or the browser). Never use the repo's source ZIP. | — | [Step 2a–2b](#step-2-install-the-linkedin-extension) |
| 4 | Open the Downloads folder and give the exact file name | Install it: **Settings → Extensions**, drag the file in, confirm. Then **Customize → Connectors → MCP Server for LinkedIn**, switch the toggle to **Enabled**, and switch off `send_message` and `connect_with_person` if they only want search. Quit Claude Desktop from the tray and reopen it. | [Step 2c–2e](#step-2-install-the-linkedin-extension) |
| 5 | After the restart, check that the LinkedIn tools are connected (19 tools). Run one short `search_jobs` call. If it reports setup in progress, wait a minute or two and retry. | Sign in to LinkedIn in the window that opens, including 2FA | [Step 3](#step-3-sign-in-to-linkedin-on-the-first-tool-call) |
| 6 | Zip [`skills/job-search/`](skills/job-search/) from this repo so `job-search/SKILL.md` is at the top of the zip, and put it in Downloads. For Claude Code use, also copy the folder to `~/.claude/skills/job-search`. | **Customize → Skills → + Add**, upload the zip, and make sure **job-search** is on | [Step 4](#step-4-add-the-job-search-skill) |
| 6b | Optional: check whether the Granola connector is connected (`list_meetings`, `get_meeting_transcript`). If it isn't, ask whether they want interview transcripts. | If yes: **Customize → Connectors → Granola → Connect**, sign in, and install the Granola app | [Optional: Granola](#optional-connect-granola-for-interview-transcripts) |
| 7 | Run the ✅ checks from Steps 1–4 and report which pass | Start a new chat with their resume: *"Find jobs I'm qualified for."* | [Step 5](#step-5-run-your-first-search) |

## Why it exists

Searching job boards by title shows you the jobs you already know about, and it keeps
running into the same walls (degree requirements, saturated titles). Postings written for
your skills under titles you've never held don't come up at all.

Claude can fix the search design, but it can't see job boards on its own:

- **Indeed** has an official connector in Claude's connector directory. It gives Claude
  `search_jobs`, `get_job_details`, `get_company_data` and `get_resume`.
- **LinkedIn doesn't publish an MCP server or a Claude connector.** The working option is
  the community project [stickerdaniel/linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server)
  (Apache-2.0). It isn't affiliated with LinkedIn. It drives a real browser that's signed
  in to your own LinkedIn account. It comes as a one-file Claude Desktop bundle (`.mcpb`).
- Connectors alone just return search results. The **skill** adds the method: pull
  capability terms from your resume, search each channel the way it responds best, read
  the full posting before scoring, keep a Ruled Out tab with the blocker named, and keep
  one tracker page as the record for the whole search. Its data lives in JSON blocks the
  page renders, so an apply link can't end up matched to the wrong company.

> ⚠️ **LinkedIn risk.** LinkedIn's User Agreement prohibits automated access, and the
> server's own README warns that accounts using it may be restricted. Use it on your own
> account only if you accept that risk.

## What's in this repo

| Folder | What it is |
|---|---|
| [`skills/job-search/`](skills/job-search/) | The skill: instructions (including the tracker artifact), two reference guides and an optional spreadsheet exporter |

## Before you start

| You need | Notes |
|---|---|
| **Claude Desktop** (the installed Windows or Mac app) | Required. Do every step in the app, not in claude.ai in a web browser. `.mcpb` extensions only work in the desktop app. Older builds called these `.dxt` files and won't open `.mcpb`. Update from https://claude.ai/download if you have no **Extensions** settings page. |
| An **Indeed** account | Used to sign in when you connect it |
| A **LinkedIn** account | Used in the browser window the extension opens |
| Python 3 with `openpyxl` (optional) | Only if you'll run the optional spreadsheet export yourself. When Claude runs it in its own sandbox, you don't need it. |

## Setup, step by step

### Step 1. Connect Indeed

About 5 minutes, plus 5 if you need to update your Indeed resume.

Indeed is an official connector in Claude's directory. You don't download or install
anything. You sign in to Indeed once, and Claude gets four Indeed tools.

**1a. (Optional, 5 minutes) Get your Indeed profile ready.** On indeed.com, sign in and
upload your current resume to your profile. The connector's `get_resume` tool reads the
resume saved there. If it's old or missing, Claude starts from the wrong background, or
you'll have to attach a resume to every chat.

**1b. Open the connector directory.** In the Claude Desktop app, open
**Customize** and select the **Connectors** tab. Switch from **Yours** to **Discover**,
or click **+ Add** and choose to browse connectors (wording may differ).

**1c. Find Indeed.** Search the directory for **Indeed** and open it. Check that the
publisher is Indeed, not a look-alike. Its page has a **← Your connectors** link at the
top, the Indeed logo, and the line *"You're not connected to Indeed yet."*

**1d. Connect it.** Click **Connect**. Your web browser opens on Indeed's sign-in page.

1. Sign in with the Indeed account from 1a.
2. Indeed asks you to allow Claude access to your account. Review it and approve
   (wording may differ).
3. The browser hands you back to Claude, which shows **Finish connecting a connector?**
   with the note *"Only continue if you started connecting a connector from Claude
   Desktop."* Optionally click **Show destination** to check it's Indeed, then click
   **Continue connecting**.

⚠️ That screen is a safety check. Click **Continue connecting** only if you just clicked
**Connect** yourself. If a link in an email or web page brought you there, click
**Not now**.

**1e. Confirm it's on.** Go back to Indeed's page (**Customize → Connectors**, then
**Indeed**). The *"You're not connected to Indeed yet"* message is gone. In a chat, open
the tools menu in the message box and make sure **Indeed** is switched on.

*Claude Code:* connectors added to your claude.ai account appear in Claude Code too. Its
list shows Indeed as a "connector" with 4 tools. If it's missing, run `/mcp` in an
interactive `claude` terminal and sign in there.

**What Claude gets:**

| Tool | Inputs | What Claude uses it for |
|---|---|---|
| `search_jobs` | `search` (title or keywords), `location` (city and state, or `remote`), `country_code` (e.g. `US`), optional `job_type` (`fulltime`, `parttime`, `contract`, `internship`, `temporary`) | One search on Indeed's job search API. Results include an apply link for each job. |
| `get_job_details` | `job_id` (from a search result) | The full posting: requirements, pay, description, apply link, and any contact names in the text |
| `get_company_data` | `companyName`, optional `jobTitle`, location, and which categories to pull (`metadata`, `ratings`, `salaries`) | Employer info, employee ratings, and salaries for a given job title, used to check pay when a posting doesn't list it |
| `get_resume` | none | The resume on your Indeed profile |

**1f. Test it.** Start a new chat and ask:

> *Search Indeed for remote operations analyst jobs in the US and show me the top five.*

Success: Claude calls `search_jobs` and lists real postings, with each job title linked to
its apply page. Then ask *"Get the full details for the first one"*: Claude calls
`get_job_details` and shows the requirements and pay. Finally ask *"What's on my Indeed
resume?"*: Claude calls `get_resume` and summarizes your profile resume.

⚠️ **One location per search.** `search_jobs` takes a single location, so "Atlanta and
remote" is two searches. Claude runs one per location you'll accept.

⚠️ **Loose keyword matching.** Different wording of the same idea surfaces different
postings from the same pool, so vary the phrasing. Indeed is also the better channel for
local and metro searches.

⚠️ **Salary data needs a job title.** `get_company_data` can only look up pay for a
specific title. If you ask "what does this company pay?" with no title, Claude has to
infer one or ask you.

⚠️ **Keep the links whole.** Indeed's apply URLs carry tracking parameters, and a link
with them stripped may not open the right job. The skill puts the full URL in the
spreadsheet.

✅ **Check:** Indeed shows as connected under **Customize → Connectors**, the test search
returns real postings with working apply links, and `get_resume` returns your current
resume.

### Optional: Connect Granola for interview transcripts

About 5 minutes. Worth doing before your first interview.

Granola is an AI notepad that transcribes your calls from your computer's own audio, so
no bot joins the meeting. With its Claude connector, Claude can pull each interview's
transcript itself, so you don't have to paste it.

**a.** In the Claude Desktop app: **Customize → Connectors**, find **Granola**, click
**Connect**, and sign in (wording may differ).

**b.** Install the Granola app from https://granola.ai and let it run during interviews.

**c.** After the call, Claude pulls the transcript to write the debrief, the thank-you
email and the next round's prep ([Step 5h](#step-5-run-your-first-search)).

| Tool | What Claude uses it for |
|---|---|
| `list_meetings`, `get_meetings` | Finding the interview |
| `get_meeting_transcript` | The full transcript: questions asked, your answers, names and next steps |
| `query_granola` | Questions across your meetings ("what did they say about the team?") |

⚠️ **Consent.** Recording and transcription rules vary by state and country, and some
require everyone on the call to agree. Tell the interviewer you're taking notes with a
transcription tool.

✅ **Check:** Granola shows as connected under **Customize → Connectors**, and after a
test meeting Claude can list it.

### Step 2. Install the LinkedIn extension

About 5 minutes.

**2a.** Open the releases page:
https://github.com/stickerdaniel/linkedin-mcp-server/releases/latest

⚠️ **Don't use the green Code → Download ZIP button** on the repo's main page. That
downloads the source code (`main.zip`), which Claude Desktop can't install. The
installable file is only on the **Releases** page.

**2b.** Under **Assets**, download the `.mcpb` file, named
`linkedin-mcp-server-v<version>.mcpb`. It's under 1 MB and lands in your **Downloads**
folder.

Direct link to the version current when this guide was written (v4.26.2):
https://github.com/stickerdaniel/linkedin-mcp-server/releases/download/v4.26.2/linkedin-mcp-server-v4.26.2.mcpb

The file name includes the version, so this link always downloads 4.26.2. If the
releases page shows a newer version, download that one instead.

**2c.** Don't double-click it. On Windows there's usually no program set to open `.mcpb`
files, so nothing happens. Install it from inside Claude Desktop instead:

1. Open **Settings** (click your name at bottom-left, or press **Ctrl + ,**).
2. Select the **Extensions** tab.
3. Either drag the `.mcpb` file from your Downloads folder onto the Extensions page, or
   click **Install Extension** / **Install from file** and pick it (wording may differ).
4. Confirm the install prompt.

**2d. Enable it.** The extension is listed with your connectors. Open **Customize →
Connectors** and click **MCP Server for LinkedIn**. Its page has:

| On the page | What to do |
|---|---|
| A toggle reading **Disabled** / **Enabled** | Switch it on. It can be off after install, and an off extension gives Claude no LinkedIn tools. |
| **Uninstall** | Leave it. Use it only to remove the extension, for example before reinstalling. |
| **Proxy server**, **Proxy username**, **Proxy password**, **Proxy bypass list** | Leave all four blank unless you need a proxy. If you fill any in, click **Save**. |
| *"Enable this connector to configure its tools."* | Once it's enabled, the per-tool switches appear here (see the ⚠️ below) |
| **View details** | Shows the version and description. Use it to check you're on the latest release. |

**2e.** Quit Claude Desktop completely and reopen it. On Windows, right-click the tray
icon and choose **Quit**; closing the window isn't enough.

The extension adds 19 tools. The ones the job search uses:

| Tool | What Claude uses it for |
|---|---|
| `search_jobs` | LinkedIn job search |
| `get_job_details` | The full posting, including the job poster's name |
| `get_saved_jobs` | Jobs you've saved on LinkedIn |
| `get_company_profile`, `get_company_employees` | Employer info and who works there |
| `get_person_profile` | A recruiter's or interviewer's public profile |
| `get_my_profile` | Your own profile, to check it matches the resume you're sending |

⚠️ **Some tools act on your account:** `send_message` and `connect_with_person` send
messages and connection requests as you. If you only want search, switch those two off
in the tool list on the extension's page (2d). The list only appears once the extension
is enabled.

⚠️ **The bundle never updates itself.** LinkedIn page changes break older versions, often
with empty results rather than a clear error. To update, download the newest `.mcpb` from
the releases page and install it the same way (2c–2e). The job-search skill checks your
version against the latest at the start of each session and tells you if you're behind
([Step 4](#step-4-add-the-job-search-skill)).

✅ **Check:** after the restart, **Customize → Connectors → MCP Server for LinkedIn** shows
the toggle **Enabled**, and **View details** shows the latest release's version.

### Step 3. Sign in to LinkedIn on the first tool call

About 5 minutes, mostly waiting.

**3a.** In a new chat, ask *"Search LinkedIn for operations analyst jobs."*

**3b.** On first start, the extension downloads its own Chromium browser (about 200 MB)
in the background, into `~/.linkedin-mcp/patchright-browsers`. If you call a tool before
that finishes, it returns a setup-in-progress error. Claude will say something like
*"LinkedIn's browser is still downloading in the background"* and wait. Give it a minute
or two and retry.

**3c.** On the first tool call that needs your account, a browser window opens on
LinkedIn's login page. Sign in normally, including 2FA. The session is saved locally
under `~/.linkedin-mcp`.

**3d.** Ask Claude to retry the search.

⚠️ LinkedIn works best with **short** queries. Two or three words (*"recovery coach"*)
return clean results. Long keyword strings return almost nothing but promoted ads.

✅ **Check:** the retry returns real LinkedIn postings with links.

### Step 4. Add the job-search skill

About 3 minutes.

**4a.** Download this repo (**Code → Download ZIP**) and unzip it.

**4b.** Zip the **`job-search`** folder by itself, so the zip has `job-search/SKILL.md` at
its top level. The folder has:

| File | What it does |
|---|---|
| [`skills/job-search/SKILL.md`](skills/job-search/SKILL.md) | The workflow Claude follows: check that Indeed and LinkedIn are connected and that the LinkedIn extension is current, ingest past applications, extract capabilities, search, score, rule out, harvest contacts, build and maintain the Job Search Tracker artifact, and make interview prep docs |
| [`skills/job-search/references/tailoring.md`](skills/job-search/references/tailoring.md) | Tailoring a resume to one posting and checking ATS keyword coverage |
| [`skills/job-search/references/applications.md`](skills/job-search/references/applications.md) | Screening questions, cover letters, salary fields, the "gap paragraph" |
| [`skills/job-search/scripts/build_tracker.py`](skills/job-search/scripts/build_tracker.py) | Optional `.xlsx` export, built from one data list in a single pass |

**4c.** In Claude Desktop, open **Customize**, select **Skills**, click **+ Add** and
upload the zip (wording may differ).

**4d.** The skill appears under **Created by you** as **job-search**. Make sure it's turned on.

*Claude Code instead of Desktop (optional):* copy the `skills/job-search` folder to
`~/.claude/skills/job-search`. Claude Code picks it up in new sessions. You still need
connectors that Claude Code can see.

🔄 From now on, every job-search session starts with an update check. Claude confirms
Indeed and LinkedIn are connected and the LinkedIn extension is **Enabled**, and compares
its version with the latest release (see [Step 5c](#step-5-run-your-first-search)). You
don't have to remember to check for updates yourself.

✅ **Check:** **job-search** is listed under **Customize → Skills → Created by you**.

### Step 5. Run your first search

About 15–30 minutes for a full pass.

**5a.** Start a new chat, attach your resume, and say *"Find jobs I'm qualified for."* The
skill triggers on requests like that.

**5b.** If you've been applying already, export your history first: Indeed's **My Jobs**
page saves as `.mhtml` (in your browser: **Save page as**), and LinkedIn has **My Items**.
Attach it. Claude puts those jobs on an **Already Applied** tab so you don't apply twice.
It also counts the title words, which shows when one title has stopped working for you.

**5c. Update check (every session).** Before the first search in each session, Claude checks that both channels are connected and
compares your LinkedIn extension's version with the latest on PyPI. If you're behind, it
gives you both numbers and the update steps, and lets you choose to update first or carry
on. It never installs anything itself.

**5d.** Claude lists 15–25 capability search terms from your resume and asks you to
confirm them. Fix them now, before it runs dozens of searches on the wrong terms.

**5e.** Answer the location questions: home city, commutable metros, remote, and any
city you'd move to.

**5f.** Claude searches Indeed, LinkedIn and the web, pulls each promising posting in
full, scores it, and **creates your Job Search Tracker artifact**: a web page in Claude
titled **"&lt;Your name&gt; — Job Search Tracker"**, private to you (*Artifact · Only you*).
A card for it appears in the chat. Click **Open** to view it.

The tracker has a dark masthead with live counts, a stat rail (Active, Pipeline, Lower
Matches, Applied, Ruled Out, Interviews), light and dark themes, and works on a phone.
Each of the six tabs shows its count:

| Tab | What's on it |
|---|---|
| **Active Targets** | Roles that clear your score threshold, sorted by score. Each card has a score badge (85+ green, 70–84 amber, under 70 grey), location, pay, track and status tags (NEW gold, REACH blue), when it was posted and found, a collapsible **Why it fits & what to watch** with the resume version to send, the named contact, and an **Open posting** button. |
| **Already Applied** | Roles you've applied to this round, with a status (Applied, Interviewing, Offer, Rejected), the date, where you found it, and a **Latest:** box for the next step: call times, take-home assignments, deadlines, and a link to the interview prep doc. |
| **Pipeline** | Promising roles that need one thing confirmed before they can be scored (pay not posted, status unclear), with an amber **Verify:** line naming it |
| **Lower Matches** | Open roles with no hard blocker that score under your cutoff. Same cards as Active Targets, sorted by score. A low score isn't a blocker, so these are kept, not ruled out. |
| **Archive** | Your earlier application history as a searchable, sortable table, with suspicious recruiter outreach flagged |
| **Ruled Out** | Each role with its hard blocker named in a red box, so you don't re-evaluate it in three weeks |

⚠️ **It's one tracker for the whole search.** Claude updates the same artifact at the same
link every time, and never makes a second one. To pick up in a new chat, paste the
tracker's link. Claude reads it and keeps editing that one.

**5g. Keep it current by just telling Claude.** You don't edit the page yourself:

| You say or paste | Claude does |
|---|---|
| *"I applied to X"*, or a confirmation screen or email | Moves the card to **Already Applied** with the date and contact. A LinkedIn "apply now to your saved job" reminder doesn't count. |
| Interview news: a call, a screen, an assignment, a submission | Sets the status to **Interviewing**, updates the **Latest:** box, and builds an interview prep doc ([5h](#step-5-run-your-first-search)) |
| A posting that says *"No longer accepting applications"* | Moves it to **Ruled Out** as "Posting closed (checked <date>)", keeping the score and contact in case it's reposted |
| *"Remove everything under 75"* | Applies the threshold to **Active Targets** and every future addition. Open roles under it move to **Lower Matches**, not deleted. Roles you've applied to are never moved or removed for their score. |
| *"Triage the pipeline"* | Pulls every Pipeline posting: closed or blocked → **Ruled Out** with the reason, at or above the threshold → **Active**, open but under it → **Lower Matches** |
| *"Show me more options"* | Re-checks **Lower Matches**. New information (pay, a warm contact, a waived requirement) can move a role up to Active, and closed postings move to Ruled Out. |

New finds go onto the tracker in the same turn they're found, and each update ends with a
one-line report of what moved where.

**5h. Once an interview is scheduled.** Tell Claude, or paste the scheduling email or
calendar invite. You don't need to ask for prep. This happens automatically, in this
order:

| # | What happens | Where you see it |
|---|---|---|
| 1 | The job's status changes to **Interviewing** (green pill). If it was still on Active Targets or another tab, it moves to **Already Applied**. | The tracker |
| 2 | The **Latest:** box gets the interview details: date and time, video link, who you're meeting, and any take-home assignment and its deadline | The job's card on **Already Applied** |
| 3 | Claude looks up the interviewer by name, from the scheduling email or the posting, and reads their LinkedIn profile. Someone who built training programs asks different questions than someone who came up through sales. | In the chat |
| 4 | Claude builds an **interview prep doc** (a Claude Doc when available) and links it from the card's **Latest:** box | A link in the chat and on the card |
| 5 | The tracker's counts and the Applied notes box update: who's interviewing, who's declined | The masthead, stat rail and **Already Applied** notes |
| 6 | Claude recommends recording the call with Granola if it isn't connected, with the consent reminder | In the chat |
| 7 | **After the call:** Claude reads the Granola transcript, debriefs your answers (what was asked, what you said, stronger answers), drafts a thank-you email citing points from the conversation, and updates the prep doc for the next round | The chat, the prep doc, and the card's **Latest:** box |

**What's in the prep doc:**

| Section | Contents |
|---|---|
| The job | The original job link and the full job description, so you have it even after the posting closes |
| 20 role questions | The questions most likely for this role, each with an answer in your voice built only from your real record. Nothing is invented. |
| 20 interviewer questions | Questions this specific interviewer is likely to ask, based on their background, with answers |
| Your intro | A short "tell me about yourself" you can say in under a minute |
| 3 questions to ask | Questions for you to ask the interviewer |

For a short screen (around 15 minutes), the four or five questions most likely to come
up are marked, since that's all there's time for. If the interviewer isn't technical,
the answers use plain language.

**For later rounds,** the transcript is what makes the prep better. Claude pulls out the
questions they're likely to dig into, the answers to tighten, anything you promised to
follow up on, and the names mentioned for the next panel, then researches those people.

⚠️ **Consent.** Tell the interviewer you're taking notes with a transcription tool. Some
states and countries require everyone on the call to agree.

**After each step,** tell Claude what happened: the call went well, you got a take-home,
you submitted it, a second round was booked. Claude adds it to the **Latest:** box, and a
new interview round gets its own prep. An offer sets the status to **Offer**; a
rejection sets it to **Rejected** (red).

⚠️ **Read every answer before you use it.** The answers come only from what's on your
resume and in your chats, but you'll be asked to expand on anything you say. If a detail
isn't exactly right, fix it in the doc.

**5i. (Optional) Spreadsheet export.** If you want a file, ask for one. Claude builds an
`.xlsx` with
[`skills/job-search/scripts/build_tracker.py`](skills/job-search/scripts/build_tracker.py).
To run it yourself, edit the `MATCHES`, `ALREADY_APPLIED` and `RULED_OUT` lists at the
top, then:

```bash
pip install openpyxl
```

```bash
python skills/job-search/scripts/build_tracker.py job_matches.xlsx
```

It prints the row counts, lists any rows without a real URL, and warns if a match is a
job you already applied to.

⚠️ **REACH cards are the most valuable.** You meet every requirement but one, and often the
posting names the hiring manager. Contact them directly instead of applying cold.

⚠️ **Postings close fast**, often within two to four weeks. Ask Claude to re-check older
cards before you apply.

⚠️ Requirements vary by posting, even within one company. The same title can have a
no-degree path in one city and require a bachelor's degree in another. Check each one.

✅ **Check:** the **Job Search Tracker** card opens a page with all six tabs. Every
**Open posting** button goes to a real link, or the card shows a literal
`SEARCH LINKEDIN: …` / `SEARCH INDEED: …` string. A link should never be made up. Telling
Claude *"I applied to <one of them>"* moves that card to **Already Applied** at the same
link.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Indeed isn't in the tools menu | It's turned off for this chat, or not connected. Check **Customize → Connectors → Yours** and switch it on ([Step 1e](#step-1-connect-indeed)). |
| Indeed asks you to sign in again, or its tools error | The connection expired. Open Indeed under **Customize → Connectors** and reconnect it (wording may differ). |
| `get_resume` returns an old or empty resume | Upload your current resume to your Indeed profile ([Step 1a](#step-1-connect-indeed)), or attach it to the chat instead |
| An Indeed apply link opens the wrong job or a search page | The URL was shortened or its parameters were stripped. Ask Claude to repeat `get_job_details` and copy the full link. |
| You downloaded `main.zip` and there's nothing to install | That's the source code from **Code → Download ZIP**. Get the `.mcpb` from **Releases → Assets** ([Step 2a](#step-2-install-the-linkedin-extension)). |
| Claude has no LinkedIn tools after installing | The extension's toggle says **Disabled**. Switch it on under **Customize → Connectors → MCP Server for LinkedIn**, then quit and reopen Claude Desktop. |
| Double-clicking the `.mcpb` does nothing | Install it from **Settings → Extensions** ([Step 2c](#step-2-install-the-linkedin-extension)) |
| No **Extensions** page in Settings | Claude Desktop is too old, or you're in a browser. Update from https://claude.ai/download. |
| LinkedIn tool says setup is in progress | The browser download hasn't finished. Wait a minute or two and retry ([Step 3b](#step-3-sign-in-to-linkedin-on-the-first-tool-call)). |
| LinkedIn searches suddenly come back empty | Your LinkedIn session expired. Trigger the login again ([Step 3c](#step-3-sign-in-to-linkedin-on-the-first-tool-call)), or delete the saved session under `~/.linkedin-mcp` and let it ask again. |
| *"Update available: mcp-server-linkedin X is out (you are on Y)"* | Download the newest `.mcpb` from the [releases page](https://github.com/stickerdaniel/linkedin-mcp-server/releases/latest), install it under **Settings → Extensions**, then quit and reopen Claude Desktop |
| LinkedIn results are all ads, voice-actor gigs and "AI trainer" roles | Your query is too long. Use two or three words. |
| One channel starts rate-limiting | Switch to the other channel or to web search, and have Claude save results to the tracker first. If every channel is throttled, stop and come back later. |
| A tool vanished mid-session | Loading a new tool can unload one already in use. Ask Claude to check which tools are available. |
| Extension changes don't take effect | Quit Claude Desktop from the tray icon, not just the window, then reopen it. |
| Manual JSON config or Docker instead of the bundle | The command, arguments and sign-in steps change between versions. Copy them from the [upstream README](https://github.com/stickerdaniel/linkedin-mcp-server#readme), not from an old guide. |
