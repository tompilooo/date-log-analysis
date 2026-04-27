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
# DETECT TZ SOURCE
# =============================
def detect_tz_source(line):
    # Apache (punya TZ sendiri)
    if "[" in line and "]" in line:
        return "from_log"

    # Palo Alto CEF (GMT)
    if "CEF:" in line and "rt=" in line:
        return "UTC"

    # FortiGate / Palo Alto CSV
    if "date=" in line or re.search(r'\d{4}/\d{2}/\d{2}', line):
        return "UTC"

    # Syslog fallback
    if re.search(r'^[A-Za-z]{3}\s+\d{1,2}', line):
        return "UTC"

    return "UTC"


# =============================
# EXTRACT TIMESTAMP
# =============================
def extract_timestamp(line):

    # Palo Alto ISO
    m = re.search(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', line)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y/%m/%d %H:%M:%S")
        except:
            pass

    # Palo Alto CEF
    m = re.search(r'(rt|start)=([A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2})', line)
    if m:
        try:
            return datetime.strptime(m.group(2), "%b %d %Y %H:%M:%S")
        except:
            pass

    # Apache
    m = re.search(r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+\-]\d{4})\]', line)
    if m:
        try:
            return datetime.strptime(m.group(1), "%d/%b/%Y:%H:%M:%S %z")
        except:
            pass

    # FortiGate
    m = re.search(r'date=(\d{4}-\d{2}-\d{2})\s+time=(\d{2}:\d{2}:\d{2})', line)
    if m:
        try:
            return datetime.strptime(
                f"{m.group(1)} {m.group(2)}",
                "%Y-%m-%d %H:%M:%S"
            )
        except:
            pass

    # Fallback
    try:
        return parser.parse(line)
    except:
        return None


# =============================
# PROCESS TEXT LOG
# =============================
def process_text_log(filepath):
    min_raw = None
    max_raw = None
    tz_label = None

    try:
        with open(filepath, 'r', errors='ignore') as f:
            for line in f:
                ts = extract_timestamp(line)
                if not ts:
                    continue

                tz_source = detect_tz_source(line)

                # assign TZ jika tidak ada
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=DEFAULT_TZ)

                if tz_label is None:
                    if tz_source == "from_log":
                        tz_label = str(ts.tzinfo)
                    else:
                        tz_label = "UTC"

                # RAW (belum convert)
                if not min_raw or ts < min_raw:
                    min_raw = ts
                if not max_raw or ts > max_raw:
                    max_raw = ts

    except Exception as e:
        print(f"[!] Error: {filepath} -> {e}")

    # NORMALIZE
    min_norm = min_raw.astimezone(TARGET_TZ) if min_raw else None
    max_norm = max_raw.astimezone(TARGET_TZ) if max_raw else None

    return min_raw, max_raw, min_norm, max_norm, tz_label


# =============================
# PROCESS EVTX
# =============================
def process_evtx(filepath):
    min_raw = None
    max_raw = None

    try:
        with Evtx(filepath) as log:
            for record in log.records():
                try:
                    xml = record.xml()
                    m = re.search(r'SystemTime="([^"]+)"', xml)

                    if m:
                        ts = parser.parse(m.group(1))

                        if not min_raw or ts < min_raw:
                            min_raw = ts
                        if not max_raw or ts > max_raw:
                            max_raw = ts

                except:
                    continue

    except Exception as e:
        print(f"[!] Error EVTX: {filepath} -> {e}")

    min_norm = min_raw.astimezone(TARGET_TZ) if min_raw else None
    max_norm = max_raw.astimezone(TARGET_TZ) if max_raw else None

    return min_raw, max_raw, min_norm, max_norm, "UTC"


# =============================
# SCAN DIRECTORY
# =============================
def scan_logs(directory):
    results = []

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            if file.lower().endswith(".evtx"):
                result = process_evtx(path)
            else:
                result = process_text_log(path)

            results.append((path, *result))

    return results


# =============================
# OUTPUT
# =============================
def print_results(results):
    print("\n===== LOG SUMMARY =====\n")

    for r in results:
        path, raw_start, raw_end, norm_start, norm_end, tz = r

        print(path)
        print(f"  Original TZ : {tz}")
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
    results = scan_logs(log_dir)
    print_results(results)