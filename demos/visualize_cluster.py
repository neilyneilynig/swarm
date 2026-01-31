#!/usr/bin/env python3
"""
Cluster Visualization Tool

Creates ASCII art visualization of the Swarm cluster topology,
showing nodes, connections, and layer distribution.
"""

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from rich.panel import Panel
from rich import box

from swarm.node import Node, NodeConfig

console = Console()


def create_cluster_diagram(nodes_info):
    """Create an ASCII diagram of the cluster."""
    
    diagram = []
    
    # Header
    diagram.append("┌" + "─" * 58 + "┐")
    diagram.append("│" + " " * 18 + "Swarm CLUSTER TOPOLOGY" + " " * 20 + "│")
    diagram.append("└" + "─" * 58 + "┘")
    diagram.append("")
    
    # Discovery layer
    diagram.append("        ┌────────────────────────────────┐")
    diagram.append("        │  Discovery Service (mDNS)      │")
    diagram.append("        │  Peer announcement & discovery │")
    diagram.append("        └──────────────┬─────────────────┘")
    diagram.append("                       │")
    
    # Nodes
    num_nodes = len(nodes_info)
    if num_nodes == 0:
        diagram.append("              No nodes detected")
    else:
        # Connection lines
        spacing = "       " if num_nodes == 2 else "   "
        if num_nodes == 1:
            diagram.append("                       │")
        elif num_nodes == 2:
            diagram.append("               ┌───────┴───────┐")
        else:
            diagram.append("          ┌────┴────┬────┴────┐")
        
        # Node boxes
        boxes = []
        for i, node in enumerate(nodes_info):
            box_lines = [
                "┌─────────────┐",
                f"│ {node['name'][:11]:^11} │",
                f"│ {node['device'][:11]:^11} │",
                f"│ {node['memory']:>4}GB RAM  │",
                f"│ Layers {node['layers']:>3}  │",
                "└─────────────┘"
            ]
            boxes.append(box_lines)
        
        # Print boxes side by side
        for line_idx in range(6):
            line_parts = []
            for box in boxes:
                line_parts.append(box[line_idx])
            diagram.append(spacing.join(line_parts))
        
        # Inter-node connections
        if num_nodes > 1:
            conn_line = "       │" + (" " * 12) + ("│" + (" " * 12)) * (num_nodes - 2) + "│"
            diagram.append(conn_line)
            diagram.append("       └" + "─" * (14 * num_nodes - 2) + "┘")
            diagram.append("              gRPC Communication")
            diagram.append("           (Hidden state transfer)")
    
    return "\n".join(diagram)


def create_layer_distribution_chart(nodes_info, total_layers=32):
    """Create a visual chart of layer distribution."""
    
    chart = []
    chart.append("Layer Distribution:")
    chart.append("")
    
    for node in nodes_info:
        start, end = node['layer_range']
        width = end - start + 1
        bar_length = int((width / total_layers) * 50)
        bar = "█" * bar_length
        percentage = (width / total_layers) * 100
        
        chart.append(f"{node['name']:12} [{start:2}-{end:2}] {bar} {percentage:5.1f}%")
    
    return "\n".join(chart)


async def main():
    """Run the cluster visualization."""
    
    console.print(Panel.fit(
        "[bold cyan]⚡ Swarm Cluster Visualization[/bold cyan]\n\n"
        "Visual representation of your distributed cluster",
        border_style="cyan"
    ))
    
    # For demo, create mock data
    # In real usage, would query actual nodes
    
    console.print("\n[dim]Scanning cluster...[/dim]\n")
    await asyncio.sleep(1)
    
    # Mock cluster data (would come from real discovery)
    nodes_info = [
        {
            "name": "Node-A",
            "device": "Mac M1",
            "memory": 16.0,
            "layers": "1-18",
            "layer_range": (1, 18)
        },
        {
            "name": "Node-B", 
            "device": "Mac Mini",
            "memory": 8.0,
            "layers": "19-27",
            "layer_range": (19, 27)
        },
        {
            "name": "Node-C",
            "device": "RPi 5",
            "memory": 4.0,
            "layers": "28-32",
            "layer_range": (28, 32)
        }
    ]
    
    # Cluster diagram
    diagram = create_cluster_diagram(nodes_info)
    console.print(Panel(diagram, border_style="green", title="[bold]Cluster Topology[/bold]"))
    
    console.print()
    
    # Layer distribution
    distribution = create_layer_distribution_chart(nodes_info)
    console.print(Panel(distribution, border_style="blue", title="[bold]Layer Partitioning (llama-7b)[/bold]"))
    
    console.print()
    
    # Summary statistics
    summary_table = Table(title="Cluster Summary", box=box.ROUNDED)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green", justify="right")
    
    total_memory = sum(n["memory"] for n in nodes_info)
    total_nodes = len(nodes_info)
    
    summary_table.add_row("Total Nodes", str(total_nodes))
    summary_table.add_row("Total Memory", f"{total_memory:.1f}GB")
    summary_table.add_row("Model Layers", "32")
    summary_table.add_row("Avg Layers/Node", f"{32/total_nodes:.1f}")
    summary_table.add_row("Network", "Gigabit Ethernet")
    summary_table.add_row("Status", "🟢 Healthy")
    
    console.print(summary_table)
    
    console.print()
    
    # Capabilities
    console.print(Panel.fit(
        "[bold green]Cluster Capabilities[/bold green]\n\n"
        "✓ Can run llama-7b (needs ~16GB)\n"
        "✓ Can run llama-13b (needs ~26GB)\n"
        "✓ Can run mistral-7b (needs ~14GB)\n"
        "✗ Cannot run llama-70b full precision (needs ~140GB)\n"
        "✓ Can run llama-70b with 4-bit quantization (needs ~35GB)\n\n"
        f"[dim]Current cluster: {total_memory:.0f}GB total memory[/dim]",
        border_style="cyan"
    ))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
