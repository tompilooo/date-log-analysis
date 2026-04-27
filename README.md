# 🕵️‍♂️ Log Timeline Extractor (DFIR Tool)

A lightweight Python tool for **Digital Forensics & Incident Response (DFIR)** to quickly generate **timeline summaries** from various log sources.

---

## 🚀 Features

* ✅ Multi-log support:

  * Apache / Nginx
  * FortiGate Firewall
  * Palo Alto (CSV, CEF, GlobalProtect)
  * Windows Event Log (`.evtx`)
* ✅ Automatic timestamp extraction
* ✅ Auto-detect log type
* ✅ **Group logs by folder + type**
* ✅ **Single recap timeline per log group**
* ✅ Timezone normalization to **UTC+7 (WIB)**
* ✅ Clean & minimal output (DFIR triage ready)

---

## 🆕 What’s New

🔹 Logs with the **same type in the same folder are grouped into one timeline**

Before:

```id="old1"
1 file = 1 timeline
```

Now:

```id="new1"
1 folder + 1 log type = 1 timeline summary
```

👉 This reflects real DFIR workflow:

* Faster triage
* Easier correlation
* Cleaner investigation scope

---

## 📂 Example Output

```id="ex1"
===== LOG SUMMARY =====

[FOLDER] sample/palo/
  Type        : paloalto_csv
  Files       : 3 files
  Original TZ : UTC
  Start       : 2014-01-01 04:58:12
  End         : 2020-08-20 09:12:11

  Normalized  : UTC+7
  Start       : 2014-01-01 11:58:12+07:00
  End         : 2020-08-20 16:12:11+07:00
--------------------------------------------------
```

---

## ⚙️ Requirements

* Python 3.8+
* Install dependencies:

```id="req1"
pip install python-evtx python-dateutil
```

---

## ▶️ Usage

```id="run1"
python main.py
```

Input your log directory:

```id="run2"
Enter log directory path: sample/
```

---

## 🧠 Supported Log Types

### 🔹 Web Server

* Apache / Nginx (Common / Combined log)

### 🔹 Firewall

* FortiGate
* Palo Alto:

  * CSV logs
  * CEF format
  * GlobalProtect logs

### 🔹 Endpoint

* Windows Event Logs (`.evtx`)

---

## 🌍 Timezone Handling

| Log Type      | Timezone Behavior       |
| ------------- | ----------------------- |
| Apache/Nginx  | Uses timezone from log  |
| Palo Alto CEF | Parsed as UTC (GMT)     |
| FortiGate     | Assumed UTC             |
| Palo Alto CSV | Assumed UTC             |
| EVTX          | Uses embedded timestamp |

👉 All timestamps are normalized to:

```id="tz1"
UTC+7 (WIB)
```

---

## 📊 Output Explanation

Each result represents:

* 📁 **Folder** → Log location
* 🏷️ **Type** → Detected log type
* 📄 **Files** → Number of logs in group
* 🕒 **Start/End (Original)** → Raw timeline
* 🔄 **Start/End (Normalized)** → Converted to UTC+7

---

## 🧪 Use Cases

* 🔍 Initial incident triage
* 🕒 Define investigation time window
* 📊 Validate log coverage
* 🔗 Prepare for timeline correlation
* 🛡️ Threat hunting baseline

---

## ⚠️ Important Notes

* Logs without timezone info are **assumed UTC**
* Modify default timezone in code if needed:

  ```python
  DEFAULT_TZ = timezone.utc
  ```
* Incorrect assumptions may affect forensic accuracy

---

## 🔥 Future Improvements

* Export to CSV / Timesketch
* Super timeline (cross-log correlation)
* IOC detection (IP, domain, user)
* Suspicious activity detection
* Visualization (timeline graph)

---

## 🛡️ Disclaimer

This tool is intended for:

* Digital forensic analysis
* Incident response investigation

Always validate findings with multiple data sources.

---

## 👨‍💻 Author

Built for DFIR practitioners who need:

> ⚡ Fast, clean, and reliable timeline summaries from heterogeneous logs
