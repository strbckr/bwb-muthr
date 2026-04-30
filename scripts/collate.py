#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta

JOURNAL_DIR = os.path.expanduser("~/journal")
FILE_EXT = ".txt"
DAYS = 30
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-opus-4-5-20251101"

SYSTEM_PROMPT = "You are a helpful assistant summarizing someone's personal journal entries from the past 30 days. Write a clear, plain summary of what they have been writing about -- what has been on their mind, what has happened, how they have been feeling. At the end, note a few themes or topics that came up repeatedly that might be worth reflecting on further. Keep the tone neutral and observational, not prescriptive. Do not set goals or objectives for the person. Do not use markdown formatting -- no headers, no bullet points, no bold text. Just plain prose."

def parse_entry(filepath):
    try:
        with open(filepath, "r", errors="replace") as f:
            raw = f.read()
    except Exception:
        return None
    lines = raw.split("\n")
    content_lines = []
    skip_next_blank = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("DATE:") or stripped.startswith("WORDS:"):
            skip_next_blank = True
            continue
        if skip_next_blank and stripped == "":
            skip_next_blank = False
            continue
        content_lines.append(line)
    return "\n".join(content_lines).strip()

def get_entries_last_n_days(n=30):
    if not os.path.isdir(JOURNAL_DIR):
        return []
    cutoff = datetime.now().date() - timedelta(days=n)
    entries = []
    for fname in sorted(os.listdir(JOURNAL_DIR)):
        if not fname.endswith(FILE_EXT) or fname.startswith("."):
            continue
        date_part = fname.replace(FILE_EXT, "")
        try:
            dt = datetime.strptime(date_part, "%Y-%m-%d_%H%M%S")
        except ValueError:
            continue
        if dt.date() < cutoff:
            continue
        content = parse_entry(os.path.join(JOURNAL_DIR, fname))
        if content:
            entries.append((dt, content))
    return entries

def call_claude(user_message):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(1)
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 2048,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user_message}]
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

def main():
    print("Reading journal entries...", file=sys.stderr)
    entries = get_entries_last_n_days(DAYS)
    if not entries:
        print("No entries found in the last 30 days.", file=sys.stderr)
        sys.exit(0)
    print(f"Found {len(entries)} entries. Sending to Claude...", file=sys.stderr)
    blocks = []
    for dt, content in entries:
        blocks.append(f"--- {dt.strftime('%B %d, %Y at %H:%M')} ---\n{content}")
    user_message = "Here are my journal entries from the past 30 days. Please summarize them.\n\n" + "\n\n".join(blocks)
    summary = call_claude(user_message)
    print(summary)
    print(f"\n-- collated {len(entries)} entries from the last {DAYS} days --", file=sys.stderr)

if __name__ == "__main__":
    main()
