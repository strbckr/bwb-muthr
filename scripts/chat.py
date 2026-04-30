#!/usr/bin/env python3
"""
chat.py — a streamlined, animated terminal chat client for Claude Sonnet 4.6.
Directly enters a chat session on launch with smooth text reveal.
"""

import curses
import os
import queue
import re
import sys
import textwrap
import threading
import time

try:
    import anthropic
except ImportError:
    print("Missing dependency. Install with: pip install anthropic")
    sys.exit(1)

# ── Config ──────────────────────────────────────────────────────────────────

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096
TTY1_LOG = os.path.expanduser("~/.tty1.log")
BASE_SYSTEM_PROMPT = (
    "You are a helpful, curious assistant. Keep responses clear and "
    "conversational. Use flowing prose over heavy markdown. When providing "
    "code, always use fenced code blocks with the language specified."
)

# ── UI Utilities ───────────────────────────────────────────────────────────

def wrap_text(text, width):
    result = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            result.append('')
        else:
            result.extend(textwrap.wrap(paragraph, width=width))
    return result

def process_markdown(text):
    output = []
    in_code_block = False
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        style = "code" if in_code_block else "normal"
        if not stripped:
            output.append(("", style))
        else:
            output.append((line, style))
    return output

def build_exchange_lines(exchanges, width, prompt_color):
    lines = []
    for user_msg, assistant_msg in exchanges:
        lines.append({"text": "", "style": curses.A_NORMAL})
        lines.append({"text": "  you ›", "style": prompt_color | curses.A_BOLD})
        for wl in wrap_text(user_msg, width - 4):
            lines.append({"text": f"  {wl}", "style": prompt_color})
        
        lines.append({"text": "", "style": curses.A_NORMAL})
        lines.append({"text": "  claude ›", "style": curses.A_BOLD})
        
        if not assistant_msg: continue

        for text, hint in process_markdown(assistant_msg):
            style = curses.color_pair(2) if hint == "code" else curses.A_NORMAL
            prefix = "    " if hint == "code" else "  "
            wrap_list = [text] if hint == "code" else textwrap.wrap(text, width - 6)
            for wl in wrap_list:
                lines.append({"text": f"{prefix}{wl}", "style": style})
    return lines

def draw_screen(stdscr, lines, scroll, prompt_color, input_buf=""):
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    
    # Input area height calculation
    input_prefix = "  you › "
    input_lines = wrap_text(input_prefix + input_buf, w)
    input_h = len(input_lines)
    
    status_row = h - 1 - input_h
    text_h = status_row
    
    for i in range(text_h):
        line_idx = scroll + i
        if line_idx >= len(lines): break
        ld = lines[line_idx]
        try:
            stdscr.addstr(i, 0, ld["text"][:w-1], ld.get("style", curses.A_NORMAL))
        except curses.error: pass

    # Clean divider
    try:
        stdscr.addstr(status_row, 0, ("─" * (w-1)), curses.A_DIM)
    except curses.error: pass

    # Input lines
    for i, il in enumerate(input_lines):
        row = status_row + 1 + i
        if row < h:
            try:
                stdscr.addstr(row, 0, il.ljust(w))
            except curses.error: pass
    stdscr.refresh()

# ── Input Handling ──────────────────────────────────────────────────────────

def get_input(stdscr, lines, prompt_color):
    curses.curs_set(1)
    buf = ""
    h, w = stdscr.getmaxyx()
    while True:
        input_h = len(wrap_text("  you › " + buf, w))
        scroll = max(0, len(lines) - (h - 2 - input_h))
        draw_screen(stdscr, lines, scroll, prompt_color, input_buf=buf)
        
        ch = stdscr.getch()
        if ch in (10, 13): # Enter
            curses.curs_set(0)
            return buf.strip()
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            buf = buf[:-1]
        elif 32 <= ch <= 126:
            buf += chr(ch)
    return None

# ── Session Logic ──────────────────────────────────────────────────────────

def chat_session(stdscr, client, prompt_color):
    exchanges = []
    api_messages = []
    lines = []
    
    while True:
        user_input = get_input(stdscr, lines, prompt_color)
        if not user_input: continue

        # Check for TTY context injection
        if user_input.startswith("/term") and os.path.exists(TTY1_LOG):
            with open(TTY1_LOG, 'r', errors='replace') as f:
                tail = "".join(f.readlines()[-50:])
                user_input = f"Terminal state:\n```\n{tail}\n```"

        api_messages.append({"role": "user", "content": user_input})
        exchanges.append((user_input, ""))
        token_queue = queue.Queue()

        def stream_worker():
            try:
                with client.messages.stream(
                    model=MODEL, max_tokens=MAX_TOKENS,
                    system=BASE_SYSTEM_PROMPT, messages=api_messages,
                ) as stream:
                    for text in stream.text_stream:
                        token_queue.put({"type": "chunk", "content": text})
                token_queue.put({"type": "done"})
            except Exception as e:
                token_queue.put({"type": "error", "content": str(e)})

        threading.Thread(target=stream_worker, daemon=True).start()

        full_response = ""
        revealed_response = ""
        stream_finished = False

        # Typing animation loop
        while not (stream_finished and len(revealed_response) >= len(full_response)):
            # Pull any new chunks from the queue
            try:
                while True:
                    msg = token_queue.get_nowait()
                    if msg["type"] == "chunk":
                        full_response += msg["content"]
                    elif msg["type"] == "done":
                        stream_finished = True
                    elif msg["type"] == "error":
                        full_response += f"\n[Error: {msg['content']}]"
                        stream_finished = True
            except queue.Empty:
                pass

            # Reveal characters slowly to create a smooth typing feel
            if len(revealed_response) < len(full_response):
                # Reveal 1-3 characters per tick for a "fast but human" speed
                step = 2 if not stream_finished else 4
                revealed_response = full_response[:len(revealed_response) + step]
                
                exchanges[-1] = (user_input, revealed_response)
                h, w = stdscr.getmaxyx()
                lines = build_exchange_lines(exchanges, w, prompt_color)
                scroll = max(0, len(lines) - (h - 3))
                draw_screen(stdscr, lines, scroll, prompt_color)
                
            time.sleep(0.01) # Refresh rate

        api_messages.append({"role": "assistant", "content": full_response})

def main(stdscr):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Export ANTHROPIC_API_KEY first.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    chat_session(stdscr, client, curses.color_pair(1))

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        sys.exit(0)
