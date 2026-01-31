# ⚡ EXO - Distributed AI Inference

**Run LLMs across multiple consumer devices. Turn your homelab into an AI supercomputer.**

Inspired by the original exo project, rebuilt from scratch with performance and simplicity in mind.

## 🎯 What is EXO?

EXO lets you pool computing resources across multiple machines to run large language models:
- Split models across Mac, Linux, Raspberry Pi, etc.
- Automatic peer discovery on your local network
- Dynamic load balancing
- Model layer partitioning

**Example:**
- MacBook M1 (16GB) → Runs layers 1-20
- Mac Mini M2 (8GB) → Runs layers 21-35
- Raspberry Pi 5 → Coordination & routing

## ✨ Features

- 🔍 **Auto-discovery** - Zero-config peer detection via mDNS
- 🧩 **Model partitioning** - Intelligent layer distribution
- ⚡ **Fast inference** - Optimized tensor transfer
- 🌐 **Multi-device** - Mac, Linux, RPi support
- 🔧 **CLI control** - Simple management interface

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Node A    │────▶│   Node B    │────▶│   Node C    │
│ Layers 1-10 │     │ Layers 11-20│     │ Layers 21-32│
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                  Discovery Service
```

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Start a node
exo node

# Discover peers (in another terminal)
exo discover

# Run inference
exo infer "Tell me about quantum computing"
```

## 📺 Demo

Check out the [interactive demos](demos/) to see EXO in action:

```bash
# Quick start tutorial
python demos/quickstart.py

# Multi-node simulation
python demos/multinode_demo.py

# Terminal examples
bash demos/terminal_examples.sh
```

### Example Output

```
$ exo discover --timeout 5

┏━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Node ID  ┃ IP Address  ┃ Device      ┃ Memory(GB) ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ a1b2c3d4 │ 192.168.1.5 │ mac_m_series│       16.0 │
│ e5f6g7h8 │ 192.168.1.8 │ raspberry_pi│        4.0 │
└──────────┴─────────────┴─────────────┴────────────┘

Total: 2 nodes, 20.0GB memory
```

## 📋 Requirements

- Python 3.9+
- 4GB+ RAM per node
- Local network connectivity

## 🛠️ Built With

- Python
- PyTorch
- gRPC (inter-node communication)
- mDNS (discovery)
- MLX (Mac acceleration)

---

**Status:** 🚧 Building from scratch
