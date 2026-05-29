# Security Design Choices

## IDS vs IPS
We use autoblock.py for automated reactive blocking via iptables.

## Automated Response
The Python autoblock script reads `fast.log` in real-time.
When an "ET SCAN" signature is detected, the source IP is immediately
blocked via `iptables -A INPUT -s <IP> -j DROP`.

## Temporary vs Permanent Blocking
- `autoblock.py`: permanent block (survives script restart)
- `autoblock_reset.py`: temporary block with countdown timer
  → Recommended for demo/testing to avoid locking yourself out

## Why iptables?
iptables is low-level, fast, and available on all Linux systems.
No extra dependencies needed.

## Reporting
Bash script parses fast.log and outputs:
- `report.txt`: human-readable summary
## Alerting
Grafana sends automatic email alerts when Suricata events are detected.
The alert rule evaluates every minute and triggers when the event count
exceeds 0, sending an email notification with the summary
"POSSIBLE NMAP DETECTED!!!"
