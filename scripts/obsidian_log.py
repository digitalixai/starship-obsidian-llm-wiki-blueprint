#!/usr/bin/env python3
# =============================================================================
# Script: obsidian_log.py
# Purpose: Appends structured session updates or single events directly to the
#          Obsidian daily journal/log.
# =============================================================================

import os
import sys
import datetime

# 1. Configuration (Fallback to environment variables or local paths)
VAULT_PATH = os.environ.get("OBSIDIAN_VAULT_PATH")
if not VAULT_PATH:
    # Example fallbacks for testing
    VAULT_PATH = os.path.expanduser("~/Documents/Obsidian Vault/Antigravity/Bitacoras")

DAYS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def log_session(session_history, project_name="Generic_Project"):
    """
    Appends the provided session history to an Obsidian daily log file.

    Args:
        session_history: List of dicts containing 'role' and 'content'.
        project_name: Name of the project/context.
    """
    try:
        if not os.path.exists(VAULT_PATH):
            print(f"❌ Error: Vault target path does not exist: {VAULT_PATH}")
            return False

        os.makedirs(VAULT_PATH, exist_ok=True)

        now = datetime.datetime.now()
        date_str = now.strftime('%Y%m%d')
        day_es = DAYS_ES[now.weekday()]

        filename = f"{date_str}_{day_es}_log_{project_name}.md"
        filepath = os.path.join(VAULT_PATH, filename)

        mode = "a" if os.path.exists(filepath) else "w"

        with open(filepath, mode, encoding="utf-8") as f:
            if mode == "w":
                f.write(f"# Log: {project_name} — {date_str} {day_es}\n\n")
                f.write(f"**Date:** {now.strftime('%Y-%m-%d')}\n")
                f.write(f"**Project:** {project_name}\n\n---\n\n")

            f.write(f"### Update: {now.strftime('%H:%M:%S')}\n\n")
            for msg in session_history:
                role = msg.get("role", "Unknown").capitalize()
                content = msg.get("content", "")
                if role in ("User", "Usuario"):
                    f.write(f"**User:** {content}\n\n")
                elif role in ("Assistant", "Model", "Agente"):
                    f.write(f"**Agent:**\n> {content}\n\n")
            f.write("---\n\n")

        print(f"✅ Session successfully logged to: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error logging session: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
        project = sys.argv[2] if len(sys.argv) > 2 else "Generic_Project"
        history = [
            {"role": "user", "content": "Update triggered via CLI"},
            {"role": "assistant", "content": message}
        ]
        log_session(history, project)
    else:
        test_history = [
            {"role": "user", "content": "Test trigger to verify script integration."},
            {"role": "assistant", "content": "Integration verified successfully."}
        ]
        log_session(test_history, "Test")
