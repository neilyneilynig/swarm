# EXO Demos

Interactive demonstrations of EXO's distributed AI inference capabilities.

## Quick Start

```bash
# 1. Interactive tutorial
python quickstart.py

# 2. Multi-node simulation
python multinode_demo.py

# 3. Cluster visualization
python visualize_cluster.py

# 4. Terminal examples (for screenshots/docs)
bash terminal_examples.sh
```

## What Each Demo Shows

### `quickstart.py`
**Best for:** First-time users

Interactive walkthrough with live code execution:
- Creating and configuring nodes
- Starting the discovery service
- Checking cluster status
- Running inference

Press Enter to step through each section.

### `multinode_demo.py`
**Best for:** Understanding distribution

Simulates a 3-node cluster on one machine:
- Mac M1 (16GB)
- Mac Mini (8GB)
- Raspberry Pi (4GB)

Shows intelligent layer partitioning and cluster formation.

### `visualize_cluster.py`
**Best for:** Visual learners

ASCII art diagrams of:
- Cluster topology
- Layer distribution
- Network connections
- Cluster capabilities

### `terminal_examples.sh`
**Best for:** Documentation

Pre-formatted examples of all CLI commands with realistic output.
Perfect for screenshots and learning the commands.

## Requirements

All demos require:
- Python 3.9+
- Rich library (`pip install rich`)
- EXO installed (`pip install -e ..`)

## Tips

1. Run `multinode_demo.py` first to see everything in action
2. Use `visualize_cluster.py` to understand the architecture
3. Try `quickstart.py` for hands-on API learning
4. Check `terminal_examples.sh` for CLI reference

## Real Multi-Machine Testing

To test across real machines:

**Machine 1:**
```bash
cd ..
exo node --port 5000
```

**Machine 2:**
```bash
cd ..
exo node --port 5000
```

**Machine 3 (client):**
```bash
cd ..
exo discover
exo infer "Your prompt here"
```

See [../DEMO.md](../DEMO.md) for complete documentation.
