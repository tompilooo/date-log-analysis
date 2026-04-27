# 🕵️‍♂️ Log Timeline Extractor (DFIR Tool)

A lightweight Python tool for **Digital Forensics & Incident Response (DFIR)** to quickly identify:

* 📅 **Earliest (Start) event**
* 📅 **Latest (End) event**
* 🌍 **Original timezone from log source**
* 🔄 **Normalized timeline (UTC+7)**

Supports multiple log sources commonly used in investigations.

---

## 🚀 Features

* ✅ Multi-log support:

  * Apache / Nginx
  * FortiGate Firewall
  * Palo Alto (CSV, CEF, GlobalProtect)
  * Windows Event Log (`.evtx`)
* ✅ Automatic timestamp extraction
* ✅ Auto-detect timezone per log source
* ✅ Normalize all timestamps to **UTC+7 (WIB)**
* ✅ Clean **summary output (no noise)**

---

## 📂 Example Output

```
===== LOG SUMMARY =====

sample/apache.log
  Original TZ : UTC
  Start       : 2015-05-17 10:05:22+00:00
  End         : 2015-05-20 14:11:03+00:00

  Normalized  : UTC+7
  Start       : 2015-05-17 17:05:22+07:00
  End         : 2015-05-20 21:11:03+07:00
--------------------------------------------------
```

---

## ⚙️ Requirements

* Python 3.8+
* Install dependencies:

```
pip install python-evtx python-dateutil
```

---

## ▶️ Usage

```
python main.py
```

Then input your log directory:

```
Enter log directory path: sample/
```

---

## 🧠 Supported Log Formats

### 🔹 Web Server

* Apache / Nginx (Common/Combined log)

### 🔹 Firewall

* FortiGate (`date=YYYY-MM-DD time=HH:MM:SS`)
* Palo Alto:

  * CSV logs
  * CEF (`rt=...`)
  * GlobalProtect

### 🔹 Endpoint

* Windows Event Log (`.evtx`)

---

## 🌍 Timezone Handling

This tool follows DFIR best practices:

| Log Type      | Timezone Handling       |
| ------------- | ----------------------- |
| Apache/Nginx  | Uses timezone from log  |
| Palo Alto CEF | Parsed as UTC (GMT)     |
| FortiGate     | Assumed UTC             |
| Palo Alto CSV | Assumed UTC             |
| EVTX          | Uses embedded timestamp |

👉 All timestamps are normalized to:

```
UTC+7 (WIB)
```

---

## ⚠️ Important Notes

* Logs without timezone info are **assumed UTC by default**
* You can modify this in the script:

  ```python
  DEFAULT_TZ = timezone.utc
  ```
* Incorrect timezone assumptions may affect forensic timelines

---

## 🧪 Use Cases

* 🔍 Initial incident triage
* 🕒 Timeline scoping
* 📊 Log coverage validation
* 🔗 Cross-log correlation preparation

---

## 🔥 Future Improvements

* Export to CSV / Timesketch
* Super timeline (multi-log merge)
* IOC detection (IP, domain, user)
* Event correlation engine

---

## 🛡️ Disclaimer

This tool is intended for **forensic analysis and security research**.
Always validate findings with additional evidence.

---

## 👨‍💻 Author

Built for DFIR practitioners who need **fast, reliable timeline extraction** from heterogeneous logs.
