"""
Analyzer Module

Analyzes Google Search Console data to identify content opportunities.
"""

import pandas as pd
from typing import List, Dict, Tuple
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class SearchConsoleAnalyzer:
    """Analyze search console data to identify opportunities."""
    
    def __init__(self, config: Dict):
        """
        Initialize analyzer with configuration.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        self.app_config = config.get('app', {})
        self.min_position = self.app_config.get('min_position', 10)
    
    def identify_opportunities(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Identify content opportunities from search console data.
        
        Args:
            df: DataFrame with search console data
            
        Returns:
            Tuple of (existing_opportunities, new_content_opportunities)
        """
        logger.info("Identifying content opportunities...")
        
        # Filter queries with position > min_position (beyond first page)
        opportunities = df[df['Position'] > self.min_position].copy()
        
        logger.info(f"Found {len(opportunities)} queries with position > {self.min_position}")
        
        # Sort by impressions (descending) to prioritize high-volume queries
        opportunities = opportunities.sort_values('Impressions', ascending=False)
        
        return opportunities
    
    def match_queries_to_urls(
        self, 
        queries_df: pd.DataFrame, 
        sitemap_urls: List[str]
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Match queries to existing URLs where applicable.
        
        Args:
            queries_df: DataFrame with search queries
            sitemap_urls: List of URLs from sitemap
            
        Returns:
            Tuple of (matched_queries, unmatched_queries)
        """
        logger.info("Matching queries to existing URLs...")
        
        matched_queries = []
        unmatched_queries = []
        
        # Create normalized URL dict for faster matching
        normalized_urls = {}
        for url in sitemap_urls:
            parsed = urlparse(url)
            path = parsed.path.lower().strip('/')
            normalized_urls[path] = url
        
        for _, row in queries_df.iterrows():
            query = row['Query'].lower()
            query_words = set(query.replace('-', ' ').split())
            
            matched = False
            best_match_url = None
            best_match_score = 0
            
            # Try to match query with URLs
            for norm_path, full_url in normalized_urls.items():
                path_words = set(norm_path.replace('-', ' ').replace('/', ' ').split())
                
                # Calculate matching score
                if path_words and query_words:
                    common_words = query_words.intersection(path_words)
                    score = len(common_words) / len(query_words)
                    
                    if score > 0.5 and score > best_match_score:
                        best_match_score = score
                        best_match_url = full_url
                        matched = True
            
            row_dict = row.to_dict()
            
            if matched and best_match_url:
                row_dict['matched_url'] = best_match_url
                row_dict['match_score'] = best_match_score
                matched_queries.append(row_dict)
            else:
                unmatched_queries.append(row_dict)
        
        matched_df = pd.DataFrame(matched_queries) if matched_queries else pd.DataFrame()
        unmatched_df = pd.DataFrame(unmatched_queries) if unmatched_queries else pd.DataFrame()
        
        logger.info(f"Matched {len(matched_df)} queries to existing URLs")
        logger.info(f"Found {len(unmatched_df)} queries without matching URLs (new content opportunities)")
        
        return matched_df, unmatched_df
    
    def calculate_opportunity_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate opportunity score for each query.
        
        Score based on:
        - Impressions (higher is better)
        - Position (closer to page 1 is better)
        - CTR (lower than expected is better - more room for improvement)
        
        Args:
            df: DataFrame with search console data
            
        Returns:
            DataFrame with added 'opportunity_score' column
        """
        df = df.copy()
        
        # Normalize metrics to 0-1 scale
        if len(df) > 0:
            # Impressions score (higher is better)
            max_impressions = df['Impressions'].max()
            if max_impressions > 0:
                df['impressions_score'] = df['Impressions'] / max_impressions
            else:
                df['impressions_score'] = 0
            
            # Position score (lower position is better, but we want queries closer to page 1)
            # Position 11-20 get higher scores than 21-30, etc.
            df['position_score'] = 1 / (df['Position'] - 10 + 1)
            df['position_score'] = df['position_score'] / df['position_score'].max()
            
            # CTR gap score (expected CTR vs actual CTR)
            # Expected CTR based on position (simplified model)
            expected_ctr = df['Position'].apply(self._expected_ctr_for_position)
            df['ctr_gap'] = expected_ctr - df['CTR']
            df['ctr_gap'] = df['ctr_gap'].clip(lower=0)  # Only positive gaps
            
            if df['ctr_gap'].max() > 0:
                df['ctr_gap_score'] = df['ctr_gap'] / df['ctr_gap'].max()
            else:
                df['ctr_gap_score'] = 0
            
            # Combined opportunity score (weighted average)
            df['opportunity_score'] = (
                df['impressions_score'] * 0.4 +
                df['position_score'] * 0.3 +
                df['ctr_gap_score'] * 0.3
            )
            
            # Sort by opportunity score
            df = df.sort_values('opportunity_score', ascending=False)
        else:
            df['opportunity_score'] = 0
        
        return df
    
    @staticmethod
    def _expected_ctr_for_position(position: float) -> float:
        """
        Calculate expected CTR based on position.
        
        Based on industry benchmarks (simplified).
        
        Args:
            position: Search result position
            
        Returns:
            Expected CTR as decimal
        """
        if position <= 1:
            return 0.30
        elif position <= 3:
            return 0.15
        elif position <= 5:
            return 0.08
        elif position <= 10:
            return 0.05
        elif position <= 20:
            return 0.02
        else:
            return 0.01
    
    def filter_high_potential_queries(
        self, 
        df: pd.DataFrame, 
        min_impressions: int = 10
    ) -> pd.DataFrame:
        """
        Filter for high-potential queries based on impressions and other metrics.
        
        Args:
            df: DataFrame with search console data
            min_impressions: Minimum impressions threshold
            
        Returns:
            Filtered DataFrame
        """
        filtered = df[df['Impressions'] >= min_impressions].copy()
        
        logger.info(f"Filtered to {len(filtered)} high-potential queries (min impressions: {min_impressions})")
        
        return filtered

