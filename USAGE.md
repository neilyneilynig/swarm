# Swarm Usage Guide

## Installation

```bash
# Clone the repo
git clone https://github.com/neilyneilynig/exo.git
cd exo

# Install dependencies
pip install -e .

# For Mac with Apple Silicon
pip install -e ".[mac]"
```

## Quick Start

### 1. Start a Node

On each machine in your cluster:

```bash
swarm node
```

This will:
- Auto-detect your device type and available memory
- Start discovery service (mDNS)
- Listen for peer connections
- Announce itself to other nodes

### 2. Discover Peers

Check what nodes are available:

```bash
swarm discover --timeout 10
```

Output:
```
┏━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Node ID  ┃ IP Address  ┃ Device      ┃ Memory(GB) ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ a1b2c3d4 │ 192.168.1.5 │ mac_m_series│       16.0 │
│ e5f6g7h8 │ 192.168.1.8 │ raspberry_pi│        4.0 │
└──────────┴─────────────┴─────────────┴────────────┘
```

### 3. Run Inference

```bash
swarm infer "Explain quantum computing in simple terms"
```

Swarm will:
1. Discover available nodes
2. Partition the model across nodes based on memory
3. Run distributed inference
4. Return the result

## Advanced Usage

### Manual Node Configuration

```bash
# Specify port
swarm node --port 6000

# Specify device type
swarm node --device-type mac_m_series

# Disable auto-discovery
swarm node --no-discover
```

### Specify Model

```bash
swarm infer "Hello" --model llama-7b
```

Available models:
- `llama-7b` - 32 layers, ~16GB RAM needed
- `llama-13b` - 40 layers, ~26GB RAM needed
- `mistral-7b` - 32 layers, ~16GB RAM needed
- `default` - 24 layers, ~10GB RAM needed

## Example Setups

### Two-Machine Cluster

**Machine 1 (MacBook M1, 16GB)**
```bash
swarm node --port 5000
```

**Machine 2 (Mac Mini M2, 8GB)**
```bash
swarm node --port 5000
```

Swarm automatically discovers both nodes and distributes layers:
- MacBook M1: Layers 1-20 (66% of model)
- Mac Mini M2: Layers 21-32 (34% of model)

### Three-Machine Cluster with Raspberry Pi

**Machine 1 (Mac, 16GB)** → Primary compute
**Machine 2 (Linux, 8GB)** → Secondary compute  
**Machine 3 (RPi 5, 4GB)** → Coordination & light layers

Swarm distributes intelligently:
- Mac: Layers 1-18
- Linux: Layers 19-28
- RPi: Layers 29-32 + coordination

## Troubleshooting

### Nodes not discovering each other

1. Check firewall settings - port 5000 and mDNS must be open
2. Ensure all devices are on the same network
3. Try manual discovery: `swarm discover --timeout 15`

### Memory issues

```bash
# Check node memory
swarm node --help

# Use smaller model
swarm infer "test" --model default
```

### Network latency

- Use wired Ethernet instead of WiFi for better performance
- Place nodes with sequential layers on faster connections

## Architecture

```
┌──────────────────────────────────────────────────┐
│              Discovery Service (mDNS)            │
│           Announces & finds peer nodes           │
└──────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼───────┐
│   Node A     │ │   Node B    │ │   Node C    │
│ Layers 1-12  │ │ Layers 13-24│ │ Layers 25-32│
└──────┬───────┘ └──────┬──────┘ └──────┬──────┘
       │                │               │
       └────────────────┼───────────────┘
                  Tensor Transfer
                  (gRPC / HTTP)
```

## Performance Tips

1. **Use wired connections** - WiFi adds latency
2. **Match layer boundaries** - Let Swarm auto-partition
3. **Add more memory** - More nodes = bigger models
4. **GPU support** - Coming soon for Metal/CUDA acceleration

## Python API

```python
import asyncio
from swarm.node import Node, NodeConfig

async def main():
    # Create node
    config = NodeConfig(port=5000, auto_discover=True)
    node = Node(config)
    
    # Start
    await node.start()
    
    # Run inference
    result = await node.run_inference(
        prompt="What is the meaning of life?",
        model="llama-7b"
    )
    
    print(result)
    
    # Stop
    await node.stop()

asyncio.run(main())
```

## What's Next?

- [ ] Real model loading (currently mock)
- [ ] gRPC inter-node communication
- [ ] GPU support (Metal, CUDA)
- [ ] Model caching
- [ ] Quantization support
- [ ] Web dashboard
- [ ] Docker deployment

---

Built with ⚡ by Neil
