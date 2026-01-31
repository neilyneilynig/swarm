"""
Peer discovery service using mDNS/Zeroconf.

Automatically discovers other EXO nodes on the local network.
"""

import asyncio
import socket
from typing import Callable, Dict, Optional, Set
from dataclasses import dataclass
from zeroconf import ServiceBrowser, ServiceInfo, Zeroconf, ServiceStateChange
from zeroconf.asyncio import AsyncZeroconf, AsyncServiceBrowser
import logging

logger = logging.getLogger(__name__)


@dataclass
class PeerInfo:
    """Information about a discovered peer node."""
    
    node_id: str
    hostname: str
    ip_address: str
    port: int
    device_type: str
    memory_gb: float
    capabilities: Dict[str, any]
    

class DiscoveryService:
    """
    Discovers and announces EXO nodes on the local network.
    
    Uses mDNS (Zeroconf) for zero-config peer discovery.
    """
    
    SERVICE_TYPE = "_exo._tcp.local."
    
    def __init__(
        self,
        node_id: str,
        port: int,
        device_type: str = "unknown",
        memory_gb: float = 0.0,
        on_peer_added: Optional[Callable[[PeerInfo], None]] = None,
        on_peer_removed: Optional[Callable[[str], None]] = None,
    ):
        self.node_id = node_id
        self.port = port
        self.device_type = device_type
        self.memory_gb = memory_gb
        self.on_peer_added = on_peer_added
        self.on_peer_removed = on_peer_removed
        
        self.peers: Dict[str, PeerInfo] = {}
        self._zeroconf: Optional[AsyncZeroconf] = None
        self._service_info: Optional[ServiceInfo] = None
        self._browser: Optional[AsyncServiceBrowser] = None
        
    async def start(self):
        """Start the discovery service."""
        logger.info(f"Starting discovery service for node {self.node_id}")
        
        # Get local IP
        local_ip = self._get_local_ip()
        
        # Create service info
        self._service_info = ServiceInfo(
            self.SERVICE_TYPE,
            f"{self.node_id}.{self.SERVICE_TYPE}",
            addresses=[socket.inet_aton(local_ip)],
            port=self.port,
            properties={
                "node_id": self.node_id,
                "device_type": self.device_type,
                "memory_gb": str(self.memory_gb),
            },
            server=f"{self.node_id}.local.",
        )
        
        # Start Zeroconf
        self._zeroconf = AsyncZeroconf()
        await self._zeroconf.async_register_service(self._service_info)
        
        # Start browsing for peers
        self._browser = AsyncServiceBrowser(
            self._zeroconf.zeroconf,
            self.SERVICE_TYPE,
            handlers=[self._on_service_state_change],
        )
        
        logger.info(f"Discovery service started on {local_ip}:{self.port}")
        
    async def stop(self):
        """Stop the discovery service."""
        logger.info("Stopping discovery service")
        
        if self._browser:
            await self._browser.async_cancel()
        
        if self._zeroconf and self._service_info:
            await self._zeroconf.async_unregister_service(self._service_info)
            await self._zeroconf.async_close()
        
        logger.info("Discovery service stopped")
        
    def _on_service_state_change(
        self,
        zeroconf: Zeroconf,
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ):
        """Handle service state changes."""
        if state_change is ServiceStateChange.Added:
            asyncio.create_task(self._on_service_added(zeroconf, service_type, name))
        elif state_change is ServiceStateChange.Removed:
            self._on_service_removed(name)
            
    async def _on_service_added(self, zeroconf: Zeroconf, service_type: str, name: str):
        """Handle new service discovery."""
        info = await asyncio.get_event_loop().run_in_executor(
            None, zeroconf.get_service_info, service_type, name
        )
        
        if not info or not info.properties:
            return
        
        # Extract node info
        node_id = info.properties.get(b"node_id", b"unknown").decode()
        
        # Don't add ourselves
        if node_id == self.node_id:
            return
        
        # Skip if already known
        if node_id in self.peers:
            return
        
        device_type = info.properties.get(b"device_type", b"unknown").decode()
        memory_gb = float(info.properties.get(b"memory_gb", b"0").decode())
        
        # Get IP address
        ip_address = socket.inet_ntoa(info.addresses[0]) if info.addresses else "unknown"
        
        peer = PeerInfo(
            node_id=node_id,
            hostname=info.server.rstrip("."),
            ip_address=ip_address,
            port=info.port,
            device_type=device_type,
            memory_gb=memory_gb,
            capabilities={},
        )
        
        self.peers[node_id] = peer
        logger.info(f"Discovered peer: {node_id} at {ip_address}:{info.port}")
        
        if self.on_peer_added:
            self.on_peer_added(peer)
            
    def _on_service_removed(self, name: str):
        """Handle service removal."""
        # Extract node_id from service name
        node_id = name.split(".")[0]
        
        if node_id in self.peers:
            del self.peers[node_id]
            logger.info(f"Peer removed: {node_id}")
            
            if self.on_peer_removed:
                self.on_peer_removed(node_id)
    
    def get_peers(self) -> Dict[str, PeerInfo]:
        """Get all discovered peers."""
        return self.peers.copy()
    
    def _get_local_ip(self) -> str:
        """Get the local IP address."""
        try:
            # Create a socket to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
