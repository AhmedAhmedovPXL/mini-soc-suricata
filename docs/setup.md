# Setup Guide

## Requirements
- 2 VMs (Ubuntu 22.04/Kali)
- Network: Host-only or NAT network between VMs
- Python 3.x
- Suricata
- Elasticsearch
- Filebeat
- Grafana

## VM1 – Defender Setup

### 1. Install Suricata
```bash
sudo apt update
sudo apt install suricata -y
sudo systemctl enable suricata
sudo systemctl start suricata
```

### 2. Update Rules
```bash
sudo suricata-update
sudo systemctl restart suricata
```
### 3. Install Elasticsearch

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt install apt-transport-https -y
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update && sudo apt install elasticsearch -y
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
```

### 4. Install Filebeat

```bash
sudo apt install filebeat -y
sudo systemctl enable filebeat
sudo systemctl start filebeat
```

### 5. Install Grafana

```bash
sudo apt install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt update && sudo apt install grafana -y
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```







### 6. Clone Repository
```bash
git clone https://github.com/AhmedAhmedovPXL/mini-soc-suricata.git
cd mini-soc-suricata
```

### 7. Make scripts executable
```bash
chmod +x scripts/*.sh
```

## VM2 – Attacker Setup
```bash
sudo apt install nmap -y
```
