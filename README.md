# 🛡️ Mini SOC – Integrated Security Project

> A simulated Security Operations Center (SOC) built as part of the Advanced Security course at PXL Hogeschool.

![Suricata](https://img.shields.io/badge/Suricata-IDS%2FIPS-orange?style=flat-square)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-Search%20%26%20Analytics-005571?style=flat-square&logo=elasticsearch)
![Grafana](https://img.shields.io/badge/Grafana-Monitoring-F46800?style=flat-square&logo=grafana)
![Python](https://img.shields.io/badge/Python-Autoblock-3776AB?style=flat-square&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=flat-square&logo=ubuntu)

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

## 🎓 Context

Built for the **Advanced Security** course at [PXL Hogeschool](https://www.pxl.be), Hasselt — as part of the Graduaat Systeem en Netwerkbeheer program (2025–2026).
