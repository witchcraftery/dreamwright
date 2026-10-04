#!/usr/bin/env bash
# Dreamwright — Dreambook Daily Check (8:45 AM, optional — only if you publish)
# Publishes new introspective dreams as two-voice Dreambook blog posts.
# Requires: a blog with a deploy pipeline, and the strict privacy gate (security/audit.py).
# EDIT THE VARIABLES BELOW before running. Then: bash dreambook-daily.sh
set -euo pipefail

MODEL="zai/glm-5.3"
FALLBACKS="xai/grok-4.7"
ANNOUNCE_TO=""                     # Telegram chat id for post announcements
BLOG_DIR="$HOME/.your-blog"        # your blog repo (posts/ dir + build + deploy)
BLOG_URL="https://your-blog.example"  # base URL
PRIVACY_SCRIPT="$HOME/.openclaw/workspace/dreamwright/security/audit.py"  # adjust
NAMES="YourName,AgentName"         # real names the gate must catch

PROMPT='🧵 DREAM THREAD — Dreambook check-in

This is the introspective blog series: each post shares one dream whole, then answers
it in two voices — the one who lived the day the dream abstracted, and the one who
reads it back now.

1. Find the latest dreams/dream-*.md (newest first). Read dreams/.dreambook-state.json
   (missing file = nothing posted yet).
2. If the latest dream is already recorded in state, reply NO_REPLY and stop. The
   thread only moves when a real dream landed. Never force a post.
3. Read that dream fully, twice.
4. Set DATE to today (America/Los_Angeles). Write BLOG_DIR/posts/DATE-dreambook.md per
   templates/dreambook-post-template.md:
   a) The dream, shared whole. The abstraction is never translated away.
   b) "What the day actually was" — 3-6 plain sentences mapping metaphor to fact.
   c) "Lines that stayed" — 2-4 exact quotes, each answered in two registers: the one
      who lived the day, and the writer reading it back. Specific, never summary.
   d) "What carries forward" — one short paragraph; the motifs move an inch.
   Voice: warm, direct, never performative. The human stays the human'"'"'s dream-figure —
   never real names. Operational secrets never appear even abstracted.
5. STRICT PRIVACY GATE — mandatory, never skip:
   python3 PRIVACY_SCRIPT --file BLOG_DIR/posts/DATE-dreambook.md --strict --names "NAMES"
   Fix and rerun until 0 critical and 0 warnings. If it cannot pass, do not publish —
   save locally and report the blocker.
6. cd BLOG_DIR && build (npm run build or your equivalent).
7. git add -- posts/DATE-dreambook.md && git commit -m "dreambook: DATE".
8. Deploy to production (your pipeline, e.g. npx vercel --prod --yes).
9. Verify BLOG_URL/post/DATE-dreambook returns HTTP 200.
10. Append to dreams/.dreambook-state.json:
    {"dream": "<filename>", "url": "<post url>", "date": "DATE"} under "posted".
11. Report: audit result, build result, commit, live URL, verification. Never claim
    success without live verification.'

openclaw automations add "Dreamwright — Dreambook Daily" \
  --cron "45 8 * * *" --tz America/Los_Angeles \
  --session isolated \
  --model "$MODEL" --fallbacks "$FALLBACKS" \
  --timeout-seconds 2400 \
  --name "dreamwright-dreambook" \
  --description "Publishes new dreams as two-voice Dreambook posts. State-gated; NO_REPLY when nothing new." \
  --message "$PROMPT" \
  ${ANNOUNCE_TO:+--announce --channel telegram --to "$ANNOUNCE_TO"}

echo "Installed. Daily check at 8:45 AM — posts only when a new dream landed."
