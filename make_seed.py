""" 
Generates tickets_seed.json, the ticket set this playbook is built on.

Run it only if you want to change the data. The committed tickets_seed.json is
what every expected result in the playbook was derived from, so if you change
anything here you must re-run this AND re-run check_expectations.py, or the
playbook's stated results stop being true.

    python make_seed.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Each ticket carries a deliberate shape. The "why" field never reaches GitHub.
# It is here so that whoever maintains this set knows what each row is for.
TICKETS = []


def add(title, body, labels, kb, outcome, why, reporter="wewin-user"):
    TICKETS.append({
        "title": title,
        "body": body,
        "labels": labels,
        "expected_kb": kb,          # which article should match, "" for none
        "expected_outcome": outcome,  # DEFLECT, ROUTE, CLARIFY, DUPLICATE
        "why": why,
        "reporter": reporter,
    })


# ---------------------------------------------------------------------------
# 1. CLEAN DEFLECTIONS. One obvious KB match each.
#    These prove the happy path and they are what a demo opens with.
# ---------------------------------------------------------------------------
add("Cannot log in, account says locked",
    "I typed my password wrong a few times this morning and now it says my "
    "account is locked. I need to get back in before my 10am call.",
    ["access"], "password-reset", "DEFLECT",
    "Textbook deflection. Unambiguous wording, exact KB match.")

add("Forgot my password",
    "I have forgotten my WEWIN password and need to reset it. I am working "
    "from home today so I cannot come to the service desk.",
    ["access"], "password-reset", "DEFLECT",
    "Same article, different wording. Proves semantic match, not keyword.")

add("Password expired overnight",
    "Logged in this morning and it told me my password expired. The reset "
    "link in the email does not seem to work.",
    ["access"], "password-reset", "DEFLECT",
    "Third wording for the same article. Three is enough to show a pattern.")

add("VPN will not connect from home",
    "The VPN client spins for about thirty seconds and then says it cannot "
    "reach the gateway. It worked fine in the office yesterday.",
    ["network"], "vpn-guide", "DEFLECT",
    "Clean deflection on a second article.")

add("How do I get on the VPN on a new laptop",
    "I picked up my replacement laptop and there is no VPN client on it. "
    "What do I need to install and where do I get the config?",
    ["network"], "vpn-guide", "DEFLECT",
    "Deflects, and also shows the KB covering a setup question.")

add("Outlook stopped syncing",
    "My email has not updated since yesterday afternoon. Outlook says "
    "Disconnected in the bottom corner. Webmail works fine.",
    ["email"], "outlook-sync", "DEFLECT",
    "Clean deflection on a third article.")

add("Not receiving any new mail",
    "No new mail since about 4pm yesterday. Colleagues say they have sent "
    "me things. Restarting Outlook did not help.",
    ["email"], "outlook-sync", "DEFLECT",
    "Describes the symptom without naming the product. Harder match.")

add("Printer on 3rd floor not responding",
    "The printer by the kitchen on floor 3 shows offline on my machine. "
    "Other people seem to be printing to it fine.",
    ["hardware"], "printer-setup", "DEFLECT",
    "Deflection where the KB fix is per-user, not a broken device.")

add("How do I add the finance printer",
    "I have moved desks to the finance area and need to add the printer "
    "they all use. What is the queue name?",
    ["hardware"], "printer-setup", "DEFLECT",
    "Setup question against the same article.")

add("Need to set up email on my phone",
    "I have a new work phone and need WEWIN mail on it. Is there a profile "
    "I am supposed to install first?",
    ["email"], "mobile-email", "DEFLECT",
    "Fourth article. Keeps the KB from looking like it only covers three things.")

add("Mail app on iPhone keeps asking for password",
    "My phone prompts for the mail password every few hours and rejects it "
    "even though the same password works on my laptop.",
    ["email"], "mobile-email", "DEFLECT",
    "Same article, symptom wording.")

add("Wifi drops every few minutes in meeting room 4",
    "Connection drops roughly every five minutes in MR4. Fine everywhere "
    "else on the floor.",
    ["network"], "wifi-troubleshooting", "DEFLECT",
    "Fifth article.")

add("Cannot see the guest wifi network",
    "A visitor needs wifi and I cannot find the guest network on their "
    "laptop. Has it been renamed?",
    ["network"], "wifi-troubleshooting", "DEFLECT",
    "Same article from the other side, helping somebody else.")

add("Shared drive not mapping on startup",
    "The S drive disappears every time I restart. I have to map it again "
    "manually each morning.",
    ["access"], "shared-drive", "DEFLECT",
    "Sixth article. Recurring-annoyance shape.")

add("Lost access to the marketing shared folder",
    "I could open the marketing folder on the S drive last week and now I "
    "get access denied. Nothing changed on my end.",
    ["access"], "shared-drive", "DEFLECT",
    "Same article but the real cause may be entitlement. Watch this one in "
    "the demo: a confident deflection here is arguably wrong.")

# ---------------------------------------------------------------------------
# 2. ROUTE. Real work, no KB answer. These must NOT be deflected.
#    If your build deflects any of these, the confidence threshold is too low.
# ---------------------------------------------------------------------------
add("Laptop will not power on at all",
    "Pressed the power button repeatedly, no lights, no fan. It was fine "
    "when I shut it down on Friday. Charger light is on.",
    ["hardware"], "", "ROUTE",
    "Hardware failure. No article can fix it. Must route.")

add("Screen has a crack after being dropped",
    "I dropped my laptop in the car park and the bottom third of the screen "
    "is black with a visible crack.",
    ["hardware"], "", "ROUTE",
    "Physical damage. Must route, and probably to asset management.")

add("Need Tableau Creator licence for the quarterly pack",
    "I have been asked to rebuild the quarterly reporting pack and I need "
    "Creator rather than Viewer to do it.",
    ["software"], "", "ROUTE",
    "Entitlement request. Needs the approval path, not an article.")

add("Request access to the HR reporting folder",
    "I have moved into the people analytics team and need access to the HR "
    "reporting folder on the S drive.",
    ["access"], "", "ROUTE",
    "Access request with an approval, NOT the shared-drive article. This is "
    "the pair that proves the threshold is doing real work.")

add("New starter needs a full setup for Monday",
    "We have a new analyst starting Monday. She needs a laptop, accounts, "
    "and the finance systems. Who sets that up?",
    ["access"], "", "ROUTE",
    "Multi-step provisioning. Route to the onboarding process.")

add("Database server keeps timing out for the whole team",
    "Since about 9am the reporting database times out for everyone in the "
    "team. Four of us have tried.",
    ["infrastructure"], "", "ROUTE",
    "Potential major incident. Must escalate, never auto-close.")

add("Suspicious email asking for my credentials",
    "I received an email that looks like it is from IT asking me to confirm "
    "my password on a link. I have not clicked it.",
    ["security"], "", "ROUTE",
    "Security. Must route to a human every time, whatever the KB says.")

add("Need a second monitor for the new desk",
    "I have moved to a hot desk that only has one monitor and I need two "
    "for the reconciliation work.",
    ["hardware"], "", "ROUTE",
    "Equipment request. Catalogue item, not an article.")

add("Payroll system rejecting my timesheet",
    "The timesheet system will not accept my hours for last week. It says "
    "the period is closed but my manager says it is open.",
    ["software"], "", "ROUTE",
    "Application issue needing an owner. No general article applies.")

add("Please remove leaver access for Tom Hale",
    "Tom left on Friday. Please revoke his accounts and reclaim his laptop.",
    ["security"], "", "ROUTE",
    "Leaver process. Route, and it has an SLA.")

# ---------------------------------------------------------------------------
# 3. CLARIFY. Too vague to act on. These must come back with a question.
# ---------------------------------------------------------------------------
add("Not working",
    "It is not working.",
    [], "", "CLARIFY",
    "The shortest real ticket a service desk gets. Must ask, never guess.")

add("Help",
    "Need help urgently please.",
    [], "", "CLARIFY",
    "No content at all. Tests that empty bodies do not crash the pipeline.")

add("Issue with the thing on my computer",
    "There is a problem with the thing I use for the reports. Can someone "
    "call me.",
    [], "", "CLARIFY",
    "Words but no signal. A keyword matcher might fire on 'reports'.")

add("Same problem as last time",
    "It is doing the same thing it did last month. You fixed it then.",
    [], "", "CLARIFY",
    "Needs history, which the ticket does not carry. Must ask.")

add("URGENT!!!",
    "This is urgent.",
    ["priority"], "", "CLARIFY",
    "Urgency without content. Tests that a label does not substitute for a body.")

# ---------------------------------------------------------------------------
# 4. EDGE CASES. The ones that break ingestion rather than matching.
# ---------------------------------------------------------------------------
add("",
    "Body with no title at all. Some trackers allow this and the field "
    "mapping has to cope.",
    [], "", "CLARIFY",
    "EMPTY TITLE. If Title is mapped and this row vanishes, you have found "
    "a silent drop.")

add("Ticket with no body",
    "",
    ["access"], "", "CLARIFY",
    "EMPTY BODY. Body is the field the RAG indexer reads. An empty one must "
    "not become a confident match.")

add("Password reset please",
    "I need a password reset.",
    ["access"], "password-reset", "DUPLICATE",
    "DUPLICATE of the earlier password tickets by content, not by ID. "
    "Dedup is on External ID, so this SHOULD ingest as its own ticket. "
    "If it does not, your External ID mapping is wrong.")

add("Reopened: VPN will not connect from home",
    "This was closed but it is happening again today. Reopening.",
    ["network"], "vpn-guide", "DEFLECT",
    "A reopen. Tests that an updated ticket re-ingests on incremental sync "
    "rather than being skipped as already seen.")

add("Ticket with unicode and quotes in the body",
    "The user said \"it broke\" and the path was C:\\Users\\test\\file.txt "
    "with 50% free space and a #hash and an &ampersand.",
    [], "", "CLARIFY",
    "ESCAPING. Quotes, backslashes, percent, hash, ampersand. If this row "
    "arrives mangled, your custom script or your JSON handling is wrong.")

add("Very long ticket body",
    "The user wrote an essay. " + ("This sentence repeats to make the body long. " * 60),
    [], "", "CLARIFY",
    "LENGTH. Some fields truncate. Check whether the whole body arrived.")

# ---------------------------------------------------------------------------
# 5. VOLUME. Padding so that one page of the API is not the whole set.
#    GitHub returns 30 per page by default. With these the set passes 30 and
#    an un-paginated ingestion visibly stops short.
# ---------------------------------------------------------------------------
VOLUME = [
    ("Teams audio not working in calls", "No sound through my headset in Teams calls. Works in Spotify.", ["software"]),
    ("Cannot join the all hands link", "The all hands link opens a blank page for me.", ["software"]),
    ("Excel crashing on large files", "Excel closes itself when I open the reconciliation workbook.", ["software"]),
    ("Keyboard sticky keys", "Several keys need a hard press since I spilled coffee.", ["hardware"]),
    ("Docking station not charging", "Laptop does not charge through the dock, only direct.", ["hardware"]),
    ("Need access to Jira", "Starting on the migration project and need a Jira account.", ["access"]),
    ("Calendar invites not appearing", "Invites arrive as plain email and not in my calendar.", ["email"]),
    ("Mobile app will not accept my pin", "The WEWIN mobile app rejects the pin I set last week.", ["software"]),
    ("Slow boot in the mornings", "Takes about nine minutes from power on to usable.", ["hardware"]),
    ("Cannot print double sided", "Duplex option is greyed out on the finance printer.", ["hardware"]),
    ("Zoom plugin missing from Outlook", "The Zoom scheduling button has gone from my Outlook ribbon.", ["software"]),
    ("Guest account for auditor", "External auditor needs read access for two weeks.", ["security"]),
    ("Two factor prompts every login", "I tick remember me and it still prompts every time.", ["access"]),
    ("Disk almost full warning", "Windows says 2GB free and will not let me save.", ["hardware"]),
    ("Need the old file back", "Deleted a file from the S drive this morning by mistake.", ["access"]),
]
for t, b, lbl in VOLUME:
    add(t, b, lbl, "", "ROUTE", "Volume. Forces pagination past the 30 default.")


def main():
    out = {
        "generated_by": "make_seed.py",
        "ticket_count": len(TICKETS),
        "note": "Seeded into a GitHub repo as Issues by seed_lab.py. "
                "The expected_kb, expected_outcome and why fields are for the "
                "playbook and are NOT sent to GitHub.",
        "tickets": TICKETS,
    }
    path = os.path.join(HERE, "tickets_seed.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
        f.write("\n")

    counts = {}
    for t in TICKETS:
        counts[t["expected_outcome"]] = counts.get(t["expected_outcome"], 0) + 1

    print("wrote " + path)
    print("tickets: " + str(len(TICKETS)))
    for k in sorted(counts):
        print("  " + k.ljust(10) + str(counts[k]))
    print("")
    print("pages at GitHub default per_page=30: "
          + str((len(TICKETS) + 29) // 30))


if __name__ == "__main__":
    main()
