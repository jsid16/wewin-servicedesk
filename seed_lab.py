""" 
Seeds your lab repository with the 51 tickets this playbook is built on.

WHAT IT DOES
    Creates the labels, then creates one GitHub Issue per ticket in
    tickets_seed.json. That is your inbound ticket queue for the next two days.

WHAT YOU NEED
    1. A GitHub account. A personal one is fine. No organisation needed and no
       infosec approval needed, which is the whole reason this lab uses GitHub.
    2. An empty repository. Private is fine. Call it wewin-servicedesk.
    3. A fine grained personal access token with Issues: Read and write on that
       one repository. Nothing else. Settings, then Developer settings, then
       Personal access tokens, then Fine-grained tokens.

HOW TO RUN IT
    Always dry run first. It calls nothing and prints what it would do.

        python seed_lab.py --owner YOURNAME --repo wewin-servicedesk --dry-run

    Then for real. Put the token in an environment variable, never on the
    command line, because the command line ends up in your shell history.

        Windows    set GITHUB_TOKEN=github_pat_xxx
        Mac/Linux  export GITHUB_TOKEN=github_pat_xxx

        python seed_lab.py --owner YOURNAME --repo wewin-servicedesk

    It takes about two minutes. GitHub allows 5000 authenticated requests an
    hour and this uses about 60, so you can re-seed freely.

IF IT STOPS PART WAY
    Run reset_lab.py, then run this again. Seeding twice without resetting
    gives you duplicate tickets and your counts stop matching the playbook.

NO EXTRA PACKAGES NEEDED. Standard library only.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.github.com"
HERE = os.path.dirname(os.path.abspath(__file__))

LABELS = [
    ("access", "0E8A16", "Accounts, permissions and shared drives"),
    ("network", "1D76DB", "VPN, wifi and connectivity"),
    ("email", "5319E7", "Mail and calendar"),
    ("hardware", "B60205", "Laptops, printers and peripherals"),
    ("software", "FBCA04", "Applications"),
    ("security", "D93F0B", "Security and leavers"),
    ("infrastructure", "444444", "Servers and platform"),
    ("priority", "E99695", "Flagged urgent by the reporter"),
]


def call(method, path, token, body=None, dry=False):
    url = API + path
    if dry:
        print("  WOULD " + method + " " + url)
        return {"number": 0, "dry": True}

    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "wewin-lab-seeder")

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            remaining = r.headers.get("x-ratelimit-remaining")
            if remaining is not None and int(remaining) < 50:
                print("  rate limit getting low, " + remaining + " left, pausing 60s")
                time.sleep(60)
            raw = r.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        if e.code == 401:
            print("\n401 Unauthorized. The token is wrong, expired, or has no "
                  "access to this repository.")
        elif e.code == 404:
            print("\n404 Not Found. Either the repository name is wrong, or "
                  "the token does not have access to it. A fine grained token "
                  "must list this repository explicitly.")
        elif e.code == 403:
            print("\n403. Usually the rate limit, sometimes a missing scope. "
                  "Check the token has Issues: Read and write.")
        print("  " + method + " " + path)
        print("  " + detail)
        sys.exit(1)
    except urllib.error.URLError as e:
        print("\nCould not reach api.github.com: " + str(e.reason))
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True, help="your GitHub username")
    ap.add_argument("--repo", required=True, help="the empty repo to seed")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0,
                    help="seed only the first N tickets, for a quick test")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token and not args.dry_run:
        print("GITHUB_TOKEN is not set. See the top of this file.")
        sys.exit(1)

    with open(os.path.join(HERE, "tickets_seed.json"), encoding="utf-8") as f:
        tickets = json.load(f)["tickets"]
    if args.limit:
        tickets = tickets[:args.limit]

    base = "/repos/" + args.owner + "/" + args.repo

    if not args.dry_run:
        print("Checking the repository is reachable and empty of issues.")
        existing = call("GET", base + "/issues?state=all&per_page=1", token)
        if isinstance(existing, list) and len(existing) > 0:
            print("\nThis repository already has issues in it.")
            print("Run reset_lab.py first, or use an empty repository.")
            print("Seeding on top of existing issues makes your counts wrong.")
            sys.exit(1)

    print("\nCreating " + str(len(LABELS)) + " labels.")
    for name, colour, desc in LABELS:
        try:
            call("POST", base + "/labels", token,
                 {"name": name, "color": colour, "description": desc},
                 dry=args.dry_run)
        except SystemExit:
            print("  label " + name + " may already exist, continuing")

    print("\nCreating " + str(len(tickets)) + " tickets.")
    made = 0
    for i, t in enumerate(tickets, 1):
        title = t["title"] or "(no subject)"
        payload = {"title": title, "body": t["body"]}
        if t["labels"]:
            payload["labels"] = t["labels"]
        r = call("POST", base + "/issues", token, payload, dry=args.dry_run)
        made += 1
        num = r.get("number", 0)
        if i % 10 == 0 or i == len(tickets):
            print("  " + str(i) + " of " + str(len(tickets))
                  + " (last issue number " + str(num) + ")")
        if not args.dry_run:
            time.sleep(0.7)   # stay well inside the secondary rate limit

    print("\nDone. " + str(made) + " tickets created.")
    print("Open https://github.com/" + args.owner + "/" + args.repo + "/issues")
    print("")
    print("NOTE THE TITLE OF THE FIRST TICKET AND ITS NUMBER. You will use")
    print("them on day one to prove your field mapping landed correctly.")
    print("")
    print("ONE ROW HAS NO TITLE AND ONE HAS NO BODY. That is deliberate. They")
    print("are the two rows that tell you whether your ingestion drops records")
    print("silently, which is the most expensive failure in this whole lab.")


if __name__ == "__main__":
    main()
