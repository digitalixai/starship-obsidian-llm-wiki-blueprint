#!/usr/bin/env python3
# =============================================================================
# Script: obsidian_sync_transcript.py
# Purpose: Synchronizes the active IDE agent session chat transcript to
#          Obsidian daily journals using unique HTML boundary markers.
# =============================================================================

import os
import sys
import json
import re
from datetime import datetime, timezone

# 1. Configuration (Fallback to environment variables or local paths)
VAULT_PATH = os.environ.get("OBSIDIAN_VAULT_PATH")
if not VAULT_PATH:
    # Example fallbacks for testing
    VAULT_PATH = os.path.expanduser("~/Documents/Obsidian Vault/Antigravity/Bitacoras")

# App data directory for the IDE cache
APP_DATA_DIR = os.environ.get("APP_DATA_DIR")
if not APP_DATA_DIR:
    if os.path.exists(os.path.expanduser("~/.gemini/antigravity-ide")):
        APP_DATA_DIR = os.path.expanduser("~/.gemini/antigravity-ide")
    else:
        APP_DATA_DIR = os.path.expanduser("~/.gemini/antigravity")

BRAIN_BASE = os.path.join(APP_DATA_DIR, "brain")

DAYS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MONTHS_ES = {
    "january": "enero", "february": "febrero", "march": "marzo", "april": "abril",
    "may": "mayo", "june": "junio", "july": "julio", "august": "agosto",
    "september": "septiembre", "october": "octubre", "november": "noviembre", "december": "diciembre"
}


def get_current_session_id():
    """Detects the most recent conversation directory index."""
    try:
        dirs = [
            d for d in os.listdir(BRAIN_BASE)
            if os.path.isdir(os.path.join(BRAIN_BASE, d))
        ]
        if not dirs:
            return None
        latest_dir = max(
            [os.path.join(BRAIN_BASE, d) for d in dirs],
            key=os.path.getmtime
        )
        return os.path.basename(latest_dir)
    except Exception as e:
        print(f"❌ Error detecting active session: {e}")
        return None


def get_project_name(transcript_path):
    """Scans the transcript to guess project name from keywords."""
    project = "Generic_Project"
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                content = data.get("content", "")
                if any(x in content for x in ["AutoCarrousel", "MediaCatalog"]):
                    return "Media_Generator"
                elif "SecurityAudit" in content or "CyberLearn" in content:
                    return "Security_Lab"
                elif "Database" in content or "CRM" in content:
                    return "Client_CRM"
                elif "SysAdmin" in content:
                    return "SysAdmin"
    except:
        pass
    return project


def sync_transcript(conv_id=None, project_name=None):
    if not conv_id:
        conv_id = get_current_session_id()

    if not conv_id:
        print("❌ Error: Active session ID could not be resolved.")
        return False

    transcript_path = os.path.join(BRAIN_BASE, conv_id, ".system_generated", "logs", "transcript.jsonl")
    if not os.path.exists(transcript_path):
        print(f"❌ Error: Transcript not found at {transcript_path}")
        return False

    if not project_name:
        project_name = get_project_name(transcript_path)

    print(f"🚀 Syncing transcript for session: {conv_id} ({project_name})")

    first_time = None
    interactions = []
    
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if not first_time and "created_at" in data:
                    first_time = data["created_at"]
                
                m_type = data.get("type")
                source = data.get("source")
                content = data.get("content", "")
                
                if not content:
                    continue
                    
                created_at = data.get("created_at")
                step_time = ""
                if created_at:
                    try:
                        s_dt = datetime.strptime(created_at[:19], "%Y-%m-%dT%H:%M:%S")
                        local_dt = s_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
                        step_time = local_dt.strftime('%H:%M:%S')
                    except Exception:
                        pass

                if m_type == "USER_INPUT" and source == "USER_EXPLICIT":
                    clean_content = re.sub(r'</?USER_REQUEST>', '', content).strip()
                    interactions.append({
                        "role": "User",
                        "content": clean_content,
                        "time": step_time
                    })
                elif m_type == "PLANNER_RESPONSE" and source == "MODEL":
                    interactions.append({
                        "role": "Antigravity Agent",
                        "content": content.strip(),
                        "time": step_time
                    })
            except Exception as e:
                pass

    if not first_time or not interactions:
        print("⚠️ No valid interaction blocks found to export.")
        return False

    try:
        dt = datetime.strptime(first_time[:19], "%Y-%m-%dT%H:%M:%S")
        date_str = dt.strftime('%Y%m%d')
        day_es = DAYS_ES[dt.weekday()]
        
        month_eng = dt.strftime('%B').lower()
        month_es = MONTHS_ES.get(month_eng, month_eng)
        month_folder_name = f"{dt.strftime('%m')}.{month_es}.{dt.year}"
    except Exception as e:
        print(f"❌ Error parsing timestamp: {e}")
        return False

    # Create HTML boundary markers for safe rewrites
    start_marker = f"<!-- START_CONVERSATION_{conv_id} -->"
    end_marker = f"<!-- END_CONVERSATION_{conv_id} -->"
    
    block = f"\n{start_marker}\n"
    block += f"## Session Transcript: {project_name} ({conv_id})\n"
    block += f"**Start time:** {dt.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for idx, turn in enumerate(interactions):
        role = turn["role"]
        body = turn["content"]
        time_suffix = f" [{turn['time']}]" if turn.get("time") else ""
        block += f"### Turn {idx+1} — {role}{time_suffix}:\n{body}\n\n"
        block += "--\n\n"
    block += f"{end_marker}\n"

    # Synchronize to target directory
    if not os.path.exists(VAULT_PATH):
        print(f"❌ Target path not found: {VAULT_PATH}. Please verify vault configurations.")
        return False
        
    os.makedirs(os.path.join(VAULT_PATH, month_folder_name), exist_ok=True)
    
    # Locate existing markdown logs matching today's prefix
    matched_files = []
    for root, dirs, files in os.walk(VAULT_PATH):
        for f in files:
            # Normalize accents for Spanish UTF-8 compatibility
            norm_f = f.replace("á", "á").replace("é", "é").replace("í", "í").replace("ó", "ó").replace("ú", "ú")
            if norm_f.endswith(".md") and norm_f.startswith(date_str):
                matched_files.append(os.path.join(root, f))

    if matched_files:
        for filepath in matched_files:
            with open(filepath, "r", encoding="utf-8") as f:
                orig_content = f.read()
                
            pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
            
            # If the block already exists, rewrite it. Otherwise, append to end.
            if pattern.search(orig_content):
                new_content = pattern.sub(lambda m: block, orig_content)
                action = "Updated existing transcript block"
            else:
                if not orig_content.endswith("\n"):
                    orig_content += "\n"
                new_content = orig_content + "\n" + block
                action = "Appended transcript block to end of note"
                
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ [{action}] in {os.path.basename(filepath)} ({len(interactions)} turns)")
    else:
        # Create a new markdown log if none exists
        filename = f"{date_str}_{day_es}_log_{project_name}.md"
        filepath = os.path.join(VAULT_PATH, month_folder_name, filename)
        
        header = f"# Log: {project_name} — {date_str} {day_es}\n\n"
        header += f"**Date:** {dt.strftime('%Y-%m-%d')}\n"
        header += f"**Project:** {project_name}\n\n---\n\n"
        header += block
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header)
        print(f"🆕 Created new daily log: {month_folder_name}/{filename} ({len(interactions)} turns)")
        
    return True


if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else None
    proj = sys.argv[2] if len(sys.argv) > 2 else None
    sync_transcript(cid, proj)
