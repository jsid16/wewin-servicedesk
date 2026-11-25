""" 
Puts the lab back to the state it was in just after seeding.

WHY THIS EXISTS
    You will run the demo more than once. After a run, tickets are closed,
    comments are posted and labels have been added. This clears all of that so
    the next run starts from the same place.

    It is also what you run if seeding stopped part way and you need to start
    again.

WHAT IT DOES
    GitHub does not let the API delete an issue. So reset has two modes.

    --mode clean    (default, and what you want before a demo)
        Reopens every closed issue, deletes every comment the bot posted,
        and removes the labels this lab adds (resolved, needs-triage,
        auto-answered). Original labels like access and network are left
        alone because they came with the seed.
        Takes about a minute. Your issue numbers stay the same.

    --mode wipe
        Closes and locks every issue so the repo reads as empty. Issue
        numbers are NOT reused, so your next seed starts at a higher number.
        Use this only if you are abandoning the repo.

    The honest third option, and the fastest: delete the repository in
    GitHub settings and make a new empty one, then seed again. Thirty
    seconds, and you get issue numbers starting at 1 again. Do that if
    anything looks tangled.

HOW TO RUN IT
        python reset_lab.py --owner YOURNAME --repo wewin-servicedesk --dry-run
        python reset_lab.py --owner YOURNAME --repo wewin-servicedesk

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

# Labels this lab adds at run time. Seed labels are not touched.
RUN_LABELS = ["resolved", "needs-triage", "auto-answered", "deflected"]


def call(method, path, token, body=None, dry=False, quiet=False):
    url = path if path.startswith("http") else API + path
    if dry:
        if not quiet:
            print("  WOULD " + method + " " + url)
        return None

    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "wewin-lab-reset")

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8")
            link = r.headers.get("Link", "")
            parsed = json.loads(raw) if raw else {}
            return {"data": parsed, "link": link}
    except urllib.error.HTTPError as e:
        if e.code == 404 and method == "DELETE":
            return {"data": {}, "link": ""}   # already gone, fine
        detail = e.read().decode("utf-8", "replace")[:300]
        print("\n" + str(e.code) + " on " + method + " " + path)
        print("  " + detail)
        sys.exit(1)
    except urllib.error.URLError as e:
        print("\nCould not reach api.github.com: " + str(e.reason))
        sys.exit(1)


def next_page(link_header):
    """GitHub paginates with a Link header. This is the same Next Link
    strategy the ServiceNow connector uses, which is why it is worth
    reading rather than skipping."""
    for part in link_header.split(","):
        bits = part.split(";")
        if len(bits) < 2:
            continue
        if 'rel="next"' in bits[1]:
            return bits[0].strip().strip("<>")
    return None


def all_issues(base, token, dry):
    """Every issue, following pagination to the end. The whole point of the
    Link header is that stopping after one page silently gives you 30."""
    if dry:
        print("  WOULD page through " + base + "/issues?state=all")
        return []
    out, url = [], API + base + "/issues?state=all&per_page=100"
    while url:
        r = call("GET", url, token)
        batch = r["data"]
        if not isinstance(batch, list):
            break
        out.extend(batch)
        url = next_page(r["link"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--mode", choices=["clean", "wipe"], default="clean")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token and not args.dry_run:
        print("GITHUB_TOKEN is not set.")
        sys.exit(1)

    base = "/repos/" + args.owner + "/" + args.repo
    issues = all_issues(base, token, args.dry_run)
    issues = [i for i in issues if "pull_request" not in i]

    print("Found " + str(len(issues)) + " issues.")
    if args.dry_run:
        print("Dry run. Nothing was changed.")
        return

    if args.mode == "wipe":
        for i, iss in enumerate(issues, 1):
            n = iss["number"]
            call("PATCH", base + "/issues/" + str(n), token, {"state": "closed"})
            call("PUT", base + "/issues/" + str(n) + "/lock", token,
                 {"lock_reason": "resolved"})
            if i % 10 == 0:
                print("  locked " + str(i) + " of " + str(len(issues)))
            time.sleep(0.5)
        print("\nWiped. Issue numbers will NOT restart. For a clean numbering,")
        print("delete the repository and seed a new one.")
        return

    reopened = comments_deleted = labels_removed = 0

    for i, iss in enumerate(issues, 1):
        n = iss["number"]

        if iss.get("state") == "closed":
            call("PATCH", base + "/issues/" + str(n), token, {"state": "open"})
            reopened += 1

        if iss.get("locked"):
            call("DELETE", base + "/issues/" + str(n) + "/lock", token)

        if iss.get("comments", 0) > 0:
            r = call("GET", base + "/issues/" + str(n) + "/comments?per_page=100", token)
            for c in r["data"]:
                call("DELETE", base + "/issues/comments/" + str(c["id"]), token)
                comments_deleted += 1
                time.sleep(0.3)

        for lbl in [l["name"] for l in iss.get("labels", [])]:
            if lbl in RUN_LABELS:
                call("DELETE", base + "/issues/" + str(n) + "/labels/" + lbl, token)
                labels_removed += 1

        if i % 10 == 0 or i == len(issues):
            print("  processed " + str(i) + " of " + str(len(issues)))
        time.sleep(0.4)

    print("")
    print("Reset complete.")
    print("  reopened          " + str(reopened))
    print("  comments deleted  " + str(comments_deleted))
    print("  run labels removed " + str(labels_removed))
    print("")
    print("ONE THING THE RESET CANNOT UNDO: your Aisera tenant still holds the")
    print("tickets it ingested earlier, with their old state. Before the next")
    print("demo, re-run your data source so the tenant matches the repo again.")
    print("A demo where the tenant and the repo disagree is worse than no demo,")
    print("because you will not know which of the two is wrong.")


if __name__ == "__main__":
    main()
