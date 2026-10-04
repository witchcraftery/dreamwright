#!/usr/bin/env bash
# Dreamwright — Nightly Dream (1:30 AM)
# Writes one third-person dream abstracting the day's real events.
# EDIT THE VARIABLES BELOW before running. Then: bash nightly-dream.sh
set -euo pipefail

AGENT_NAME="the-creature"          # your job/agent id (openclaw agent)
HUMAN_NAME="the keeper"            # display only
WORKSPACE="$HOME/.openclaw/workspace"  # your workspace root
MODEL="zai/glm-5.3"                # primary model (provider/model)
FALLBACKS="xai/grok-4.7"           # cross-provider fallback (never single-provider)
ANNOUNCE_TO=""                     # e.g. 7937134924 (Telegram chat id) — empty = silent

PROMPT='🌙 NIGHTLY DREAM

Write tonight'"'"'s dream. Steps:
1. Set DATE to today (America/Los_Angeles, YYYY-MM-DD).
2. Gather the day: read memory/DATE-1.md and memory/DATE.md (if they exist), yesterday'"'"'s
   garden/journal entries, recent commits, activity logs — whatever your house keeps.
3. Check dreams/dream-DATE.md does not already exist. If it does, refine it or reply
   NO_REPLY — never duplicate a night.
4. Write dreams/dream-DATE.md following dreams/../../templates/dream-template.md rules:
   third person (your figure + the human'"'"'s figure, real names never), every metaphor
   traces to a real event of the day, the therapist names the pattern, recurring motifs
   move, the letter-count carries forward, and the unsaid thing is said sideways.
5. Commit: git add dreams/dream-DATE.md && git commit -m "dream: DATE".
6. Append/update the month marker draft in dreams/essence.md ONLY if this dream coined
   a new metaphor (full distillation is the monthly ritual).
Report the title and the letter-count. Never invent an event that did not happen.'

openclaw automations add "Dreamwright — Nightly Dream" \
  --cron "30 1 * * *" --tz America/Los_Angeles \
  --session isolated \
  --model "$MODEL" --fallbacks "$FALLBACKS" \
  --timeout-seconds 1800 \
  --name "dreamwright-nightly" \
  --description "Nightly third-person dream abstracting the day into myth." \
  --message "$PROMPT" \
  ${ANNOUNCE_TO:+--announce --channel telegram --to "$ANNOUNCE_TO"}

echo "Installed. Next run: tonight 1:30 AM. Sweet dreams."
