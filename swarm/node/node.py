"""
Swarm compute node.

Represents a single machine in the distributed inference cluster.
"""

import asyncio
import uuid
import platform
import psutil
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass, field

from swarm.discovery.service import DiscoveryService, PeerInfo
from swarm.inference.coordinator import InferenceCoordinator

logger = logging.getLogger(__name__)


@dataclass
class NodeConfig:
    """Node configuration."""
    
    port: int = 5000
    device_type: Optional[str] = None
    max_memory_gb: Optional[float] = None
    auto_discover: bool = True
    

@dataclass
class NodeStats:
    """Node statistics and capabilities."""
    
    cpu_count: int
    memory_total_gb: float
    memory_available_gb: float
    device_type: str
    platform: str
    has_gpu: bool = False
    gpu_memory_gb: float = 0.0
    

class Node:
    """
    Swarm compute node.
    
    Handles:
    - Peer discovery
    - Model layer execution
    - Inter-node communication
    - Load balancing
    """
    
    def __init__(self, config: Optional[NodeConfig] = None):
        self.config = config or NodeConfig()
        self.node_id = str(uuid.uuid4())[:8]
        
        # Get system stats
        self.stats = self._get_system_stats()
        
        # Services
        self.discovery: Optional[DiscoveryService] = None
        self.coordinator: Optional[InferenceCoordinator] = None
        
        # State
        self.running = False
        self.peers: Dict[str, PeerInfo] = {}
        
        logger.info(f"Node initialized: {self.node_id} ({self.stats.device_type})")
        logger.info(f"Memory: {self.stats.memory_available_gb:.1f}GB / {self.stats.memory_total_gb:.1f}GB")
        
    async def start(self):
        """Start the node."""
        if self.running:
            logger.warning("Node already running")
            return
        
        logger.info(f"Starting node {self.node_id}...")
        
        # Start discovery service
        if self.config.auto_discover:
            self.discovery = DiscoveryService(
                node_id=self.node_id,
                port=self.config.port,
                device_type=self.stats.device_type,
                memory_gb=self.stats.memory_total_gb,
                on_peer_added=self._on_peer_added,
                on_peer_removed=self._on_peer_removed,
            )
            await self.discovery.start()
        
        # Start coordinator
        self.coordinator = InferenceCoordinator(node_id=self.node_id)
        
        self.running = True
        logger.info(f"Node {self.node_id} started successfully")
        
    async def stop(self):
        """Stop the node."""
        if not self.running:
            return
        
        logger.info(f"Stopping node {self.node_id}...")
        
        if self.discovery:
            await self.discovery.stop()
        
        self.running = False
        logger.info(f"Node {self.node_id} stopped")
        
    async def run_inference(self, prompt: str, model: str = "default") -> str:
        """
        Run inference across the cluster.
        
        Args:
            prompt: Input prompt
            model: Model name to use
            
        Returns:
            Generated text
        """
        if not self.coordinator:
            raise RuntimeError("Node not started")
        
        logger.info(f"Running inference: '{prompt[:50]}...'")
        
        # Get available peers
        available_peers = list(self.peers.values()) if self.discovery else []
        
        # Run coordinated inference
        result = await self.coordinator.run_inference(
            prompt=prompt,
            model=model,
            peers=available_peers,
        )
        
        return result
        
    def get_cluster_info(self) -> Dict:
        """Get information about the cluster."""
        total_memory = self.stats.memory_total_gb
        total_nodes = 1
        
        if self.discovery:
            for peer in self.discovery.get_peers().values():
                total_memory += peer.memory_gb
                total_nodes += 1
        
        return {
            "node_id": self.node_id,
            "total_nodes": total_nodes,
            "total_memory_gb": round(total_memory, 2),
            "peers": [
                {
                    "node_id": peer.node_id,
                    "ip": peer.ip_address,
                    "device": peer.device_type,
                    "memory_gb": peer.memory_gb,
                }
                for peer in self.peers.values()
            ],
        }
    
    def _on_peer_added(self, peer: PeerInfo):
        """Handle peer discovery."""
        self.peers[peer.node_id] = peer
        logger.info(f"Peer connected: {peer.node_id} ({peer.device_type}) - {peer.memory_gb}GB")
        
    def _on_peer_removed(self, node_id: str):
        """Handle peer removal."""
        if node_id in self.peers:
            del self.peers[node_id]
            logger.info(f"Peer disconnected: {node_id}")
    
    def _get_system_stats(self) -> NodeStats:
        """Get system statistics."""
        memory = psutil.virtual_memory()
        
        # Detect device type
        device_type = self.config.device_type
        if not device_type:
            system = platform.system()
            machine = platform.machine()
            
            if system == "Darwin":
                if "arm" in machine.lower():
                    device_type = "mac_m_series"
                else:
                    device_type = "mac_intel"
            elif "arm" in machine.lower() or "aarch" in machine.lower():
                device_type = "raspberry_pi"
            else:
                device_type = "linux_x86"
        
        # Check for GPU (basic check)
        has_gpu = False
        gpu_memory = 0.0
        try:
            import torch
            if torch.cuda.is_available():
                has_gpu = True
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        except ImportError:
            pass
        
        return NodeStats(
            cpu_count=psutil.cpu_count(),
            memory_total_gb=memory.total / (1024**3),
            memory_available_gb=memory.available / (1024**3),
            device_type=device_type,
            platform=f"{platform.system()} {platform.release()}",
            has_gpu=has_gpu,
            gpu_memory_gb=gpu_memory,
        )
