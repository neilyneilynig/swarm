"""
Swarm - Distributed AI Inference

Run large language models across multiple consumer devices.
"""

__version__ = "0.1.0"

from swarm.node.node import Node
from swarm.discovery.service import DiscoveryService
from swarm.inference.coordinator import InferenceCoordinator

__all__ = ["Node", "DiscoveryService", "InferenceCoordinator"]
