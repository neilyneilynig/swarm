"""
EXO - Distributed AI Inference

Run large language models across multiple consumer devices.
"""

__version__ = "0.1.0"

from exo.node.node import Node
from exo.discovery.service import DiscoveryService
from exo.inference.coordinator import InferenceCoordinator

__all__ = ["Node", "DiscoveryService", "InferenceCoordinator"]
