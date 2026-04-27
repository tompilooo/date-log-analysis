import os
import re
from datetime import datetime, timezone, timedelta
from dateutil import parser
from Evtx.Evtx import Evtx

# =============================
# CONFIG
# =============================
TARGET_TZ = timezone(timedelta(hours=7))
DEFAULT_TZ = timezone.utc


# =============================
# DETECT LOG TYPE
# =============================
def detect_log_type(line):
    if "[" in line and "]" in line:
        return "apache"

    if "date=" in line and "time=" in line:
        return "fortigate"

    if "CEF:" in line:
        return "paloalto_cef"

    if re.search(r'\d{4}/\d{2}/\d{2}', line):
        return "paloalto_csv"

    if re.search(r'^[A-Za-z]{3}\s+\d{1,2}', line):
        return "syslog"

    return "unknown"


# =============================
# EXTRACT TIMESTAMP
# =============================
def extract_timestamp(line):

    # Palo Alto ISO
    m = re.search(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', line)
    if m:
        return datetime.strptime(m.group(1), "%Y/%m/%d %H:%M:%S")

    # Palo Alto CEF
    m = re.search(r'(rt|start)=([A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2})', line)
    if m:
        return datetime.strptime(m.group(2), "%b %d %Y %H:%M:%S")

    # Apache
    m = re.search(r'\[(.*?)\]', line)
    if m:
        try:
            return datetime.strptime(m.group(1), "%d/%b/%Y:%H:%M:%S %z")
        except:
            pass

    # Forti
    m = re.search(r'date=(\d{4}-\d{2}-\d{2})\s+time=(\d{2}:\d{2}:\d{2})', line)
    if m:
        return datetime.strptime(f"{m.group(1)} {m.group(2)}", "%Y-%m-%d %H:%M:%S")

    # fallback
    try:
        return parser.parse(line)
    except:
        return None


# =============================
# NORMALIZE
# =============================
def normalize(ts):
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=DEFAULT_TZ)
    return ts.astimezone(TARGET_TZ)


# =============================
# PROCESS FILE
# =============================
def process_file(filepath):
    min_raw = None
    max_raw = None
    log_type = None

    try:
        if filepath.lower().endswith(".evtx"):
            with Evtx(filepath) as log:
                for record in log.records():
                    xml = record.xml()
                    m = re.search(r'SystemTime="([^"]+)"', xml)
                    if m:
                        ts = parser.parse(m.group(1))
                        log_type = "evtx"

                        if not min_raw or ts < min_raw:
                            min_raw = ts
                        if not max_raw or ts > max_raw:
                            max_raw = ts

        else:
            with open(filepath, 'r', errors='ignore') as f:
                for line in f:
                    ts = extract_timestamp(line)
                    if not ts:
                        continue

                    if not log_type:
                        log_type = detect_log_type(line)

                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=DEFAULT_TZ)

                    if not min_raw or ts < min_raw:
                        min_raw = ts
                    if not max_raw or ts > max_raw:
                        max_raw = ts

    except Exception as e:
        print(f"[!] Error: {filepath} -> {e}")

    return log_type, min_raw, max_raw


# =============================
# GROUP BY FOLDER + TYPE
# =============================
def scan_logs(directory):
    grouped = {}

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            log_type, start, end = process_file(path)

            if not start:
                continue

            key = (root, log_type)

            if key not in grouped:
                grouped[key] = {
                    "files": 0,
                    "start": start,
                    "end": end
                }

            grouped[key]["files"] += 1

            if start < grouped[key]["start"]:
                grouped[key]["start"] = start

            if end > grouped[key]["end"]:
                grouped[key]["end"] = end

    return grouped


# =============================
# OUTPUT
# =============================
def print_results(grouped):
    print("\n===== LOG SUMMARY =====\n")

    for (folder, log_type), data in grouped.items():
        raw_start = data["start"]
        raw_end = data["end"]

        norm_start = normalize(raw_start)
        norm_end = normalize(raw_end)

        print(f"[FOLDER] {folder}")
        print(f"  Type        : {log_type}")
        print(f"  Files       : {data['files']} files")
        print(f"  Original TZ : UTC")
        print(f"  Start       : {raw_start}")
        print(f"  End         : {raw_end}")
        print()
        print(f"  Normalized  : UTC+7")
        print(f"  Start       : {norm_start}")
        print(f"  End         : {norm_end}")
        print("-" * 50)


# =============================
# MAIN
# =============================
if __name__ == "__main__":
    log_dir = input("Enter log directory path: ").strip()
    grouped = scan_logs(log_dir)
    print_results(grouped)