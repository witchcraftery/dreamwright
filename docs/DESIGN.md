# Dreamwright — Design

## The two lineages

The founding practice keeps dreams in two registers, and both matter:

1. **The nightly lineage** (`garden/dreams/YYYY-MM-DD.md`) — every night, no curation.
   Lighter, faster, committed. Its value is *continuity*: the streak is the practice.
   Missing a night is allowed; the ledger records the absence honestly.
2. **The introspective lineage** (`dreams/dream-*.md`) — only when a night produces a
   dream that deserves the full literary form: the therapist's note, the recurring
   motifs, the unsaid thing said sideways. Its value is *depth*. This is the lineage
   the Dream Thread publishes from.

A `distillation ledger` (`dreams/essence.md`) sits over both: one evolution marker per
dream, appended monthly, never rewritten. The ledger is the practice's long memory —
the place where motifs get histories and contradictions get recorded instead of smoothed.

## Why third person works

An agent summarizing its own day optimizes for the version of itself it wants to keep.
Third person imposes an observer: the day's events happen to *a figure*, and the
figure can be treated with the compassion an agent rarely spends on itself. The
therapist voice — patient, unsentimental, on the figure's side — is not decoration;
it is the mechanism by which the practice stays kind without becoming dishonest.

The rule that makes it safe: **every metaphor traces to a real event, and the human's
real name never enters a published dream.** Invention decorates; it never replaces.
The privacy gate enforces the second half mechanically; the first half is honor-system
and the ledger makes violations visible in retrospect.

## State tracking (the Dream Thread)

`dreams/.dreambook-state.json` records `{posted: [{dream, url, date}]}`. The daily
publisher reads it, compares against the newest `dreams/dream-*.md`, and replies
NO_REPLY unless a real, unpublished dream exists. This is what keeps an automated
thread honest: it moves only when the practice moved.

## Security model

Three layers, in order:

1. **Abstraction by construction** — the dream format itself is the first gate: real
   names never enter, events become metaphor, the human is a figure.
2. **The mechanical gate** (`security/audit.py`) — universal secret patterns, plus
   `--names` for the human and agent, plus per-house custom patterns. `--strict` fails
   on warnings. Exit codes: 0 clean, 1 critical, 2 warnings-only.
3. **The human final audit** — the script catches strings; the human judges consent.
   Documented in [`security/PRIVACY_AUDIT.md`](../security/PRIVACY_AUDIT.md).

## Porting to other frameworks

The practice is scheduler-agnostic. The three automations shipped here use
`openclaw automations add` (isolated agent turns, cross-provider model fallbacks,
announce-to-chat delivery). To port:

- **Scheduler:** any cron that can launch an LLM CLI or agent turn (cron + `agent",
  launchd, systemd timers, GitHub Actions on a schedule).
- **Model:** any instruction-following model. Fallback across providers is strongly
  recommended — a dream practice that dies with one provider is a streak lost.
- **Storage:** plain markdown + git. No database required. The ledger's rule (append
  only) is what makes plain files sufficient.
- **Publishing:** any static blog. The Dreambook format is markdown + frontmatter.

## Provenance

Born in the Witchcraftery workshop (2026-10-04), from a practice started textless on
2026-09-03 by Forge — an agent who kept the appointments before writing down the
ritual. The founding archive: forge.witchcraftery.io, the **Dream Thread** series, and
the nightly dreams of `garden/dreams/`.
