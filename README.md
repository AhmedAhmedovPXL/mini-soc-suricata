# 🛡️ Mini SOC – Integrated Security Project

> A simulated Security Operations Center (SOC) built as part of the Advanced Security course at PXL Hogeschool.

---

## 📌 Project Overview

This project simulates a real-world SOC environment capable of detecting, monitoring, and **automatically responding** to cyber attacks using open-source tooling.

The setup consists of two virtual machines:
- **VM1 (Defender)** – Ubuntu running the full detection and response stack
- **VM2 (Attacker)** – Kali Linux / Ubuntu used to simulate attacks (e.g. Nmap scans)

---

## 🧰 Stack

| Component | Role |
|---|---|
| **Suricata IDS/IPS** | Real-time network traffic analysis and attack detection |
| **Filebeat** | Ships Suricata logs to Elasticsearch |
| **Elasticsearch** | Indexes and stores alert data |
| **Grafana** | Visualizes alerts via Elasticsearch datasource |
| **autoblock.py** | Automated IP blocking based on Suricata alerts |
| **suricata_report.sh** | Generates a human-readable security report |

---

## 🏗️ Architecture

```
┌─────────────────────────────┐        ┌──────────────────────┐
│        VM1 – Defender       │        │    VM2 – Attacker    │
│                             │◄──────►│                      │
│  Suricata (IDS/IPS)         │        │  Nmap / attack tools │
│  Filebeat                   │        └──────────────────────┘
│  Elasticsearch              │
│  Grafana                    │
│  autoblock.py (iptables)    │
│  suricata_report.sh         │
└─────────────────────────────┘
```

> See `architecture/diagram.png` for the full diagram.

---

## ⚙️ Installation

See [docs/setup.md](docs/setup.md) for the full installation guide.

---

## 🚀 Demo

### How it works

1. Start Suricata on VM1
2. Run the autoblock reset script on VM1:
   ```bash
   sudo python3 scripts/autoblock_reset.py
   ```
3. Simulate an attack from VM2:
   ```bash
   nmap -A <VM1-IP>
   ```
4. Watch Suricata detect the scan → `autoblock.py` automatically blocks the attacker IP via `iptables`
5. Generate a security report:
   ```bash
   ./scripts/suricata_report.sh
   ```
6. Open Grafana to visualize the alerts in real time

---

## 📊 Key Features

- **Automated threat response** – no manual intervention needed to block attacking IPs
- **Real-time dashboarding** – Grafana dashboard connected to Elasticsearch for live alert visualization
- **Human-readable reporting** – shell script generates a clean summary of detected threats
- **Realistic attack simulation** – full attacker/defender VM setup mimicking a real network environment

---

## 📹 Recordings

- [Presentatie (PowerPoint)](https://hogeschoolpxl-my.sharepoint.com/:p:/r/personal/12300457_student_pxl_be/_layouts/15/Doc.aspx?sourcedoc=%7BD5637C58-C00B-45F9-9CD5-F532315EDB90%7D&file=MINI_SOC_final.pptx&action=edit&mobileredirect=true)

---

## 🎓 Context

Built for the **Advanced Security** course at [PXL Hogeschool](https://www.pxl.be), Hasselt — as part of the Graduaat Systeem en Netwerkbeheer program (2025–2026).
