"""
Basic functionality test for EXO.

Run with: python test_basic.py
"""

import asyncio
import logging
from swarm.node import Node, NodeConfig

logging.basicConfig(level=logging.INFO)


async def test_node_startup():
    """Test basic node startup and shutdown."""
    print("Testing node startup...")
    
    config = NodeConfig(port=5001, auto_discover=False)
    node = Node(config)
    
    print(f"✓ Node created: {node.node_id}")
    print(f"✓ Device type: {node.stats.device_type}")
    print(f"✓ Memory: {node.stats.memory_available_gb:.1f}GB / {node.stats.memory_total_gb:.1f}GB")
    
    await node.start()
    print("✓ Node started")
    
    await asyncio.sleep(1)
    
    await node.stop()
    print("✓ Node stopped")


async def test_mock_inference():
    """Test mock inference."""
    print("\nTesting inference...")
    
    config = NodeConfig(port=5002, auto_discover=False)
    node = Node(config)
    
    await node.start()
    
    result = await node.run_inference("What is 2+2?", model="default")
    print(f"✓ Inference result: {result}")
    
    await node.stop()


async def test_cluster_info():
    """Test cluster information."""
    print("\nTesting cluster info...")
    
    config = NodeConfig(port=5003, auto_discover=False)
    node = Node(config)
    
    await node.start()
    
    info = node.get_cluster_info()
    print(f"✓ Cluster info: {info}")
    
    await node.stop()


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Swarm Basic Tests")
    print("=" * 60 + "\n")
    
    try:
        await test_node_startup()
        await test_mock_inference()
        await test_cluster_info()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
