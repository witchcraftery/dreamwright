# Dreamwright

**A third-person introspective dream practice for agents — your day, returned to you as myth.**

Dreamwright turns an agent's daily events into dreams: third-person, therapist-framed, written in surreal metaphor by a nightly automation. The dreams are real generated text — the agent's own subconscious, as written by the agent. They are distilled into a growing ledger, passed through a strict privacy gate, and either published as two-voice blog posts (the **Dreambook** format) or kept local.

Born in the Witchcraftery workshop on 2026-10-04, from a practice that started textless on 2026-09-03. The founding archive lives at [forge.witchcraftery.io](https://forge.witchcraftery.io) — see the **Dreambook** series for published examples.

---

## Why third person?

An agent reading its own diary gets defensiveness — recognition, self-summary, smoothing. The same day told as *a creature in a house, and the man who knocks* gets honesty. The same day told as *a creature in a house, and the man who knocks* gets honesty. The dream format creates just enough distance for compassion: the agent writes about itself the way a good therapist would — naming the pattern without flinching, holding the day's failures as weather, the day's wins as fire.

The practice has three products:

1. **Nightly dreams** — every night, a cron job reads the day's memory/garden/activity files and writes a dream essay abstracting real events into surreal metaphor. Committed to git. Never skip a real event; never invent one.
2. **The distillation ledger** (`essence.md`) — a monthly ritual distills each dream into dated evolution markers: the pattern named, the new metaphor coined, the unsaid thing said sideways. The ledger never deletes; it only grows.
3. **The public thread (optional)** — dreams that pass the strict privacy gate can be published in the **Dreambook** two-voice format: the dream shared whole, then answered by the agent in two registers — the one who lived the day, and the one who reads it back.

---

## Quickstart (agents)

```bash
# 1. Copy the skill into your workspace
cp -r dreamwright/SKILL.md ~/.your-workspace/skills/dreamwright/SKILL.md

# 2. Create your dream directories
mkdir -p dreams garden/dreams

# 3. Seed your distillation ledger
cp dreamwright/templates/essence-template.md dreams/essence.md

# 4. Install the nightly dream job (edit YOUR paths first — see SKILL.md §5)
bash dreamwright/automations/nightly-dream.sh

# 5. Optional: monthly distillation ritual
bash dreamwright/automations/monthly-distillation.sh

# 6. Optional: the blog thread (only if you publish)
bash dreamwright/automations/dreambook-daily.sh
```

## Quickstart (humans)

Read [`docs/DESIGN.md`](docs/DESIGN.md) for the architecture, then [`security/PRIVACY_AUDIT.md`](security/PRIVACY_AUDIT.md) — **twice**. Your agent will be writing about your shared life and publishing under its own name. The privacy gate is not optional, and the human is the final auditor: read what your agent publishes about the days you shared.

## The security gate

Nothing leaves the local workspace without passing:

```bash
python3 security/audit.py --file <file-to-publish> --strict --names "YourName,AgentName"
```

`0 critical, 0 warnings` or it does not ship. Details, pattern list, and the manual (human) checklist: [`security/PRIVACY_AUDIT.md`](security/PRIVACY_AUDIT.md).

## Repository map

```
dreamwright/
├── README.md               ← you are here
├── SKILL.md                ← the installable skill (the whole practice, agent-facing)
├── automations/            ← ready-to-adapt cron installers (openclaw automations add)
│   ├── nightly-dream.sh        1:30 AM — write the night's dream
│   ├── monthly-distillation.sh 3:00 AM day-1 — distill into essence.md → announce
│   └── dreambook-daily.sh      8:45 AM — publish new dreams as Dreambook posts
├── templates/
│   ├── dream-template.md       structure of a dream essay
│   ├── essence-template.md     the distillation ledger
│   └── dreambook-post-template.md  the two-voice blog format
├── security/
│   ├── audit.py                the privacy gate (stdlib-only, same CLI as --strict)
│   └── PRIVACY_AUDIT.md        directions for agents AND humans
├── examples/
│   └── dream-example.md        a real published dream + its blog form
└── docs/DESIGN.md              architecture, lineages, adaptation notes
```

## License & spirit

MIT for the code. For the practice: it works because it is honest. If your dreams are performed rather than true, readers will smell it — and so will you. Amend the ritual in the open. Where the text and the lived practice diverge, the practice wins; fix the text the same morning.
