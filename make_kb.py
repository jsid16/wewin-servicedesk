""" 
Generates the 7 knowledge base articles, the index page and the Jekyll config
into 02_Knowledge_Base.

Run this only if you want to change the articles. The committed files are what
the 51 seeded tickets were written against, so changing an article may change
which tickets deflect.

    python make_kb.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "02_Knowledge_Base"))

CONFIG = """theme: jekyll-theme-minimal
title: WEWIN IT Knowledge Base
description: Self service articles for WEWIN Corp employees
"""

ARTICLES = {}

ARTICLES["password-reset"] = ("""# Resetting your WEWIN password

**Applies to:** all WEWIN accounts | **Owner:** IT Service Desk | **Reviewed:** January 2026

Use this article if you have forgotten your password, your password has
expired, or your account has locked after too many failed attempts.

## If your account is locked

WEWIN locks an account after five failed sign in attempts. The lock clears by
itself after 30 minutes, so if you can wait, you do not need to do anything.

To clear it immediately:

1. Go to **reset.wewin.com** from any device, including your phone.
2. Enter your WEWIN email address.
3. Choose **Unlock my account**.
4. Approve the notification on your registered phone.
5. The lock clears within a minute. Your password has not changed.

## If you have forgotten your password

1. Go to **reset.wewin.com**.
2. Enter your WEWIN email address.
3. Choose **Reset my password**.
4. Approve the notification on your registered phone.
5. Choose a new password. It must be at least 14 characters and cannot be one
   of your last ten passwords.

## If your password has expired

WEWIN passwords expire every 180 days. You get a warning 14 days before. If it
expires while you are signed in, you stay signed in until you lock the screen
or restart, so reset it before you walk away.

The process is the same as a forgotten password, above.

## If the reset email or link does not work

The reset link is valid for 15 minutes and can only be used once. If you
requested several resets, only the newest link works. Go back to
reset.wewin.com and start again rather than clicking an older email.

## If you have no phone enrolled

You cannot self serve. Contact the IT Service Desk on extension 4400 from a
WEWIN desk phone, or ask your manager to raise a ticket on your behalf. For
security reasons this cannot be done over email.

## After you reset

Your new password reaches other systems within about 15 minutes. If your email
on your phone starts asking for a password after a reset, that is expected.
Enter the new one.
""", "Locked out, forgotten password, expired password")

ARTICLES["vpn-guide"] = ("""# Connecting to the WEWIN VPN

**Applies to:** WEWIN laptops | **Owner:** Network Team | **Reviewed:** January 2026

The VPN gives you access to internal systems when you are not in a WEWIN
office. You do not need it for email, Teams or anything on the web.

## First time setup on a new laptop

New laptops ship with the VPN client already installed. If yours does not have
it:

1. Open **Company Portal** from the Start menu.
2. Search for **WEWIN VPN**.
3. Click **Install**. It takes about three minutes.
4. Restart the laptop. The client does not work properly until you do.
5. Open **WEWIN VPN** from the Start menu. The server address fills in by
   itself. If it is blank, enter **vpn.wewin.com**.

You do not need a separate VPN password. Sign in with your WEWIN account.

## If the VPN will not connect

Work through these in order. Most failures are the first one.

1. **Check you are actually on a network.** Open a web page first. Hotel and
   airport wifi often needs you to accept terms in a browser before anything
   else works, and the VPN cannot do that for you.
2. **Restart the client**, not just the connection. Quit it from the system
   tray and reopen it.
3. **Check the clock.** If your laptop's time is more than five minutes out,
   the connection is rejected with a generic error. This is the cause people
   never guess.
4. **Try the backup gateway.** In the client, change the server to
   **vpn2.wewin.com**. If that works, the main gateway has a problem and you
   should say so when you raise a ticket.
5. **Restart the laptop.**

## If it connects then drops after a few seconds

This is almost always a second VPN or a network filtering tool installed on
the same machine, often from a previous employer or a personal subscription.
Two VPN clients cannot run at once. Uninstall the other one.

## If it says "cannot reach the gateway"

Your network is blocking the connection. This is common on guest wifi,
conference wifi and some home routers with strict firewalls. Test by
connecting your laptop to your phone's hotspot. If the VPN works on the
hotspot, the network you were on is the problem, not the VPN.

## What to include when you raise a ticket

The exact error text, whether it works on a phone hotspot, and whether you
have ever connected successfully from this location before.
""", "Cannot connect, drops out, new laptop setup")

ARTICLES["outlook-sync"] = ("""# Outlook is not receiving new mail

**Applies to:** Outlook on WEWIN laptops | **Owner:** Messaging Team | **Reviewed:** January 2026

Use this if Outlook has stopped updating, shows Disconnected, or is showing
older mail than webmail does.

## First, check whether it is only Outlook

Open **mail.wewin.com** in a browser and sign in. If your new mail is there,
the mail itself is fine and the problem is the Outlook client on your machine.
If the mail is missing there too, it was never delivered, and this article
will not help.

This one check saves most of the time spent on this problem.

## If Outlook says Disconnected or Working Offline

1. Look at the bottom right corner of Outlook for the status.
2. If it says **Working Offline**, go to the **Send / Receive** tab and click
   **Work Offline** to switch it back off. This gets switched on by accident
   more than any other setting in Outlook.
3. If it says **Disconnected**, close Outlook completely and reopen it. Wait
   two minutes before deciding it has not worked.

## If it stays disconnected

1. Check whether other things reach the internet. If nothing does, fix that
   first.
2. If you are off site, check the VPN. Outlook does not need the VPN, but some
   home networks block the ports it uses, and the VPN works around that.
3. Restart the laptop. For this specific fault it genuinely does work often
   enough to be worth doing before raising a ticket.

## If mail arrives but is hours late

Your mailbox may be full. In Outlook go to **File**. The bar at the top shows
how much of your quota is used. Above 95 percent, delivery slows and then
stops. Empty **Deleted Items** and the **Junk** folder, which most people
never do, and which is usually enough.

## If the calendar is out of date but mail is fine

Calendar and mail sync separately. Close Outlook, reopen it, and leave it for
five minutes before judging.

## What to include when you raise a ticket

Whether webmail shows the missing mail, the exact status text at the bottom
right of Outlook, and the time the last message arrived.
""", "Not receiving mail, disconnected, sync problems")

ARTICLES["mobile-email"] = ("""# Setting up WEWIN email on a phone

**Applies to:** personal and WEWIN phones | **Owner:** Messaging Team | **Reviewed:** January 2026

## Before you start

Your phone must have a screen lock with a PIN, pattern or biometric. WEWIN
mail will not set up on a phone without one, and the error it gives does not
explain that.

## Setting it up

1. Install **Microsoft Outlook** from the App Store or Play Store. Use the
   Outlook app rather than the phone's built in mail app. The built in apps
   work but lose calendar features and are the cause of most of the problems
   in the next section.
2. Open it and enter your full WEWIN email address.
3. Sign in with your WEWIN password.
4. Approve the prompt on your other device.
5. Accept the device policy when it asks. This lets WEWIN wipe **only** the
   work mail if the phone is lost. It does not give WEWIN access to your
   photos, messages or anything else personal, and that is worth knowing
   before you decline it.

## If it keeps asking for your password

This is the most common problem and it has three causes.

1. **You recently reset your WEWIN password.** The phone still has the old
   one. Delete the account from Outlook and add it again. Changing the
   password in the app is not enough.
2. **You are using the phone's built in mail app.** It does not handle the
   WEWIN sign in properly. Install the Outlook app instead.
3. **Your account is locked.** See the password reset article.

## If mail arrives late or only when you open the app

Check that background refresh is enabled for Outlook in your phone's settings,
and that battery saving is not restricting it. Aggressive battery settings,
which are on by default on many Android phones, stop mail arriving until you
open the app.

## Leaving WEWIN or changing phones

Remove the account from the Outlook app before you wipe or hand over the
phone. If you cannot, tell the IT Service Desk so the work data can be removed
remotely.
""", "Phone setup, password prompts, late mail")

ARTICLES["printer-setup"] = ("""# Adding a printer and fixing a printer that shows offline

**Applies to:** WEWIN laptops | **Owner:** End User Computing | **Reviewed:** January 2026

## Adding a printer

WEWIN printers are named by site, floor and area, for example
**LON-03-KITCHEN** or **LON-02-FINANCE**.

1. Open **Printers and scanners** from the Start menu.
2. Click **Add a printer or scanner**, then **Add a printer by name**.
3. Type `\\\\print.wewin.com\\` followed by the printer name.
4. Windows installs the driver by itself. This takes about a minute.

If you do not know the printer name, it is on a label on the front of the
printer. If the label has gone, print a configuration page from the printer's
own menu, which shows its network name.

## If a printer shows offline but other people can print to it

The printer is fine and your machine's copy of it has gone stale. This is the
most common printer ticket WEWIN receives.

1. Open **Printers and scanners**.
2. Click the printer, then **Remove**.
3. Add it again using the steps above.

That fixes it the large majority of the time. If it comes back within a day,
raise a ticket and say that removing and re-adding fixed it temporarily, which
points at a different cause.

## If nothing prints and the queue fills up

1. In **Printers and scanners**, open the printer and click **Open queue**.
2. Cancel every document in the list, including ones that say Deleting.
3. If documents will not cancel, restart the laptop. The print service can
   only be fully cleared by a restart.

## If printing is very slow

Printing a large PDF or a slide deck with photographs can take several
minutes. Before raising a ticket, test with a one page text document. If that
prints quickly, the printer is working and the file is the issue.

## Double sided printing is greyed out

Not every WEWIN printer has a duplex unit. If the option is missing, that
printer cannot print double sided. The nearest duplex capable printer is
usually the main one on each floor.
""", "Adding a printer, offline, queue stuck, duplex")

ARTICLES["wifi-troubleshooting"] = ("""# WEWIN wifi, including guest access

**Applies to:** WEWIN offices | **Owner:** Network Team | **Reviewed:** January 2026

## The networks

**WEWIN-CORP** is for WEWIN laptops and phones. It signs you in
automatically with your WEWIN account. You should never need to type a
password for it, and if you are being asked for one, your device certificate
has expired and you should raise a ticket.

**WEWIN-GUEST** is for visitors and personal devices. It needs a code, which
reception issues and which lasts for one day.

There is no other network. If your device shows something that looks like a
WEWIN network and is not one of these two, do not connect to it and tell
Information Security.

## If the connection drops repeatedly in one room

Meeting rooms with heavy glass and rooms on the edge of a floor have known
weak coverage. Before raising a ticket, check whether it happens elsewhere on
the same floor. A ticket that says "drops in MR4, fine everywhere else" gets
fixed. A ticket that says "wifi is bad" does not.

## If you cannot see the guest network

Guest wifi is not broadcast in every part of every building, and it is
deliberately off in some secure areas. Try near reception. If it is visible
there but not where your visitor is sitting, that is the expected behaviour
rather than a fault.

## If you connect but nothing loads

This is usually a sign in page that has not appeared. Open a browser and go to
any plain http site. The sign in page should appear. Phones often suppress it,
so try a laptop.

## If a visitor's code does not work

Codes expire at midnight on the day they are issued and are single device.
Reception can issue another one. Codes are not transferable between visitors,
which is why one that worked for a colleague's guest will not work for yours.

## Before raising a wifi ticket

Include the building and room, whether it affects one device or several, and
whether a phone on mobile data in the same spot works normally.
""", "Dropping connection, guest wifi, cannot connect")

ARTICLES["shared-drive"] = ("""# Shared drive problems

**Applies to:** WEWIN laptops | **Owner:** End User Computing | **Reviewed:** January 2026

This article covers drives that do not appear and drives that disappear. If
you need access to a folder you have never had access to before, that is an
access request and not a fault. Raise it through the service portal, because
it needs approval from the folder's owner and nothing in this article will
grant it.

## If the S drive disappears every time you restart

The mapping is not set to reconnect. This is the most common shared drive
ticket.

1. Open **File Explorer**.
2. Right click **This PC** and choose **Map network drive**.
3. Drive letter: **S**
4. Folder: `\\\\files.wewin.com\\shared`
5. **Tick "Reconnect at sign-in".** This is the box that was missed.
6. Click **Finish**.

## If the drive is there but a folder inside it says access denied

You do not have permission to that folder. This is not a fault, even if you
had access last week.

Permissions are reviewed every six months and access that has not been used
for 90 days is removed automatically. If you used to have access and no longer
do, it was most likely reclaimed during a review.

Request it again through the service portal. Say which folder and why you need
it. The folder owner approves it, usually within a day.

## If the drive is slow when you are off site

Shared drives are slow over the VPN, especially with large files. This is
expected. For files you work on regularly away from the office, use SharePoint
instead, which is built for it.

## If you deleted a file by mistake

Do not panic and do not create a replacement file with the same name, which
makes recovery harder.

1. Right click the folder the file was in.
2. Choose **Properties**, then **Previous Versions**.
3. Pick a version from before the deletion and open it.
4. Copy the file back out.

Snapshots are kept for 30 days. Beyond that, raise a ticket the same day you
notice, because the backup window is shorter than people expect.

## If you need access to a new folder

Service portal, not this article. It needs the owner's approval.
""", "Drive not mapping, access denied, deleted file")


def main():
    os.makedirs(OUT, exist_ok=True)

    with open(os.path.join(OUT, "_config.yml"), "w", encoding="utf-8") as f:
        f.write(CONFIG)

    index = ["# WEWIN IT Knowledge Base", "",
             "Self service articles for WEWIN Corp employees. If you cannot "
             "find an answer here, raise a ticket through the service portal.",
             "", "## Articles", ""]

    for slug, (body, blurb) in ARTICLES.items():
        with open(os.path.join(OUT, slug + ".md"), "w", encoding="utf-8") as f:
            f.write(body)
        title = body.split("\n", 1)[0].lstrip("# ").strip()
        index.append("- [" + title + "](" + slug + ") - " + blurb)

    index += [
        "",
        "## Contact",
        "",
        "- IT Service Desk: extension 4400",
        "- Information Security: security@wewin.example",
        "",
        "---",
        "",
        "> **Note for trainers.** This index page is what makes a crawl at "
        "Max Depth 2 work. The crawler reads this page, follows the seven "
        "links, and ingests each article. If you delete this file, set Max "
        "Depth to 1 and add every article URL as its own starting URL.",
        "",
        "> WEWIN Corp is fictional and so is everything in these articles. "
        "This repository is public, so do not replace them with any real "
        "content.",
        "",
    ]

    with open(os.path.join(OUT, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index))

    print("wrote " + str(len(ARTICLES)) + " articles, index.md and _config.yml")
    print("into " + OUT)
    for slug in ARTICLES:
        print("  " + slug + ".md")


if __name__ == "__main__":
    main()
