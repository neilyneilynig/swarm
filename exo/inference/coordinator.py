"""
Inference coordinator.

Handles distributed inference across multiple nodes by partitioning
model layers and coordinating execution.
"""

import asyncio
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass

from exo.discovery.service import PeerInfo

logger = logging.getLogger(__name__)


@dataclass
class LayerPartition:
    """Represents a partition of model layers assigned to a node."""
    
    node_id: str
    start_layer: int
    end_layer: int
    ip_address: str
    port: int
    

@dataclass
class ModelSpec:
    """Model specification."""
    
    name: str
    total_layers: int
    memory_per_layer_mb: float
    

class InferenceCoordinator:
    """
    Coordinates distributed inference across multiple nodes.
    
    Responsibilities:
    - Partition model layers across available nodes
    - Coordinate forward pass execution
    - Handle tensor transfer between nodes
    - Load balancing
    """
    
    # Model specifications (simplified for demo)
    MODELS = {
        "llama-7b": ModelSpec("llama-7b", 32, 500),
        "llama-13b": ModelSpec("llama-13b", 40, 650),
        "mistral-7b": ModelSpec("mistral-7b", 32, 500),
        "default": ModelSpec("default", 24, 400),
    }
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.current_partitions: List[LayerPartition] = []
        
    async def run_inference(
        self,
        prompt: str,
        model: str,
        peers: List[PeerInfo],
    ) -> str:
        """
        Run distributed inference.
        
        Args:
            prompt: Input prompt
            model: Model name
            peers: Available peer nodes
            
        Returns:
            Generated text
        """
        model_spec = self.MODELS.get(model, self.MODELS["default"])
        
        # Calculate partitioning
        partitions = self._partition_model(model_spec, peers)
        
        if not partitions:
            logger.warning("No partitions available, running locally")
            return await self._run_local_inference(prompt, model_spec)
        
        logger.info(f"Running distributed inference across {len(partitions)} nodes")
        for p in partitions:
            logger.info(f"  {p.node_id}: layers {p.start_layer}-{p.end_layer}")
        
        # Execute distributed inference
        result = await self._run_distributed_inference(prompt, model_spec, partitions)
        
        return result
        
    def _partition_model(
        self,
        model_spec: ModelSpec,
        peers: List[PeerInfo],
    ) -> List[LayerPartition]:
        """
        Partition model layers across available nodes.
        
        Uses a greedy algorithm based on available memory.
        """
        if not peers:
            return []
        
        # Add self to the pool
        all_nodes = [
            {"node_id": self.node_id, "memory_gb": 4.0, "ip": "localhost", "port": 5000}
        ] + [
            {"node_id": p.node_id, "memory_gb": p.memory_gb, "ip": p.ip_address, "port": p.port}
            for p in peers
        ]
        
        # Calculate layers per node based on memory
        total_memory = sum(n["memory_gb"] for n in all_nodes)
        total_layers = model_spec.total_layers
        
        partitions = []
        current_layer = 0
        
        for node in all_nodes:
            # Allocate layers proportional to memory
            memory_ratio = node["memory_gb"] / total_memory
            layers_for_node = max(1, int(total_layers * memory_ratio))
            
            # Don't exceed total layers
            layers_for_node = min(layers_for_node, total_layers - current_layer)
            
            if layers_for_node > 0:
                partitions.append(LayerPartition(
                    node_id=node["node_id"],
                    start_layer=current_layer,
                    end_layer=current_layer + layers_for_node - 1,
                    ip_address=node["ip"],
                    port=node["port"],
                ))
                current_layer += layers_for_node
            
            if current_layer >= total_layers:
                break
        
        return partitions
        
    async def _run_local_inference(self, prompt: str, model_spec: ModelSpec) -> str:
        """
        Run inference locally (fallback).
        
        This is a mock implementation for demonstration.
        In a real system, this would load and run the model.
        """
        logger.info(f"Running local inference with {model_spec.name}")
        
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Mock response
        return f"[Local inference on {self.node_id}] Response to: {prompt}"
        
    async def _run_distributed_inference(
        self,
        prompt: str,
        model_spec: ModelSpec,
        partitions: List[LayerPartition],
    ) -> str:
        """
        Run distributed inference across nodes.
        
        This is a mock implementation for demonstration.
        A real implementation would:
        1. Send embeddings to first node
        2. Pass hidden states between nodes
        3. Get final output from last node
        """
        logger.info(f"Starting distributed inference across {len(partitions)} nodes")
        
        # Simulate layer-by-layer execution
        current_hidden_state = f"embedding({prompt})"
        
        for partition in partitions:
            logger.info(
                f"Executing layers {partition.start_layer}-{partition.end_layer} "
                f"on {partition.node_id}"
            )
            
            # Simulate network transfer and computation
            await asyncio.sleep(0.2)
            
            # In reality, would send hidden_state to node and receive output
            current_hidden_state = f"output_from_{partition.node_id}"
        
        # Mock final response
        result = f"[Distributed inference across {len(partitions)} nodes] Response to: {prompt}"
        
        logger.info("Distributed inference complete")
        return result
        
    def get_partition_info(self) -> List[Dict]:
        """Get current partition information."""
        return [
            {
                "node_id": p.node_id,
                "layers": f"{p.start_layer}-{p.end_layer}",
                "endpoint": f"{p.ip_address}:{p.port}",
            }
            for p in self.current_partitions
        ]
