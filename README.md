# Raspberry Pi PLC Communication Setup

This project enables communication between a Raspberry Pi and a PLC using Ethernet. It requires setting a static IP for the Ethernet interface and setting up a Python virtual environment.

---

## 📍 1. Set a Static IP Address (Ethernet)

This project assumes the PLC uses IP `192.168.2.1`. The Raspberry Pi must be manually configured to be on the same subnet.

### Steps:

🛠️ Dual-NIC Configuration (Wi-Fi + Static Ethernet for PLC)

This setup configures:

- wlan0 for internet access (via DHCP)
- eth0 with a static IP (192.168.2.10) for direct communication with a PLC (192.168.2.1)

📋 Prerequisites

- Raspberry Pi OS or Debian-based distro using NetworkManager
- PLC connected directly via Ethernet cable to Raspberry Pi

🔧 Configuration Steps

1. Ensure eth0 is not managed by dhcpcd:
   Edit:
     sudo nano /etc/dhcpcd.conf
   Comment out or remove any 'interface eth0' section.

2. Identify the Ethernet connection name:
     ```Bash
     nmcli connection show
     ```

3. Set static IP for eth0 using NetworkManager:
   ```Bash
   sudo nmcli connection modify "Wired connection 1" \
      ipv4.addresses 192.168.2.10/24 \
      ipv4.method manual \
      connection.autoconnect yes
   ```

4. Activate the connection:
   ```Bash
   sudo nmcli connection up "Wired connection 1"
   ```

5. Verify:
   ```Bash
     ip a show eth0
     ping 192.168.2.1
   ```

The above setup is persistent across reboots and isolates PLC communication from internet traffic.

---

## 🐍 3. Python Virtual Environment Setup

After cloning the project:

```bash
git clone https://github.com/your-repo/plc-comm-test.git
cd plc-comm-test
```

### Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### To activate the venv in future sessions:

```bash
source .venv/bin/activate
```

---

## ✅ Final Notes

* Ensure the PLC is powered and reachable at `192.168.2.1`.
* Test connectivity:

  ```bash
  ping 192.168.2.1
  ```
* You may add an `activate.sh` script to simplify venv activation.