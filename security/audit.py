#!/usr/bin/env python3
"""
Dreamwright Privacy Gate — pre-publish audit for dreams and dream-derived posts.

Scans a file (or directory) for real names, secrets, credentials, and personal
infrastructure that must not leave the local workspace. Built for the Dreamwright
dream practice: dreams abstract real events into metaphor, and this gate is the
check that the abstraction actually held.

Exit codes: 0 = clean, 1 = critical issues found, 2 = warnings only (fails --strict)

Usage:
  python3 audit.py --file posts/2026-10-04-dreambook.md --strict --names "Nick,Forge"
  python3 audit.py --dir posts/ --names "Nick,Forge"
  python3 audit.py --file any.md --config my-patterns.json

"""

import json
import re
import sys
from pathlib import Path

# ============================================================================
# CRITICAL PATTERNS — universal secrets. One hit = do not ship, any mode.
# ============================================================================

CRITICAL_PATTERNS = [
    # Cloud & service keys
    (r'\bAKIA[0-9A-Z]{16}\b', "AWS access key id"),
    (r'\bsk_live_[A-Za-z0-9]+', "Stripe live secret key"),
    (r'\brk_live_[A-Za-z0-9]+', "Stripe live restricted key"),
    (r'\bgh[pousr]_[A-Za-z0-9]{36,}', "GitHub token"),
    (r'\bxox[baprs]-[A-Za-z0-9\-]+', "Slack token"),
    (r'\bsk-[A-Za-z0-9\-_]{20,}', "OpenAI-style API key"),
    (r'\bglpat-[A-Za-z0-9\-_]{20,}', "GitLab personal access token"),
    (r'\bntn_[A-Za-z0-9]+', "Notion integration token"),
    # Generic credential assignments
    (r'\bBearer\s+[A-Za-z0-9\-_\.]{20,}', "Bearer auth token"),
    (r'\bapi[_-]?key["\s:=]+["\'][A-Za-z0-9\-_]{16,}', "API key assignment"),
    (r'\bsecret["\s:=]+["\'][A-Za-z0-9\-_]{16,}', "Secret value assignment"),
    (r'\bpassword["\s:=]+["\'][^"\']{8,}', "Password assignment"),
    # Private key material
    (r'-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----', "Private key block"),
    # Connection strings with embedded credentials
    (r'(?:postgresql|postgres|mongodb|mysql|redis)://[^\s/:@]+:[^\s/@]+@[^\s]+', "Database connection string with credentials"),
    # High-entropy strings that look like keys (40+ chars, mixed)
    (r'\b[A-Za-z0-9_\-]{43,}\b', "Possible key or token (high entropy, 43+ chars)"),
]

# ============================================================================
# WARNING PATTERNS — context-dependent. Fails only in --strict mode.
# ============================================================================

WARNING_PATTERNS = [
    (r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b', "Email address"),
    (r'\+1\s*\(?\d{3}\)?\s*[\-\.\s]?\d{3}\s*[\-\.\s]?\d{4}', "Phone number"),
    (r'\b\d{3}[\-\.\s]\d{3}[\-\.\s]\d{4}\b', "Phone number (no country code)"),
    (r'/Users/[A-Za-z0-9_.\-]+', "Absolute macOS path (leaks username)"),
    (r'/home/[A-Za-z0-9_.\-]+', "Absolute home path (leaks username)"),
    (r'\b(?:10|192\.168)\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "Private/internal IP address"),
    (r'https?://[^\s/:@]+:[^\s/@]+@[^\s]+', "URL with embedded credentials"),
    (r'\$\d{1,3}(?:,\d{3})+(?:\.\d{2})?\s*(?:cash|equity|balance|account|portfolio|position)', "Financial account specifics"),
    (r'\b(?:api|staging|dev|internal|admin)\.[a-z0-9\-]+\.[a-z]{2,}\b', "Internal/infrastructure hostname"),
]

# ============================================================================
# Custom personal patterns — loaded via --config (JSON: {"critical": [...],
# "warning": [...]} with [pattern, label] pairs). Put YOUR infrastructure,
# your tailscale IPs, your internal hostnames, your key prefixes here.
# ============================================================================


def load_custom_patterns(config_path):
    critical, warning = [], []
    if not config_path:
        return critical, warning
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for pat, label in data.get("critical", []):
            critical.append((re.compile(pat), label))
        for pat, label in data.get("warning", []):
            warning.append((re.compile(pat), label))
    except (OSError, ValueError) as exc:
        print(f"⚠️  Could not load config {config_path}: {exc}")
    return critical, warning


def compile_names(names):
    """Real names are scanned as whole-word case-insensitive matches."""
    compiled = []
    for name in names or []:
        name = name.strip()
        if len(name) >= 3:
            compiled.append((re.compile(r'\b' + re.escape(name) + r'\b', re.IGNORECASE),
                             f'Real name "{name}"'))
    return compiled


def scan_text(text, critical, warning):
    crit_hits, warn_hits = [], []
    for pattern, label in critical:
        for match in pattern.finditer(text):
            snippet = text[max(0, match.start() - 30):match.end() + 30].replace("\n", " ")
            crit_hits.append((label, match.group(0)[:24], snippet))
    for pattern, label in warning:
        for match in pattern.finditer(text):
            snippet = text[max(0, match.start() - 30):match.end() + 30].replace("\n", " ")
            warn_hits.append((label, match.group(0)[:24], snippet))
    return crit_hits, warn_hits


def report(target, crit_hits, warn_hits, strict):
    print("=" * 60)
    print(f"Dreamwright Privacy Gate — {target}")
    print("=" * 60)
    if crit_hits:
        print(f"\n🚨 CRITICAL ({len(crit_hits)}):")
        for label, hit, snippet in crit_hits[:12]:
            print(f"  • {label}: {hit}…\n    context: …{snippet}…")
    if warn_hits:
        print(f"\n⚠️  WARNINGS ({len(warn_hits)}):")
        for label, hit, snippet in warn_hits[:12]:
            print(f"  • {label}: {hit}…\n    context: …{snippet}…")

    print("\n" + "=" * 60)
    if strict:
        fails = len(crit_hits) + len(warn_hits)
        print(f"  Results: {len(crit_hits)} critical, {len(warn_hits)} warnings (--strict)")
        if fails == 0:
            print("  ✅ CLEAN — safe to publish")
            print("=" * 60)
            return 0
        print("  🛑 NOT CLEAN — do not publish")
        print("=" * 60)
        return 1 if crit_hits else 2
    if crit_hits:
        print(f"  Results: {len(crit_hits)} critical, {len(warn_hits)} warnings")
        print("  🛑 CRITICAL ISSUES — do not publish")
        print("=" * 60)
        return 1
    print(f"  Results: {len(crit_hits)} critical, {len(warn_hits)} warnings")
    print("  ✅ No critical issues" + (" (warnings present — review)" if warn_hits else " — clean"))
    print("=" * 60)
    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dreamwright Privacy Gate")
    parser.add_argument("--file", help="single file to scan")
    parser.add_argument("--dir", help="directory to scan (markdown/text)")
    parser.add_argument("--text", help="raw text to scan")
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    parser.add_argument("--names", default="", help="comma-separated real names to catch")
    parser.add_argument("--config", help="JSON file with custom [pattern,label] pairs")
    args = parser.parse_args()

    if not (args.file or args.dir or args.text):
        parser.error("one of --file, --dir, --text is required")

    custom_critical, custom_warning = load_custom_patterns(args.config)
    critical = [(re.compile(p), label) for p, label in CRITICAL_PATTERNS] + custom_critical
    warning = [(re.compile(p), label) for p, label in WARNING_PATTERNS] + custom_warning
    critical += compile_names(args.names.split(",") if args.names else [])

    total_crit, total_warn, target = [], [], (args.file or args.dir or "text")
    texts = []
    if args.text:
        texts.append(("text", args.text))
    elif args.file:
        texts.append((args.file, Path(args.file).read_text(encoding="utf-8", errors="replace")))
    elif args.dir:
        for path in sorted(Path(args.dir).rglob("*")):
            if path.suffix.lower() in {".md", ".txt", ".html"} and path.is_file():
                texts.append((str(path), path.read_text(encoding="utf-8", errors="replace")))

    for label, text in texts:
        crit_hits, warn_hits = scan_text(text, critical, warning)
        total_crit += [(label,) + hit for hit in crit_hits]
        total_warn += [(label,) + hit for hit in warn_hits]

    sys.exit(report(target, total_crit, total_warn, args.strict))


if __name__ == "__main__":
    main()
