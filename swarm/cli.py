"""
Swarm CLI - Command-line interface for distributed AI inference.
"""

import asyncio
import click
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.logging import RichHandler

from swarm.node.node import Node, NodeConfig

console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, console=console)],
)

logger = logging.getLogger("swarm")


@click.group()
@click.version_option(version="0.1.0")
def main():
    """
    ⚡ Swarm - Distributed AI Inference

    Run large language models across multiple devices.
    """
    pass


@main.command()
@click.option("--port", default=5000, help="Port to listen on")
@click.option("--device-type", help="Device type (auto-detected if not specified)")
@click.option("--no-discover", is_flag=True, help="Disable auto-discovery")
def node(port: int, device_type: str, no_discover: bool):
    """Start an Swarm compute node."""

    config = NodeConfig(
        port=port,
        device_type=device_type,
        auto_discover=not no_discover,
    )

    node_instance = Node(config)

    # Display startup info
    console.print(
        Panel.fit(
            f"[bold green]⚡ Swarm Node Starting[/bold green]\n\n"
            f"Node ID: [cyan]{node_instance.node_id}[/cyan]\n"
            f"Device: [yellow]{node_instance.stats.device_type}[/yellow]\n"
            f"Memory: [magenta]{node_instance.stats.memory_available_gb:.1f}GB[/magenta] / "
            f"{node_instance.stats.memory_total_gb:.1f}GB\n"
            f"Port: [blue]{port}[/blue]\n"
            f"Auto-discovery: [green]{'ON' if not no_discover else 'OFF'}[/green]",
            title="Swarm Node",
        )
    )

    async def run():
        try:
            await node_instance.start()

            console.print("\n[green]✓[/green] Node started successfully")
            console.print("[dim]Press Ctrl+C to stop[/dim]\n")

            # Keep running and show updates
            while node_instance.running:
                await asyncio.sleep(5)

                # Show cluster status every 30 seconds
                if int(asyncio.get_event_loop().time()) % 30 == 0:
                    _display_cluster_status(node_instance)

        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down...[/yellow]")
        finally:
            await node_instance.stop()
            console.print("[green]✓[/green] Node stopped")

    asyncio.run(run())


@main.command()
@click.argument("prompt")
@click.option("--model", default="default", help="Model to use")
@click.option("--node-id", help="Specific node to connect to")
def infer(prompt: str, model: str, node_id: str):
    """Run inference with the given prompt."""

    console.print(f"\n[cyan]Prompt:[/cyan] {prompt}\n")

    async def run():
        # Create a client node
        config = NodeConfig(auto_discover=True)
        node_instance = Node(config)

        try:
            await node_instance.start()

            # Wait a bit for peer discovery
            console.print("[dim]Discovering peers...[/dim]")
            await asyncio.sleep(2)

            # Show cluster
            cluster = node_instance.get_cluster_info()
            console.print(
                f"[green]✓[/green] Found {cluster['total_nodes']} node(s) "
                f"with {cluster['total_memory_gb']}GB total memory\n"
            )

            # Run inference
            with console.status("[bold cyan]Running inference...", spinner="dots"):
                result = await node_instance.run_inference(prompt, model)

            # Display result
            console.print(
                Panel(
                    result,
                    title="[green]Result[/green]",
                    border_style="green",
                )
            )

        finally:
            await node_instance.stop()

    asyncio.run(run())


@main.command()
@click.option("--timeout", default=5, help="Discovery timeout in seconds")
def discover(timeout: int):
    """Discover available Swarm nodes on the network."""

    console.print(f"[cyan]Discovering nodes for {timeout} seconds...[/cyan]\n")

    async def run():
        config = NodeConfig(auto_discover=True)
        node_instance = Node(config)

        try:
            await node_instance.start()
            await asyncio.sleep(timeout)

            cluster = node_instance.get_cluster_info()

            # Display results
            table = Table(title="Discovered Nodes")
            table.add_column("Node ID", style="cyan")
            table.add_column("IP Address", style="magenta")
            table.add_column("Device", style="yellow")
            table.add_column("Memory (GB)", style="green", justify="right")

            # Add self
            table.add_row(
                f"{node_instance.node_id} (self)",
                "localhost",
                node_instance.stats.device_type,
                f"{node_instance.stats.memory_total_gb:.1f}",
            )

            # Add peers
            for peer in cluster["peers"]:
                table.add_row(
                    peer["node_id"],
                    peer["ip"],
                    peer["device"],
                    f"{peer['memory_gb']:.1f}",
                )

            console.print(table)
            console.print(
                f"\n[green]Total:[/green] {cluster['total_nodes']} nodes, "
                f"{cluster['total_memory_gb']:.1f}GB memory"
            )

        finally:
            await node_instance.stop()

    asyncio.run(run())


@main.command()
def status():
    """Show Swarm system status."""

    console.print(
        Panel.fit(
            "[bold green]⚡ Swarm - Distributed AI Inference[/bold green]\n\n"
            "Version: 0.1.0\n"
            "Status: Operational\n\n"
            "[dim]Use 'exo discover' to find nodes\n"
            "Use 'exo node' to start a compute node\n"
            "Use 'exo infer <prompt>' to run inference[/dim]",
            title="Swarm Status",
        )
    )


def _display_cluster_status(node: Node):
    """Display current cluster status."""
    cluster = node.get_cluster_info()

    console.print(f"\n[cyan]Cluster Status:[/cyan]")
    console.print(f"  Nodes: {cluster['total_nodes']}")
    console.print(f"  Total Memory: {cluster['total_memory_gb']}GB")

    if cluster["peers"]:
        console.print(f"  Peers: {', '.join(p['node_id'] for p in cluster['peers'])}")


if __name__ == "__main__":
    main()
