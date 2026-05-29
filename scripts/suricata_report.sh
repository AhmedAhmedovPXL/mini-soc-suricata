#!/bin/bash
# =============================================================================
# suricata_report.sh
# -----------------------------------------------------------------------------
# Generates a security report from Suricata alert logs.
#
# Output:
#   - report.txt  : Human-readable summary of alerts
#   - alerts.csv  : CSV file for Grafana visualization
#
# Usage:
#   ./suricata_report.sh
#
# Requirements:
#   - Suricata running and logging to /var/log/suricata/fast.log
#   - awk, grep, sort available (standard on Ubuntu)
# =============================================================================

LOG="/var/log/suricata/fast.log"     # standaard locatie van Suricata fast-log
REPORT="report.txt"                  # menselijk leesbaar rapport
CSV="alerts.csv"                     # machine-leesbaar voor Grafana/Excel

# === Tekstueel rapport ===
echo "SURICATA SECURITY REPORT" > $REPORT
echo "Generated: $(date)" >> $REPORT
echo "=========================" >> $REPORT
echo "" >> $REPORT

# Total alerts
echo "Total alerts:" >> $REPORT

# wc -l telt het aantal regels; elke regel in fast.log = 1 alert
wc -l < $LOG >> $REPORT
echo "" >> $REPORT

# Top attack types
echo "Top attack types:" >> $REPORT
# Veldscheider '] ' splitst op de bracket na de timestamp
# $2 bevat dan de alert-naam tussen [** ... **]
# cut -d'[' -f1 verwijdert het deel vanaf de volgende [
# sort | uniq -c telt hoe vaak elk type voorkomt
# sort -nr sorteert numeriek aflopend, head pakt de top 10
awk -F'] ' '{print $2}' $LOG | cut -d'[' -f1 | sort | uniq -c | sort -nr | head >> $REPORT
echo "" >> $REPORT

# Top source IPs
echo "Top source IPs:" >> $REPORT

# grep -oP met regex \d+\.\d+\.\d+\.\d+ pakt alle IPv4-adressen
# (let op: ook destination IPs komen hierin terug, niet enkel source)
grep -oP '\d+\.\d+\.\d+\.\d+' $LOG | sort | uniq -c | sort -nr | head >> $REPORT
echo "" >> $REPORT

echo "Done. Report saved as $REPORT"

# === CSV output for Grafana 
# Columns: timestamp, alert_type, src_ip
echo "timestamp,alert_type,src_ip" > $CSV
awk -F'] ' '{
    # timestamp = eerste deel van logregel
    timestamp=$1
    # alert_type = tweede deel van logregel
    alert_type=$2
    # src_ip = eerste IPv4 in logregel
    match(alert_type, /[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/, ip)
    src_ip = ip[0]
    # clean alert_type van IP en haakjes
    gsub(/ *\[[^]]*\] */, "", alert_type)
    print timestamp "," alert_type "," src_ip
}' $LOG >> $CSV

echo "CSV saved as $CSV"
