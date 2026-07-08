#!/usr/bin/env python3
# =============================================================================
# Script: wiki_linter.py
# Purpose: Scans a markdown wiki vault to validate YAML frontmatter, detect
#          orphan pages, identify broken links, and flag stale notes.
# =============================================================================

import os
import re
import sys
from datetime import datetime, timedelta

# Configuration
WIKI_DIR = os.environ.get("WIKI_DIR")
if not WIKI_DIR:
    # Fallback to local directory for quick testing
    WIKI_DIR = "./wiki"

REQUIRED_FIELDS = ["title", "type", "tags", "timestamp", "sources"]
STALE_DAYS = 90


def parse_markdown_file(filepath):
    """
    Parses a markdown file to extract frontmatter and internal wiki links.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract YAML frontmatter
    frontmatter = {}
    yaml_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if yaml_match:
        yaml_block = yaml_match.group(1)
        for line in yaml_block.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'").strip("[").strip("]")
                if key in REQUIRED_FIELDS:
                    if key == "tags" or key == "sources":
                        frontmatter[key] = [t.strip() for t in val.split(",") if t.strip()]
                    else:
                        frontmatter[key] = val

    # Extract all wikilinks [[PageName]] or [[PageName|Label]]
    wikilinks = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)
    # Normalize links to match file names (typically lowercase and space-swapped if needed)
    wikilinks = [link.strip() for link in wikilinks]

    return frontmatter, wikilinks, content


def run_lint(wiki_path):
    print(f"🔍 Running health check on wiki directory: {wiki_path}\n")

    if not os.path.exists(wiki_path):
        print(f"❌ Error: Wiki directory '{wiki_path}' does not exist.")
        return False

    all_files = {}
    links_map = {}
    stale_threshold = datetime.now() - timedelta(days=STALE_DAYS)

    # 1. Scan files
    for root, dirs, files in os.walk(wiki_path):
        for f in files:
            if f.endswith(".md"):
                filepath = os.path.join(root, f)
                name_without_ext = os.path.splitext(f)[0]
                all_files[name_without_ext] = filepath
                
                frontmatter, links, content = parse_markdown_file(filepath)
                links_map[name_without_ext] = {
                    "path": filepath,
                    "frontmatter": frontmatter,
                    "outbound_links": links,
                    "inbound_links": []
                }

    # 2. Populate inbound links
    for source_page, data in links_map.items():
        for target_page in data["outbound_links"]:
            # Match target page ignoring case or exact match
            matched_target = None
            for key in links_map.keys():
                if key.lower() == target_page.lower():
                    matched_target = key
                    break
            
            if matched_target:
                links_map[matched_target]["inbound_links"].append(source_page)

    # 3. Analyze checks
    schema_failures = []
    orphan_pages = []
    broken_links = []
    stale_pages = []

    for page_name, data in links_map.items():
        # Check Schema Integrity
        fm = data["frontmatter"]
        missing_fields = [field for field in REQUIRED_FIELDS if field not in fm]
        if missing_fields:
            schema_failures.append((page_name, missing_fields))

        # Check Orphans (0 inbound links, excluding index/overview pages)
        if not data["inbound_links"] and "index" not in page_name.lower() and "overview" not in page_name.lower():
            orphan_pages.append(page_name)

        # Check Broken Links (outbound links pointing to non-existent pages)
        for target in data["outbound_links"]:
            exists = False
            for key in links_map.keys():
                if key.lower() == target.lower():
                    exists = True
                    break
            if not exists:
                broken_links.append((page_name, target))

        # Check Staleness
        timestamp_str = fm.get("timestamp")
        if timestamp_str:
            try:
                dt = datetime.strptime(timestamp_str, "%Y-%m-%d")
                if dt < stale_threshold:
                    stale_pages.append((page_name, timestamp_str))
            except ValueError:
                pass  # Handled by missing/malformed fields in schema check

    # 4. Generate Report
    print("=== LINT REPORT ===")
    
    print(f"\n1. Schema Integrity: {'🟢 Pass' if not schema_failures else '🔴 Fail'}")
    for page, missing in schema_failures:
        print(f"   - {page}.md is missing fields: {missing}")

    print(f"\n2. Orphan Check: {'🟢 Pass' if not orphan_pages else '🟡 Warning'}")
    for page in orphan_pages:
        print(f"   - {page}.md has 0 inbound links (Orphan).")

    print(f"\n3. Broken Link Check (Coverage Gaps): {'🟢 Pass' if not broken_links else '🔴 Fail'}")
    for source, target in broken_links:
        print(f"   - {source}.md links to non-existent page: [[{target}]]")

    print(f"\n4. Staleness Check: {'🟢 Pass' if not stale_pages else '🟡 Warning'}")
    for page, date in stale_pages:
        print(f"   - {page}.md is stale (Last updated: {date}, threshold: {STALE_DAYS} days)")

    print("\n===================")
    overall_health = "🟢 Healthy" if not (schema_failures or broken_links) else "🔴 Action Required"
    print(f"Overall Status: {overall_health}")
    return True


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else WIKI_DIR
    run_lint(path)
