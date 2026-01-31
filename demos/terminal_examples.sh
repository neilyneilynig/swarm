#!/bin/bash
# Terminal Examples for Documentation Screenshots
# These commands demonstrate EXO features for documentation

set -e

echo "======================================"
echo "EXO Terminal Examples"
echo "======================================"
echo ""

# Example 1: Starting a node
echo "Example 1: Starting a Node"
echo "----------------------------"
echo ""
echo "$ exo node"
echo ""
cat << 'EOF'
┌─────────────────────────────────────────────┐
│            ⚡ EXO Node Starting            │
│                                             │
│ Node ID: a1b2c3d4                          │
│ Device: mac_m_series                       │
│ Memory: 14.2GB / 16.0GB                    │
│ Port: 5000                                 │
│ Auto-discovery: ON                         │
└─────────────────────────────────────────────┘

✓ Node started successfully
Press Ctrl+C to stop
EOF
echo ""
echo ""

# Example 2: Discovering peers
echo "Example 2: Discovering Peers"
echo "-----------------------------"
echo ""
echo "$ exo discover --timeout 5"
echo ""
cat << 'EOF'
Discovering nodes for 5 seconds...

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Node ID    ┃ IP Address   ┃ Device      ┃ Memory(GB) ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ a1b2c3d4   │ 192.168.1.5  │ mac_m_series│       16.0 │
│ e5f6g7h8   │ 192.168.1.8  │ mac_intel   │        8.0 │
│ i9j0k1l2   │ 192.168.1.12 │ raspberry_pi│        4.0 │
└────────────┴──────────────┴─────────────┴────────────┘

Total: 3 nodes, 28.0GB memory
EOF
echo ""
echo ""

# Example 3: Running inference
echo "Example 3: Running Inference"
echo "----------------------------"
echo ""
echo "$ exo infer \"What is quantum entanglement?\""
echo ""
cat << 'EOF'
Prompt: What is quantum entanglement?

Discovering peers...
✓ Found 3 node(s) with 28.0GB total memory

Running distributed inference...

Executing layers 1-18 on a1b2c3d4
Executing layers 19-27 on e5f6g7h8
Executing layers 28-32 on i9j0k1l2

┌──────────────────────────────────────────────┐
│                   Result                     │
├──────────────────────────────────────────────┤
│ Quantum entanglement is a phenomenon where   │
│ two particles become correlated in such a    │
│ way that the quantum state of one particle   │
│ cannot be described independently of the     │
│ other, even when separated by large          │
│ distances...                                 │
│                                              │
│ [Distributed inference across 3 nodes]       │
└──────────────────────────────────────────────┘
EOF
echo ""
echo ""

# Example 4: Cluster architecture
echo "Example 4: Cluster Architecture"
echo "--------------------------------"
echo ""
cat << 'EOF'
        Distributed Inference Flow
        
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Node A    │────▶│   Node B    │────▶│   Node C    │
│ Mac M1 16GB │     │ Mac Mini 8GB│     │ RPi 5 4GB   │
│             │     │             │     │             │
│ Layers 1-18 │     │ Layers 19-27│     │ Layers 28-32│
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
              mDNS Discovery Service
              (Zero-config networking)
              
Inference Request Flow:
1. User sends prompt to any node
2. Coordinator partitions model across cluster
3. Each node processes its assigned layers
4. Hidden states passed between nodes
5. Final result returned to user

Total Resources: 28GB RAM, 3 devices
Capable of running: llama-70b (with quantization)
EOF
echo ""
echo ""

# Example 5: Python API
echo "Example 5: Python API Usage"
echo "---------------------------"
echo ""
cat << 'EOF'
import asyncio
from exo.node import Node, NodeConfig

async def main():
    # Create and start node
    config = NodeConfig(port=5000, auto_discover=True)
    node = Node(config)
    await node.start()
    
    # Wait for peer discovery
    await asyncio.sleep(5)
    
    # Check cluster
    cluster = node.get_cluster_info()
    print(f"Cluster: {cluster['total_nodes']} nodes")
    print(f"Memory: {cluster['total_memory_gb']}GB")
    
    # Run inference
    result = await node.run_inference(
        prompt="Explain neural networks",
        model="llama-7b"
    )
    
    print(result)
    
    # Cleanup
    await node.stop()

asyncio.run(main())
EOF
echo ""
echo ""

echo "======================================"
echo "Screenshots generated!"
echo "Use 'script' or 'asciinema' to record"
echo "======================================"
