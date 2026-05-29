# Configuration Guide

## Suricata

### Check your network interface

```bash
ip a
```

### Edit the Suricata config

```bash
sudo nano /etc/suricata/suricata.yaml
```

Set the correct interface name (replace `ens33` with your interface):

```yaml
af-packet:
  - interface: ens33
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes
    use-mmap: yes
    tpacket-v3: yes
    copy-mode: ips
    copy-iface: ens33
```

Test the configuration:

```bash
sudo suricata -T -c /etc/suricata/suricata.yaml -v
```

Restart after changes:

```bash
sudo systemctl restart suricata
```

### Eve.json output

Suricata is configured to write structured JSON logs to `eve.json`.
This is enabled by default in `/etc/suricata/suricata.yaml`:

```yaml
- eve-log:
    enabled: yes
    filetype: regular
    filename: /var/log/suricata/eve.json
```

### Log locations

| Log file | Purpose |
|---|---|
| `/var/log/suricata/fast.log` | Human-readable alerts, used by autoblock.py |
| `/var/log/suricata/eve.json` | Structured JSON output, used by Filebeat |

---

## Filebeat

Filebeat reads `eve.json` and ships the events directly to Elasticsearch.

The relevant section of `/etc/filebeat/filebeat.yml`:

```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/suricata/eve.json
    json.keys_under_root: true
    json.add_error_key: true

output.elasticsearch:
  hosts: ["localhost:9200"]
  preset: balanced
```

Key settings explained:

| Setting | Value | Purpose |
|---|---|---|
| `paths` | `/var/log/suricata/eve.json` | Reads Suricata JSON logs |
| `json.keys_under_root` | `true` | Promotes JSON fields to top level |
| `json.add_error_key` | `true` | Adds error field if JSON parsing fails |
| `hosts` | `localhost:9200` | Elasticsearch endpoint |

Restart Filebeat after changes:

```bash
sudo systemctl restart filebeat
```

Verify Filebeat is running:

```bash
sudo systemctl status filebeat
```

---

## Elasticsearch

Elasticsearch runs on `localhost:9200` and receives events from Filebeat.

Verify it is reachable:

```bash
curl http://localhost:9200
```

Expected output: a JSON response with cluster name and version info.

Check if Suricata events are being indexed:

```bash
curl http://localhost:9200/_cat/indices?v
```

---

## Grafana

Grafana runs on port `3000`.

### Connect Elasticsearch as datasource

1. Open your browser and go to `http://<defender-ip>:3000`
2. Login with credentials: `admin / admin`
3. Go to **Configuration → Data Sources → Add data source**
4. Select **Elasticsearch**
5. Set the URL to `http://localhost:9200`
6. Set the index name to `filebeat-*`
7. Click **Save & Test** — you should see "Index OK"

### Build a dashboard

1. Go to **Dashboards → New Dashboard**
2. Add a panel and select the Elasticsearch datasource
3. Query on fields like `alert.signature`, `src_ip`, `event_type`
4. Useful visualizations:
   - Time series of alerts over time
   - Table of top source IPs
   - Pie chart of alert types

---

## autoblock_reset.py

The blocking duration can be adjusted in the script:

```python
BLOCK_TIME = 60  # seconds before the IP is unblocked
```

The script monitors `fast.log` and blocks IPs that trigger `ET SCAN` signatures.

Run it with:

```bash
sudo python3 scripts/autoblock_reset.py
```

## Grafana Alerting

### Gmail App Password

Gmail requires an App Password instead of your regular password.
Regular passwords will not work due to Google's security policy.

To create an App Password:

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Go to **Security**
3. Enable **2-Step Verification** (required for App Passwords)
4. Search for **App Passwords** in the Google account search bar
5. Choose **App:** Mail, **Device:** Other → type "Grafana"
6. Click **Generate**
7. Copy the 16-character password
8. Use this password in `grafana.ini` as the `password` value

> **Note:** Never use your regular Gmail password in Grafana.
> App Passwords can be revoked at any time via your Google account.



Grafana is configured to send email alerts when a possible Nmap scan is detected.

### SMTP Configuration

Edit `/etc/grafana/grafana.ini` and remove the `;` from the following lines:

```ini
[smtp]
enabled = true
host = smtp.gmail.com:587
user = your email
password = your google apppass
from_address = your email
from_name = Grafana SOC Alert
```

Restart Grafana:

```bash
sudo systemctl restart grafana-server
```

### Alert Rule Configuration

- **Name:** SOC Alert NMAP
- **Datasource:** Elasticsearch
- **Query:** Count all events on `@timestamp`
- **Reduce:** Max, Drop Non-numeric Values
- **Threshold:** IS ABOVE 0
- **Evaluation:** Every 1m, Pending period 1m
- **Summary:** POSSIBLE NMAP DETECTED!!!

### Contact Point

- **Name:** SOC Alert
- **Type:** Email
- **Address:** your email

