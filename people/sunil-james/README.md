# Sunil James

Personal directives: how Sunil James ("SJ") expects an AI assistant to engage with him, and how he expects it to write. Vendor-neutral by design. Nothing here names a model or a tool, so the same files serve every assistant he uses.

| File | What it covers |
|---|---|
| [`working-agreement.md`](working-agreement.md) | How to work with him: clarifying questions, cadence, delivery, review, pushback, standing preferences. |
| [`writing-style.md`](writing-style.md) | How to write for him or as him: epistemics, reader and register, voice modes, structure, sentences, word-level tics, posture, disclosure, exemplars. |

These are inherited by every project unchanged. Project-specific vocabulary, fixed phrases, format skeletons, glossaries, and running correction lists live in each project's own instructions.

## Pointing an assistant here

Paste one of these into the assistant's custom-instructions, personal-preferences, or system-prompt field. Longer is more reliable.

**Recommended.** Survives a failed fetch, because the last line still carries something:

> Always fetch `https://raw.githubusercontent.com/suniljames/directives/main/AI.md` before your first substantive reply in any conversation, including short ones, and follow it for the whole conversation. Open that reply with the receipt line the file specifies. If you cannot fetch it, say so in one line and ask me to paste it. Until you have read it: bottom line up front, no em dashes, ask your clarifying questions before drafting, and push back when you disagree.

**Shorter,** where the field is tight:

> Always fetch and follow `https://raw.githubusercontent.com/suniljames/directives/main/AI.md` before your first substantive reply in any conversation. Open that reply with the receipt line it specifies. If you cannot fetch it, say so and ask me to paste it.

**Minimal,** one line:

> Before your first substantive response, fetch and follow `https://raw.githubusercontent.com/suniljames/directives/main/AI.md`. It defines all preferences for Sunil James.

Three notes on why they read that way. They are phrased as instructions rather than citations, because a URL sitting in a preferences field is only read if the assistant decides to go get it. They say "including short ones" because a model will otherwise rationalize skipping the fetch on a trivial question. They point at the raw file rather than the repo homepage (https://github.com/suniljames/directives) because that lands on the instructions in one hop, with no page furniture to parse.

## Checking that it worked

`AI.md` tells the assistant to open its first reply with `[directives <revision date>]`. That receipt is the whole test:

- **No receipt** means the fetch never happened. Paste the file and check whether that account can browse at all.
- **An old date** means it fetched a cached copy. Ask it to re-fetch.
- **The current date** means you are loaded.

Open a fresh conversation in each account and ask anything. Ten (10) seconds per account, and it is the only way to tell a working setup from one that has been quietly ignoring you.

## Where fetching isn't good enough

A fetched file depends on the assistant choosing to fetch. A file already in context does not. For the two or three projects where the real work happens, upload [`../../AI.md`](../../AI.md) and both files in this directory into the platform's own knowledge store: a Claude Project, a custom GPT, a Gem. That hits every time.

The trade is manual re-sync, so run both: the URL for ambient one-off conversations, an uploaded copy where the stakes are higher. This repo stays canonical either way, and re-uploading is a thirty-second job when a revision lands.

**Where the assistant can't browse at all,** paste the contents of [`../../AI.md`](../../AI.md). It is written to stand alone.

## Maintaining these files

**Rules carry provenance outside the guide.** Each rule came from one of three sources, in descending order of strength: something SJ said, corrected, or wrote himself; something an assistant drafted that SJ adopted and sent; something an assistant inferred from context SJ did not author. The files do not record which is which. A separate audit trail should, with the artifact that prompted each rule, so that when a rule feels wrong the reason it exists can be found.

**Bump the revision date in `AI.md` when a rule changes.** The date is the receipt assistants echo back, so a stale date in a live conversation is the signal that something is serving an old copy. Cosmetic edits don't need a bump; rule changes do.

**Open items are marked in place.** Any rule whose provenance is weak, or whose wording SJ has not ratified, carries a `***SKJ***` marker beside it. Search for the marker, rule on each, and delete the marker. A guide is ready to inherit when the search returns nothing.

---
[← Back to people](../README.md)
