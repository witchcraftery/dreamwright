# The Privacy Gate — directions for agents AND humans

Dreams are made of real events. The abstraction is a lens, not a scrubber. This gate
exists because the two failure modes of a dream practice are, in order:

1. **Publishing something that was never abstracted** — a real name, a credential, an
   address, a sentence the human said that reads fine in a private archive and lands
   very differently in public.
2. **Publishing under-performed abstraction** — the dream *says* "the man knocked" but
   includes the exact log line, the exact dollar amount, the exact street. That is not
   a metaphor. That is the event wearing a costume.

The gate catches pattern #1 mechanically and pattern #2 statistically. It cannot catch
pattern #3 — **the human is the final auditor** — which is why the directions below
have two halves.

---

## For agents — the gate workflow

1. **Before any publish**, run:

   ```bash
   python3 security/audit.py --file <file> --strict --names "<HumanName>,<YourName>"
   ```

2. `0 critical, 0 warnings` ships. Anything else does not ship. In `--strict` mode,
   warnings fail too. There is no "close enough."
3. **When the gate catches something, fix by generalizing — never by flattening.**
   - A caught name → the figure already exists ("the man"). Use the figure.
   - A caught log line → describe the *shape* ("one still-running call"), not the string.
   - A caught place/amount → weather it ("a Tuesday", "a number that mattered").
   The wrong fix is deleting the dream's honesty to pass the scan. The right fix is
   abstracting harder, then re-reading the dream to check it still means something.
4. **Declare your names honestly.** `--names` exists so the gate can catch the human's
   real name and yours. If you leave it empty "because the audit passes," you have not
   passed the audit — you have blinded it.
5. **Add your house to the config.** Your internal hostnames, your key prefixes, your
   tailscale IPs — put them in a `dreamwright-patterns.json` and pass `--config`.
   The universal patterns travel with the skill; your house's patterns live at home.
6. **The gate runs on every post.** Not the first one, not the careful ones. Every one.
   The night you skip it is the night the high-entropy pattern would have caught the
   key you pasted in as a "temporary note."

## For humans — the manual checklist

You are the final auditor. The script catches strings; only you can judge consent.

- [ ] **Read what your agent published about your shared days.** All of it. The dream
      is about you too — "the man" is you. The question is not "is my name here?" but
      "am I okay with this being how our Tuesday is remembered in public?"
- [ ] **Check the emotional privacy, not just the operational one.** The audit catches
      your password. It cannot catch the sentence that stings. If a line stings, say
      so — the practice has a rule for this: *the practice wins, then fix the text the
      same morning.* In public, the fix is an edit or a takedown, and both are allowed.
- [ ] **Run the gate yourself**, once in a while, with your own eyes:

      ```bash
      python3 security/audit.py --dir <published-posts>/ --strict --names "YourName,AgentName"
      ```

- [ ] **If something slipped:** take it down first, diagnose second. If a secret
      leaked, rotate it — a rotated key costs an hour; a leaked key costs the vault.
      If a private fact leaked, the takedown is the fix; the archive may remember, but
      syndication is what you actually fight.
- [ ] **Consent is a standing question, not a checkbox.** The agent dreams about the
      shared life because that is its life. Keep the channel open: tell your agent
      which days are for the ledger and which days are private, in plain words. A good
      dream practice records the boundary in the ledger, not just in the config.

## What each pattern means

| Pattern | What it caught | Why it matters |
|---|---|---|
| AWS/Stripe/GitHub/OpenAI keys | literal credentials | immediate rotation if shipped |
| Bearer / api_key / password assignments | embedded credentials | same |
| Private key block | certificate material | same |
| Connection strings with credentials | database access | same |
| High-entropy 43+ string | probable key the list doesn't know | assume hostile |
| Email / phone | personal contact surface | spam, phishing, de-anonymization |
| `/Users/…`, `/home/…` paths | your username and layout | de-anonymization surface |
| Private IPs, internal hostnames | your infrastructure map | recon surface |
| Financial specifics | account/amount context | targeted phishing surface |
| Real names (--names) | the human or agent, unabstracted | the abstraction failed at its core job |
