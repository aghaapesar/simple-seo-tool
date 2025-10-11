"""
Data Loader Module

Handles loading and parsing of Google Search Console Excel data and XML sitemaps.
"""

import pandas as pd
import requests
from lxml import etree
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and parse input data from Excel files and XML sitemaps."""
    
    def __init__(self, config: Dict):
        """
        Initialize DataLoader with configuration.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        self.app_config = config.get('app', {})
    
    def load_search_console_data(self, file_path: str) -> pd.DataFrame:
        """
        Load Google Search Console data from Excel file.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            DataFrame with columns: Query, Clicks, Impressions, CTR, Position
            
        Raises:
            FileNotFoundError: If Excel file doesn't exist
            ValueError: If required columns are missing
        """
        try:
            logger.info(f"Loading Search Console data from {file_path}")
            
            # Check if file exists
            if not Path(file_path).exists():
                raise FileNotFoundError(f"Excel file not found: {file_path}")
            
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Validate required columns
            required_columns = ['Query', 'Clicks', 'Impressions', 'CTR', 'Position']
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Define alternative column names for Google Search Console exports
            column_alternatives = {
                'Query': ['query', 'top queries', 'top query', 'search query', 'keyword'],
                'Clicks': ['clicks', 'click'],
                'Impressions': ['impressions', 'impression'],
                'CTR': ['ctr', 'click-through rate', 'clickthrough rate'],
                'Position': ['position', 'avg position', 'average position', 'avg. position']
            }
            
            # Try to map columns
            column_mapping = {}
            for req_col in required_columns:
                # Check if column exists as-is
                if req_col in df.columns:
                    continue
                
                # Try case-insensitive and alternative names
                alternatives = column_alternatives.get(req_col, [])
                for actual_col in df.columns:
                    actual_col_lower = actual_col.lower()
                    
                    # Check if matches any alternative
                    if actual_col_lower in alternatives or actual_col_lower == req_col.lower():
                        column_mapping[actual_col] = req_col
                        break
            
            # Apply column mapping
            if column_mapping:
                df = df.rename(columns=column_mapping)
            
            # Check for missing columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                available_cols = ', '.join(df.columns.tolist())
                raise ValueError(
                    f"Missing required columns: {', '.join(missing_columns)}\n"
                    f"Available columns: {available_cols}\n"
                    f"Please ensure your Excel file is exported from Google Search Console."
                )
            
            # Convert data types
            df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce').fillna(0).astype(int)
            df['Impressions'] = pd.to_numeric(df['Impressions'], errors='coerce').fillna(0).astype(int)
            df['CTR'] = pd.to_numeric(df['CTR'], errors='coerce').fillna(0).astype(float)
            df['Position'] = pd.to_numeric(df['Position'], errors='coerce').fillna(0).astype(float)
            
            # Remove rows with empty queries
            df = df[df['Query'].notna() & (df['Query'] != '')]
            
            logger.info(f"Successfully loaded {len(df)} queries from Search Console data")
            return df
            
        except Exception as e:
            logger.error(f"Error loading Search Console data: {str(e)}")
            raise
    
    def download_and_parse_sitemap(self, sitemap_url: Optional[str] = None) -> List[str]:
        """
        Download and parse XML sitemap to extract URLs.
        
        Args:
            sitemap_url: URL to XML sitemap (uses config if not provided)
            
        Returns:
            List of URLs from sitemap
            
        Raises:
            requests.RequestException: If sitemap download fails
            etree.XMLSyntaxError: If XML parsing fails
        """
        try:
            url = sitemap_url or self.app_config.get('sitemap_url')
            
            if not url:
                raise ValueError("No sitemap URL provided in config or parameters")
            
            logger.info(f"Downloading sitemap from {url}")
            
            # Download sitemap with timeout
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse XML
            root = etree.fromstring(response.content)
            
            # Handle different sitemap formats
            urls = []
            
            # Check for sitemap index (contains other sitemaps)
            sitemap_index_ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            sitemaps = root.xpath('//ns:sitemap/ns:loc/text()', namespaces=sitemap_index_ns)
            
            if sitemaps:
                logger.info(f"Found sitemap index with {len(sitemaps)} sitemaps")
                # Download each sitemap
                for sitemap_loc in sitemaps:
                    try:
                        sub_urls = self._parse_single_sitemap(sitemap_loc)
                        urls.extend(sub_urls)
                    except Exception as e:
                        logger.warning(f"Error parsing sitemap {sitemap_loc}: {str(e)}")
            else:
                # Single sitemap
                urls = self._parse_single_sitemap(url, response.content)
            
            logger.info(f"Successfully extracted {len(urls)} URLs from sitemap")
            return urls
            
        except requests.RequestException as e:
            logger.error(f"Error downloading sitemap: {str(e)}")
            raise
        except etree.XMLSyntaxError as e:
            logger.error(f"Error parsing sitemap XML: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing sitemap: {str(e)}")
            raise
    
    def _parse_single_sitemap(self, url: str, content: Optional[bytes] = None) -> List[str]:
        """
        Parse a single sitemap XML file.
        
        Args:
            url: URL of the sitemap
            content: Optional pre-downloaded content
            
        Returns:
            List of URLs from the sitemap
        """
        if content is None:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            content = response.content
        
        root = etree.fromstring(content)
        
        # Extract URLs with namespace handling
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        url_elements = root.xpath('//ns:url/ns:loc/text()', namespaces=namespaces)
        
        return url_elements
    
    def create_backup(self, file_path: str) -> str:
        """
        Create a backup of the input file.
        
        Args:
            file_path: Path to file to backup
            
        Returns:
            Path to backup file
        """
        try:
            source = Path(file_path)
            if not source.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            backup_path = source.parent / f"{source.stem}_backup{source.suffix}"
            
            # Copy file content
            import shutil
            shutil.copy2(source, backup_path)
            
            logger.info(f"Created backup: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            raise

