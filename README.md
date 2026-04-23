# 🌐 SDN Traffic Control using POX Controller

A Software-Defined Networking (SDN) experiment that implements static routing and access control using the POX OpenFlow controller and Mininet network emulator.

---

## 👤 Author
- **Name:** Dhanush Sai Suprapadha
- **SRN:** PES2UG24CS154
- **Course:** Computer Networks Laboratory — PES University

---

## 📌 Overview

This project implements a custom POX controller module (`control_modes.py`) that performs MAC-based packet forwarding with three configurable traffic control modes. The network topology is emulated using Mininet with 4 hosts (h1, h2, h3, h4) connected through a single OpenFlow switch.

---

## 🗂️ File Structure

```
pox/
└── pox/
    └── control_modes.py   ← Custom POX controller module
```

---

## ⚙️ How It Works

The controller listens for `PacketIn` events from the switch. On each event it:

1. 📥 Learns the source MAC address and maps it to the incoming port
2. 🔍 Looks up the destination MAC in the table
3. 🚦 Applies the active MODE rule
4. 📤 Forwards or drops the packet accordingly

---

## 🚦 Traffic Control Modes

| Mode | Policy | Effect |
|------|--------|--------|
| 1️⃣ Mode 1 | h1 → only h2 allowed | Packets from h1 to h3/h4 are blocked |
| 2️⃣ Mode 2 | Allow everything | Full mesh connectivity, no restrictions |
| 3️⃣ Mode 3 | Block all from h1 | h1 is completely isolated from the network |

To switch modes, edit the `MODE` variable at the top of `control_modes.py`:

```python
MODE = 1   # Change to 1, 2, or 3
```

---

## 🧪 Experiment Results

### ✅ Mode 2 — Allow All
```
h1 -> h2  h3  h4
h2 -> h1  h3  h4
h3 -> h1  h2  h4
h4 -> h1  h2  h3
*** Results: 0% dropped (12/12 received)
```

### ⚠️ Mode 1 — h1 to h2 Only
```
h1 -> h2  h3  h4
h2 -> X   h3  h4
h3 -> X   h2  h4
h4 -> X   h2  h3
*** Results: 25% dropped (9/12 received)
```

### ❌ Mode 3 — Block All from h1
```
h1 -> X   X   X
h2 -> X   h3  h4
h3 -> X   h2  h4
h4 -> X   h2  h3
*** Results: 50% dropped (6/12 received)
```

---

## 🛠️ Setup and Run

### Prerequisites
- 🐍 Python 3.6–3.9 (recommended for POX)
- 📦 POX Controller (`pox` repository)
- 🖧 Mininet

### Steps

**1. Clone POX (if not already done)**
```bash
git clone https://github.com/noxrepo/pox.git
cd pox
```

**2. Place the module**
```bash
cp control_modes.py ~/pox/pox/
```

**3. Start the POX controller**
```bash
cd ~/pox
./pox.py control_modes
```

**4. In a separate terminal, start Mininet**
```bash
sudo mn --controller=remote --topo=single,4
```

**5. Test connectivity**
```
mininet> pingall
```

---

## 📋 Key Observations

- 🔄 MAC learning happens on first contact via flooding — mode rules only apply once the destination MAC is known
- 🚫 In Mode 3, h1 never gets to send a packet, so other hosts never learn h1's MAC — causing bidirectional isolation
- 📜 The POX terminal logs every blocked packet in real time (`MODE1 BLOCK: h1 → port X`)
- ✅ Regression test passed — routing behaviour is identical after controller restart

---

## 📡 Tech Stack

- **SDN Controller:** POX 0.7.0 (gar)
- **Protocol:** OpenFlow 1.0
- **Emulator:** Mininet
- **Language:** Python
