#!/usr/bin/env python3
"""
EXO Quick Start Demo

Demonstrates the core features of EXO:
1. Start a node
2. Discover peers
3. Run inference
"""

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


async def demo():
    """Run the quick start demo."""
    
    # Header
    console.print(Panel.fit(
        "[bold green]⚡ EXO Quick Start Demo[/bold green]\n\n"
        "This demo shows how to:\n"
        "  1. Start an EXO compute node\n"
        "  2. Discover peers on the network\n"
        "  3. Run distributed inference",
        title="Welcome to EXO",
        border_style="green"
    ))
    
    console.print("\n[cyan]Press Enter to continue...[/cyan]")
    input()
    
    # Step 1: Import and create node
    console.print("\n[bold]Step 1: Create an EXO Node[/bold]\n")
    
    code1 = """from exo.node import Node, NodeConfig

# Create node configuration
config = NodeConfig(
    port=5000,
    auto_discover=True  # Enable automatic peer discovery
)

# Initialize node
node = Node(config)
print(f"Node created: {node.node_id}")
print(f"Device: {node.stats.device_type}")
print(f"Memory: {node.stats.memory_available_gb:.1f}GB")"""
    
    console.print(Syntax(code1, "python", theme="monokai", line_numbers=True))
    
    # Actually run it
    console.print("\n[dim]Running...[/dim]\n")
    from exo.node import Node, NodeConfig
    
    config = NodeConfig(port=5000, auto_discover=False)  # No discovery for demo
    node = Node(config)
    
    console.print(f"[green]✓[/green] Node created: [cyan]{node.node_id}[/cyan]")
    console.print(f"[green]✓[/green] Device: [yellow]{node.stats.device_type}[/yellow]")
    console.print(f"[green]✓[/green] Memory: [magenta]{node.stats.memory_available_gb:.1f}GB[/magenta] / {node.stats.memory_total_gb:.1f}GB")
    
    console.print("\n[cyan]Press Enter for next step...[/cyan]")
    input()
    
    # Step 2: Start the node
    console.print("\n[bold]Step 2: Start the Node[/bold]\n")
    
    code2 = """# Start the node
await node.start()

# Node is now:
# - Listening for connections
# - Announcing itself via mDNS
# - Ready to discover peers
# - Ready to run inference"""
    
    console.print(Syntax(code2, "python", theme="monokai", line_numbers=True))
    
    console.print("\n[dim]Starting node...[/dim]\n")
    await node.start()
    console.print("[green]✓[/green] Node started and ready")
    
    console.print("\n[cyan]Press Enter for next step...[/cyan]")
    input()
    
    # Step 3: Check cluster
    console.print("\n[bold]Step 3: Check Cluster Status[/bold]\n")
    
    code3 = """# Get cluster information
cluster = node.get_cluster_info()

print(f"Total nodes: {cluster['total_nodes']}")
print(f"Total memory: {cluster['total_memory_gb']}GB")
print(f"Peers: {len(cluster['peers'])}")"""
    
    console.print(Syntax(code3, "python", theme="monokai", line_numbers=True))
    
    console.print("\n[dim]Getting cluster info...[/dim]\n")
    cluster = node.get_cluster_info()
    
    console.print(f"[green]✓[/green] Total nodes: [cyan]{cluster['total_nodes']}[/cyan]")
    console.print(f"[green]✓[/green] Total memory: [magenta]{cluster['total_memory_gb']}GB[/magenta]")
    console.print(f"[green]✓[/green] Peers discovered: [yellow]{len(cluster['peers'])}[/yellow]")
    
    console.print("\n[cyan]Press Enter for next step...[/cyan]")
    input()
    
    # Step 4: Run inference
    console.print("\n[bold]Step 4: Run Distributed Inference[/bold]\n")
    
    code4 = """# Run inference across the cluster
result = await node.run_inference(
    prompt="Explain quantum computing in simple terms",
    model="llama-7b"
)

print(result)"""
    
    console.print(Syntax(code4, "python", theme="monokai", line_numbers=True))
    
    console.print("\n[dim]Running inference...[/dim]\n")
    
    with console.status("[bold cyan]Executing distributed inference...", spinner="dots"):
        result = await node.run_inference(
            prompt="Explain quantum computing in simple terms",
            model="default"
        )
    
    console.print("\n[green]✓[/green] Inference complete!\n")
    console.print(Panel(result, title="[green]Result[/green]", border_style="green"))
    
    console.print("\n[cyan]Press Enter to finish...[/cyan]")
    input()
    
    # Cleanup
    console.print("\n[bold]Step 5: Stop the Node[/bold]\n")
    
    code5 = """# Clean shutdown
await node.stop()"""
    
    console.print(Syntax(code5, "python", theme="monokai", line_numbers=True))
    
    console.print("\n[dim]Stopping node...[/dim]")
    await node.stop()
    console.print("[green]✓[/green] Node stopped cleanly\n")
    
    # Summary
    console.print(Panel.fit(
        "[bold green]Demo Complete! 🎉[/bold green]\n\n"
        "You've learned how to:\n"
        "  [green]✓[/green] Create and configure an EXO node\n"
        "  [green]✓[/green] Start the discovery service\n"
        "  [green]✓[/green] Check cluster status\n"
        "  [green]✓[/green] Run distributed inference\n\n"
        "[dim]Next: Try running multiple nodes and see them discover each other![/dim]",
        title="Summary",
        border_style="green"
    ))


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted[/yellow]")
        sys.exit(0)
