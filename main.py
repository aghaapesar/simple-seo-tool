#!/usr/bin/env python3
"""
SEO Content Analysis & Optimization Tool

Main application entry point with two operational modes:
1. Content Optimization Mode: Analyze Search Console data for content improvements
2. SEO Data Collection Mode: Scrape page titles and meta tags from sitemaps

Features:
- Interactive file selection from input/ directory
- Interactive sitemap management with caching
- Test mode for quick validation
- Resume capability for interrupted operations
- Progress tracking with detailed status messages
"""

import sys
import yaml
import logging
import argparse
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm

# Import custom modules
from src.data_loader import DataLoader
from src.analyzer import SearchConsoleAnalyzer
from src.ai_processor import AIProcessor
from src.clustering import KeywordClusterer
from src.excel_writer import ExcelWriter
from src.sitemap_manager import SitemapManager
from src.file_selector import FileSelector
from src.page_scraper import PageScraper
from src.knowledge_base import KnowledgeBase


# Configure logging with detailed format
# Ensure logs directory exists
Path('logs').mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/seo_optimizer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def print_banner():
    """Display application banner."""
    print("\n" + "="*70)
    print("🚀 SEO CONTENT ANALYSIS & OPTIMIZATION TOOL")
    print("="*70)
    print("Version: 2.1 | Persian AI + Knowledge Base")
    print("="*70 + "\n")


def get_project_name_interactive() -> str:
    """
    Get project name from user interactively.
    
    Returns:
        Project name entered by user
    """
    print("\n" + "="*70)
    print("📋 PROJECT IDENTIFICATION")
    print("="*70)
    print("\nEnter a name for this project (e.g., website domain or brand name)")
    print("This will be used to track content history and avoid duplicates.")
    print("\nExamples:")
    print("  - example.com")
    print("  - my-website")
    print("  - blog-project")
    print("-"*70)
    
    while True:
        project_name = input("\nProject name: ").strip()
        
        if not project_name:
            print("❌ Project name cannot be empty. Please try again.")
            continue
        
        if len(project_name) < 3:
            print("❌ Project name must be at least 3 characters.")
            continue
        
        # Confirm with user
        print(f"\n✅ Project name: {project_name}")
        confirm = input("   Is this correct? (Y/n): ").strip().lower()
        
        if confirm not in ['n', 'no']:
            return project_name
        
        print("\n   Let's try again...")


def print_section(title: str, step: str = ""):
    """
    Print formatted section header.
    
    Args:
        title: Section title
        step: Optional step indicator (e.g., "1/7")
    """
    if step:
        print(f"\n{'='*70}")
        print(f"[{step}] {title}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'='*70}")
        print(f"{title}")
        print(f"{'='*70}\n")


class SEOContentOptimizer:
    """
    Main application class for SEO content optimization.
    
    Manages two operational modes:
    1. Content optimization using Search Console data
    2. SEO data collection from sitemaps
    """
    
    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize SEO Content Optimizer.
        
        Args:
            config_path: Path to YAML configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize core components
        self.data_loader = DataLoader(self.config)
        self.analyzer = SearchConsoleAnalyzer(self.config)
        self.ai_processor = AIProcessor(self.config)
        self.clusterer = KeywordClusterer(self.config)
        self.excel_writer = ExcelWriter(self.config)
        
        # Initialize new interactive components
        self.sitemap_manager = SitemapManager()
        self.file_selector = FileSelector()
        self.page_scraper = PageScraper()
        
        logger.info("✅ SEO Content Optimizer initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """
        Load and validate configuration from YAML file.
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
            
        Raises:
            SystemExit: If config file not found or invalid
        """
        try:
            config_file = Path(config_path)
            
            if not config_file.exists():
                logger.error(f"Configuration file not found: {config_path}")
                print(f"\n❌ Config file not found: {config_path}")
                print("   Please copy config.sample.yaml to config.yaml")
                sys.exit(1)
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            logger.info(f"📄 Configuration loaded from {config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            print(f"\n❌ Failed to load config: {str(e)}")
            sys.exit(1)
    
    def run_content_optimization(self, test_mode: bool = False):
        """
        Run content optimization workflow using Search Console data.
        
        This mode analyzes existing search performance and generates:
        1. Improvement suggestions for existing content
        2. New content ideas based on keyword clusters
        
        Args:
            test_mode: If True, limit processing to 10 queries for testing
        """
        print_banner()
        print("📊 MODE: Content Optimization & Analysis")
        
        try:
            # Step 1: Select Excel files
            print_section("Select Input Files", "1/7")
            selected_files = self.file_selector.select_files_interactive()
            
            if not selected_files:
                print("\n❌ No files selected. Exiting...")
                return
            
            # Step 2: Get sitemap configuration
            print_section("Sitemap Configuration", "2/7")
            sitemap_url = self.sitemap_manager.get_sitemap_url_interactive()
            sitemap_urls = self.sitemap_manager.download_and_parse_sitemap(sitemap_url)
            
            if not sitemap_urls:
                print("\n⚠️  No URLs extracted from sitemap. Continuing without URL matching...")
                sitemap_urls = []
            
            # Process each selected file
            for file_idx, excel_file in enumerate(selected_files, 1):
                print_section(f"Processing File: {excel_file.name}", f"{file_idx}/{len(selected_files)}")
                
                # Step 3: Load Search Console data
                print(f"\n[3/7] Loading Search Console data from {excel_file.name}...")
                search_data = self.data_loader.load_search_console_data(str(excel_file))
                
                # Apply test mode limit
                if test_mode:
                    search_data = search_data.head(10)
                    print(f"🧪 TEST MODE: Limited to {len(search_data)} queries")
                
                print(f"✅ Loaded {len(search_data)} queries")
                
                # Step 4: Identify opportunities
                print(f"\n[4/7] Identifying content opportunities...")
                opportunities = self.analyzer.identify_opportunities(search_data)
                opportunities = self.analyzer.calculate_opportunity_score(opportunities)
                opportunities = self.analyzer.filter_high_potential_queries(opportunities, min_impressions=10)
                
                print(f"✅ Found {len(opportunities)} high-potential opportunities")
                
                # Step 5: Match queries to URLs
                print(f"\n[5/7] Matching queries to existing URLs...")
                matched_queries, unmatched_queries = self.analyzer.match_queries_to_urls(
                    opportunities,
                    sitemap_urls
                )
                
                print(f"   📌 Matched to existing pages: {len(matched_queries)}")
                print(f"   ✨ New content opportunities: {len(unmatched_queries)}")
                
                # Step 6: Generate AI-powered improvements
                print(f"\n[6/7] Generating AI-powered suggestions...")
                
                improvements_data = []
                new_content_clusters = []
                
                # Process existing content improvements
                if len(matched_queries) > 0:
                    print(f"\n   🔄 Processing {len(matched_queries.groupby('matched_url'))} existing URLs...")
                    
                    url_groups = matched_queries.groupby('matched_url')
                    
                    for url, group in tqdm(url_groups, desc="   Analyzing pages"):
                        keywords = group['Query'].tolist()
                        avg_position = group['Position'].mean()
                        total_impressions = group['Impressions'].sum()
                        
                        # Get AI suggestions
                        ai_suggestions = self.ai_processor.generate_content_improvements(
                            url=url,
                            keywords=keywords,
                            position=avg_position,
                            impressions=total_impressions
                        )
                        
                        improvements_data.append({
                            'url': url,
                            'main_keyword': keywords[0] if keywords else '',
                            'position': avg_position,
                            'impressions': total_impressions,
                            'ai_suggestions': ai_suggestions
                        })
                    
                    print(f"   ✅ Generated {len(improvements_data)} improvement suggestions")
                
                # Process new content suggestions
                if len(unmatched_queries) > 0:
                    print(f"\n   🔄 Clustering {len(unmatched_queries)} keywords for new content...")
                    
                    new_content_keywords = unmatched_queries['Query'].tolist()
                    
                    # Cluster with AI
                    ai_clusters = self.ai_processor.cluster_keywords(new_content_keywords)
                    
                    # Merge with metadata
                    new_content_clusters = self.clusterer.merge_clusters_with_metadata(
                        ai_clusters,
                        unmatched_queries
                    )
                    
                    # Validate and filter
                    new_content_clusters = self.clusterer.validate_clusters(new_content_clusters)
                    new_content_clusters = self.clusterer.extract_top_clusters(new_content_clusters, top_n=50)
                    
                    print(f"   ✅ Created {len(new_content_clusters)} new content suggestions")
                
                # Step 7: Generate Excel reports
                print(f"\n[7/7] Generating Excel reports...")
                
                file_stem = excel_file.stem
                
                if improvements_data:
                    improvements_file = self.excel_writer.write_existing_content_improvements(
                        improvements_data,
                        filename=f"improvements_{file_stem}.xlsx"
                    )
                    print(f"   ✅ Created: {Path(improvements_file).name}")
                
                if new_content_clusters:
                    suggestions_file = self.excel_writer.write_new_content_suggestions(
                        new_content_clusters,
                        filename=f"new_content_{file_stem}.xlsx"
                    )
                    print(f"   ✅ Created: {Path(suggestions_file).name}")
                
                print(f"\n{'='*70}")
                print(f"✅ COMPLETED: {excel_file.name}")
                print(f"{'='*70}")
            
            # Final summary
            print_section("🎉 ALL FILES PROCESSED SUCCESSFULLY!")
            print(f"📁 Output directory: {self.excel_writer.output_dir.absolute()}")
            print(f"📊 Processed {len(selected_files)} file(s)")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Process interrupted by user")
            logger.info("Process interrupted by user")
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}", exc_info=True)
            print(f"\n\n❌ Fatal error: {str(e)}")
            sys.exit(1)
    
    def run_seo_data_collection(self, test_mode: bool = False):
        """
        Run SEO data collection mode to scrape page titles and meta tags.
        
        This mode:
        1. Downloads sitemap(s)
        2. Scrapes each URL for SEO data
        3. Saves results to separate Excel files per sitemap
        4. Supports resume functionality
        
        Args:
            test_mode: If True, limit to 10 pages per sitemap
        """
        print_banner()
        print("🔍 MODE: SEO Data Collection (Page Scraping)")
        
        if test_mode:
            print("🧪 TEST MODE ENABLED: Will scrape only 10 pages\n")
        
        try:
            # Step 1: Get sitemap configuration
            print_section("Sitemap Configuration", "1/2")
            sitemap_url = self.sitemap_manager.get_sitemap_url_interactive()
            sitemap_urls = self.sitemap_manager.download_and_parse_sitemap(sitemap_url)
            
            if not sitemap_urls:
                print("\n❌ No URLs found in sitemap. Exiting...")
                return
            
            # Step 2: Scrape pages
            print_section("Scraping SEO Data", "2/2")
            
            output_file = self.page_scraper.scrape_urls_batch(
                urls=sitemap_urls,
                sitemap_url=sitemap_url,
                test_mode=test_mode
            )
            
            # Final summary
            print_section("🎉 SCRAPING COMPLETED!")
            print(f"📁 Output file: {output_file.absolute()}")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Process interrupted by user")
            print("   You can resume by running the program again.")
            logger.info("Scraping interrupted by user")
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}", exc_info=True)
            print(f"\n\n❌ Fatal error: {str(e)}")
            sys.exit(1)


def select_mode_interactive() -> str:
    """
    Interactive mode selection.
    
    Returns:
        Selected mode: 'content' or 'scraping'
    """
    print_banner()
    print("Please select operational mode:\n")
    print("  [1] Content Optimization")
    print("      Analyze Search Console data for content improvements")
    print("      Input: Excel files from Google Search Console")
    print("      Output: Improvement suggestions + New content ideas\n")
    print("  [2] SEO Data Collection")
    print("      Scrape page titles and meta tags from sitemap")
    print("      Input: Sitemap URL")
    print("      Output: Excel with SEO data for all pages\n")
    print("-"*70)
    
    while True:
        choice = input("Your selection (1 or 2): ").strip()
        
        if choice == '1':
            return 'content'
        elif choice == '2':
            return 'scraping'
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")


def main():
    """Main entry point with enhanced argument parsing."""
    parser = argparse.ArgumentParser(
        description='SEO Content Analysis & Optimization Tool v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                  # Interactive mode selection
  %(prog)s --mode content                   # Content optimization mode
  %(prog)s --mode scraping                  # SEO data collection mode
  %(prog)s --mode content --test            # Test mode (10 items)
  %(prog)s --config custom_config.yaml      # Use custom config
        """
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['content', 'scraping'],
        help='Operational mode: content (optimization) or scraping (SEO data collection)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Enable test mode (process only 10 items for quick validation)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Check if config exists
    if not Path(args.config).exists():
        print(f"\n❌ Configuration file '{args.config}' not found")
        print("\n   Please create config.yaml based on config.sample.yaml")
        print("   Example: cp config.sample.yaml config.yaml\n")
        sys.exit(1)
    
    # Get mode (interactive or from args)
    mode = args.mode if args.mode else select_mode_interactive()
    
    # Initialize optimizer
    optimizer = SEOContentOptimizer(config_path=args.config)
    
    # Run selected mode
    if mode == 'content':
        optimizer.run_content_optimization(test_mode=args.test)
    elif mode == 'scraping':
        optimizer.run_seo_data_collection(test_mode=args.test)


if __name__ == "__main__":
    main()
