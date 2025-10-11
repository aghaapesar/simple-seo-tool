#!/usr/bin/env python3
"""
Test script for clustering functionality
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from ai_processor import AIProcessor
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def test_clustering():
    """Test the clustering functionality"""
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize AI processor
    ai_processor = AIProcessor(config)
    
    # Test keywords (Persian)
    test_keywords = [
        "کاشت گل",
        "نگهداری گیاهان",
        "گیاهان آپارتمانی",
        "کاشت سبزیجات",
        "طراحی باغ",
        "کود گیاهی",
        "آبیاری گیاهان",
        "تکثیر گل"
    ]
    
    print("🧪 Testing Persian keyword clustering...")
    print(f"Keywords: {test_keywords}")
    
    try:
        # Test clustering
        clusters = ai_processor.cluster_keywords(test_keywords)
        
        print(f"\n✅ Successfully created {len(clusters)} clusters:")
        
        for i, cluster in enumerate(clusters, 1):
            print(f"\n📁 Cluster {i}:")
            print(f"  Topic: {cluster.get('main_topic', 'N/A')}")
            print(f"  Title: {cluster.get('article_title', 'N/A')}")
            print(f"  Keywords: {cluster.get('keywords', [])}")
            print(f"  Headings: {len(cluster.get('h2_headings', []))} headings")
            print(f"  Type: {cluster.get('content_type', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_clustering()
    sys.exit(0 if success else 1)
