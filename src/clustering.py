"""
Clustering Module

Handles keyword clustering using both traditional ML methods and AI.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)


class KeywordClusterer:
    """Cluster keywords using various methods."""
    
    def __init__(self, config: Dict):
        """
        Initialize clusterer with configuration.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        self.app_config = config.get('app', {})
        self.clustering_threshold = self.app_config.get('clustering_threshold', 0.7)
    
    def preprocess_for_clustering(self, queries_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Preprocess queries for clustering.
        
        Args:
            queries_df: DataFrame with queries and metrics
            
        Returns:
            List of query dictionaries with metadata
        """
        queries_data = []
        
        for _, row in queries_df.iterrows():
            queries_data.append({
                'query': row['Query'],
                'impressions': row.get('Impressions', 0),
                'clicks': row.get('Clicks', 0),
                'position': row.get('Position', 0),
                'ctr': row.get('CTR', 0)
            })
        
        return queries_data
    
    def cluster_with_ml(self, queries: List[str]) -> List[List[str]]:
        """
        Cluster keywords using traditional ML (TF-IDF + DBSCAN).
        
        This is a fallback method when AI clustering is not available.
        
        Args:
            queries: List of search queries
            
        Returns:
            List of clusters (each cluster is a list of queries)
        """
        logger.info(f"Clustering {len(queries)} queries using ML method...")
        
        if len(queries) < 2:
            return [queries]
        
        try:
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 3),
                min_df=1,
                stop_words='english'
            )
            
            tfidf_matrix = vectorizer.fit_transform(queries)
            
            # Calculate similarity matrix
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Convert similarity to distance
            distance_matrix = 1 - similarity_matrix
            
            # Cluster using DBSCAN
            epsilon = 1 - self.clustering_threshold  # Convert similarity to distance threshold
            clusterer = DBSCAN(
                eps=epsilon,
                min_samples=2,
                metric='precomputed'
            )
            
            cluster_labels = clusterer.fit_predict(distance_matrix)
            
            # Group queries by cluster
            clusters_dict = {}
            for idx, label in enumerate(cluster_labels):
                if label not in clusters_dict:
                    clusters_dict[label] = []
                clusters_dict[label].append(queries[idx])
            
            # Convert to list of clusters (excluding noise cluster -1 if it exists)
            clusters = []
            for label, cluster_queries in clusters_dict.items():
                if label != -1:  # -1 is noise in DBSCAN
                    clusters.append(cluster_queries)
                else:
                    # Add noise points as individual clusters if they have high impressions
                    for query in cluster_queries:
                        clusters.append([query])
            
            logger.info(f"Created {len(clusters)} clusters using ML")
            return clusters
            
        except Exception as e:
            logger.error(f"Error in ML clustering: {str(e)}")
            # Fallback: return all queries as individual clusters
            return [[q] for q in queries]
    
    def merge_clusters_with_metadata(
        self,
        ai_clusters: List[Dict[str, Any]],
        queries_df: pd.DataFrame
    ) -> List[Dict[str, Any]]:
        """
        Merge AI cluster results with query metadata.
        
        Args:
            ai_clusters: Clusters from AI processor
            queries_df: Original DataFrame with query metrics
            
        Returns:
            Enhanced clusters with metadata
        """
        logger.info("Merging clusters with query metadata...")
        
        # Create query lookup dictionary
        query_data = {}
        for _, row in queries_df.iterrows():
            query_data[row['Query'].lower()] = {
                'impressions': row.get('Impressions', 0),
                'clicks': row.get('Clicks', 0),
                'position': row.get('Position', 0),
                'ctr': row.get('CTR', 0)
            }
        
        enhanced_clusters = []
        
        for cluster in ai_clusters:
            keywords = cluster.get('keywords', [])
            
            # Calculate aggregate metrics for cluster
            total_impressions = 0
            total_clicks = 0
            positions = []
            ctrs = []
            
            for keyword in keywords:
                kw_lower = keyword.lower()
                if kw_lower in query_data:
                    data = query_data[kw_lower]
                    total_impressions += data['impressions']
                    total_clicks += data['clicks']
                    if data['position'] > 0:
                        positions.append(data['position'])
                    if data['ctr'] > 0:
                        ctrs.append(data['ctr'])
            
            avg_position = np.mean(positions) if positions else 0
            avg_ctr = np.mean(ctrs) if ctrs else 0
            avg_impressions = total_impressions / len(keywords) if keywords else 0
            
            enhanced_cluster = {
                'main_topic': cluster.get('main_topic', 'Unknown'),
                'keywords': keywords,
                'suggested_title': cluster.get('suggested_title', ''),
                'h2_headings': cluster.get('h2_headings', []),
                'total_impressions': total_impressions,
                'avg_impressions': avg_impressions,
                'total_clicks': total_clicks,
                'avg_position': avg_position,
                'avg_ctr': avg_ctr,
                'keyword_count': len(keywords)
            }
            
            enhanced_clusters.append(enhanced_cluster)
        
        # Sort by total impressions (descending)
        enhanced_clusters.sort(key=lambda x: x['total_impressions'], reverse=True)
        
        logger.info(f"Enhanced {len(enhanced_clusters)} clusters with metadata")
        return enhanced_clusters
    
    def validate_clusters(self, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate and filter clusters based on quality criteria.
        
        Args:
            clusters: List of cluster dictionaries
            
        Returns:
            Filtered list of valid clusters
        """
        valid_clusters = []
        
        for cluster in clusters:
            # Validation criteria
            has_title = bool(cluster.get('suggested_title'))
            has_keywords = len(cluster.get('keywords', [])) >= 1  # At least 1 keyword
            has_headings = len(cluster.get('h2_headings', [])) >= 2  # At least 2 headings
            
            if has_title and has_keywords and has_headings:
                valid_clusters.append(cluster)
            else:
                logger.warning(f"Skipping invalid cluster: {cluster.get('main_topic', 'Unknown')}")
        
        logger.info(f"Validated {len(valid_clusters)} clusters out of {len(clusters)}")
        return valid_clusters
    
    def extract_top_clusters(
        self,
        clusters: List[Dict[str, Any]],
        top_n: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Extract top N clusters by impressions.
        
        Args:
            clusters: List of cluster dictionaries
            top_n: Number of top clusters to return
            
        Returns:
            Top N clusters
        """
        sorted_clusters = sorted(
            clusters,
            key=lambda x: x.get('total_impressions', 0),
            reverse=True
        )
        
        return sorted_clusters[:top_n]

