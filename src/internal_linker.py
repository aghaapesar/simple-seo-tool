"""
Internal Linker - Smart Internal Linking System

This module creates smart internal links in content based on sitemap URLs.

Features:
- Parse sitemaps to extract URLs and categorize them
- Add internal links based on semantic relevance
- Follow linking rules (1 link per 300-400 words, no links in headings, etc.)
- Support for blog posts, products, and product categories
- Semantic matching for anchor text
"""

import logging
import re
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote
import difflib

logger = logging.getLogger(__name__)


class URLItem:
    """Represents a URL from sitemap with metadata."""
    
    def __init__(self, url: str, url_type: str = 'unknown'):
        """
        Initialize URL item.
        
        Args:
            url: The URL
            url_type: Type of URL (blog, product, category, other)
        """
        self.url = url
        self.url_type = url_type
        self.title = self._extract_title_from_url(url)
        self.keywords = self._extract_keywords_from_url(url)
    
    def _extract_title_from_url(self, url: str) -> str:
        """Extract readable title from URL."""
        try:
            # Get path from URL
            parsed = urlparse(url)
            path = unquote(parsed.path)
            
            # Get last segment
            segments = [s for s in path.split('/') if s]
            if segments:
                title = segments[-1]
                # Remove file extensions
                title = re.sub(r'\.(html|htm|php)$', '', title)
                # Replace hyphens/underscores with spaces
                title = re.sub(r'[-_]', ' ', title)
                return title.strip()
            
            return url
            
        except Exception as e:
            logger.error(f"Error extracting title from URL: {e}")
            return url
    
    def _extract_keywords_from_url(self, url: str) -> List[str]:
        """Extract keywords from URL."""
        try:
            parsed = urlparse(url)
            path = unquote(parsed.path)
            
            # Split by common separators
            keywords = re.split(r'[/\-_]', path)
            
            # Clean and filter
            keywords = [k.strip() for k in keywords if k.strip()]
            keywords = [k for k in keywords if len(k) > 2]  # Remove very short words
            
            return keywords
            
        except Exception as e:
            logger.error(f"Error extracting keywords from URL: {e}")
            return []


class InternalLinker:
    """Creates smart internal links in content."""
    
    def __init__(self, sitemap_urls: List[str]):
        """
        Initialize Internal Linker.
        
        Args:
            sitemap_urls: List of URLs from sitemap
        """
        self.urls: List[URLItem] = []
        self._categorize_urls(sitemap_urls)
        
        logger.info(f"✅ Internal Linker initialized with {len(self.urls)} URLs")
    
    def _categorize_urls(self, urls: List[str]):
        """
        Categorize URLs into blog, product, category, etc.
        
        Args:
            urls: List of URL strings
        """
        for url in urls:
            url_type = self._determine_url_type(url)
            url_item = URLItem(url, url_type)
            self.urls.append(url_item)
        
        # Log statistics
        categories = {}
        for url_item in self.urls:
            categories[url_item.url_type] = categories.get(url_item.url_type, 0) + 1
        
        logger.info(f"   📊 URL Categories:")
        for cat, count in categories.items():
            logger.info(f"      - {cat}: {count}")
    
    def _determine_url_type(self, url: str) -> str:
        """
        Determine URL type based on patterns.
        
        Args:
            url: URL string
            
        Returns:
            URL type (blog, product, category, other)
        """
        url_lower = url.lower()
        
        # Persian and English patterns for categories
        category_patterns = [
            r'/category/',
            r'/cat/',
            r'/categories/',
            r'/دسته/',
            r'/دسته-بندی/',
            r'/product-category/',
            r'/shop/',
        ]
        
        # Product patterns
        product_patterns = [
            r'/product/',
            r'/محصول/',
            r'/p/',
        ]
        
        # Blog patterns
        blog_patterns = [
            r'/blog/',
            r'/post/',
            r'/article/',
            r'/مقاله/',
            r'/وبلاگ/',
        ]
        
        # Check patterns
        for pattern in category_patterns:
            if re.search(pattern, url_lower):
                return 'category'
        
        for pattern in product_patterns:
            if re.search(pattern, url_lower):
                return 'product'
        
        for pattern in blog_patterns:
            if re.search(pattern, url_lower):
                return 'blog'
        
        return 'other'
    
    def add_internal_links(
        self,
        content_html: str,
        max_links: Optional[int] = None,
        words_per_link: Tuple[int, int] = (300, 400)
    ) -> str:
        """
        Add internal links to HTML content.
        
        Args:
            content_html: HTML content
            max_links: Maximum number of links (if None, calculated from word count)
            words_per_link: Range for words per link (min, max)
            
        Returns:
            HTML content with internal links added
        """
        # Calculate word count
        text_only = re.sub(r'<[^>]+>', '', content_html)
        word_count = len(text_only.split())
        
        # Calculate max links if not provided
        if max_links is None:
            avg_words_per_link = sum(words_per_link) / 2
            max_links = int(word_count / avg_words_per_link)
        
        logger.info(f"   Adding up to {max_links} internal links to {word_count} words of content")
        
        # Get URLs by priority (categories > products > blogs)
        priority_urls = self._get_prioritized_urls()
        
        if not priority_urls:
            logger.warning("   No URLs available for linking")
            return content_html
        
        # Split content into sections (avoid links in headings)
        sections = self._split_content_into_sections(content_html)
        
        # Track added links
        links_added = 0
        link_distribution = {'category': 0, 'product': 0, 'blog': 0, 'other': 0}
        
        # Add links to sections
        modified_sections = []
        
        for section in sections:
            if section['type'] == 'heading':
                # Never add links to headings
                modified_sections.append(section['content'])
                continue
            
            # Try to add link to this section if we haven't reached max
            if links_added < max_links:
                # Find best match for this section
                best_url = self._find_best_url_for_section(
                    section['content'],
                    priority_urls,
                    link_distribution,
                    max_links - links_added
                )
                
                if best_url:
                    # Add link
                    modified_content = self._add_link_to_section(
                        section['content'],
                        best_url
                    )
                    
                    if modified_content != section['content']:
                        # Link was added
                        modified_sections.append(modified_content)
                        links_added += 1
                        link_distribution[best_url.url_type] += 1
                        logger.info(f"      ✓ Added {best_url.url_type} link: {best_url.title[:40]}")
                    else:
                        modified_sections.append(section['content'])
                else:
                    modified_sections.append(section['content'])
            else:
                modified_sections.append(section['content'])
        
        # Join sections
        result_html = '\n'.join(modified_sections)
        
        logger.info(f"   ✅ Added {links_added} internal links:")
        for link_type, count in link_distribution.items():
            if count > 0:
                logger.info(f"      - {link_type}: {count}")
        
        return result_html
    
    def _get_prioritized_urls(self) -> List[URLItem]:
        """
        Get URLs sorted by priority (categories first, then products, then blogs).
        
        Returns:
            Sorted list of URLItem objects
        """
        categories = [u for u in self.urls if u.url_type == 'category']
        products = [u for u in self.urls if u.url_type == 'product']
        blogs = [u for u in self.urls if u.url_type == 'blog']
        others = [u for u in self.urls if u.url_type == 'other']
        
        return categories + products + blogs + others
    
    def _split_content_into_sections(self, html: str) -> List[Dict[str, str]]:
        """
        Split HTML content into sections (headings and paragraphs).
        
        Args:
            html: HTML content
            
        Returns:
            List of section dictionaries with 'type' and 'content'
        """
        sections = []
        
        # Split by major tags
        parts = re.split(
            r'(<h[1-6][^>]*>.*?</h[1-6]>|<p[^>]*>.*?</p>|<ul[^>]*>.*?</ul>|<ol[^>]*>.*?</ol>|<div[^>]*>.*?</div>)',
            html,
            flags=re.DOTALL
        )
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Determine type
            if re.match(r'<h[1-6]', part, re.IGNORECASE):
                sections.append({'type': 'heading', 'content': part})
            elif re.match(r'<(p|ul|ol|div)', part, re.IGNORECASE):
                sections.append({'type': 'paragraph', 'content': part})
            else:
                # Plain text - wrap in paragraph
                if part.strip():
                    sections.append({'type': 'paragraph', 'content': f'<p>{part}</p>'})
        
        return sections
    
    def _find_best_url_for_section(
        self,
        section_html: str,
        urls: List[URLItem],
        current_distribution: Dict[str, int],
        remaining_slots: int
    ) -> Optional[URLItem]:
        """
        Find best URL to link in this section.
        
        Args:
            section_html: HTML content of section
            urls: Available URLs
            current_distribution: Current link type distribution
            remaining_slots: How many more links can be added
            
        Returns:
            Best matching URLItem or None
        """
        # Extract text from section
        text = re.sub(r'<[^>]+>', '', section_html).lower()
        
        # Calculate match scores for each URL
        scored_urls = []
        
        for url_item in urls:
            # Calculate semantic match score
            score = self._calculate_match_score(text, url_item)
            
            # Adjust score based on distribution (prefer underrepresented types)
            type_count = current_distribution.get(url_item.url_type, 0)
            
            # Bonus for categories (highest priority)
            if url_item.url_type == 'category':
                score *= 1.5
            
            # Penalty if this type already has many links
            if type_count > remaining_slots / 3:
                score *= 0.5
            
            scored_urls.append((score, url_item))
        
        # Sort by score
        scored_urls.sort(key=lambda x: x[0], reverse=True)
        
        # Return best match if score is good enough
        if scored_urls and scored_urls[0][0] > 0.3:
            return scored_urls[0][1]
        
        return None
    
    def _calculate_match_score(self, text: str, url_item: URLItem) -> float:
        """
        Calculate how well a URL matches the text content.
        
        Args:
            text: Text content (lowercase)
            url_item: URL item to match
            
        Returns:
            Match score (0.0 to 1.0)
        """
        score = 0.0
        
        # Check if title words appear in text
        title_words = url_item.title.lower().split()
        for word in title_words:
            if len(word) > 2 and word in text:
                score += 0.2
        
        # Check if keywords appear in text
        for keyword in url_item.keywords:
            keyword_lower = keyword.lower()
            if len(keyword_lower) > 2 and keyword_lower in text:
                score += 0.15
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def _add_link_to_section(
        self,
        section_html: str,
        url_item: URLItem
    ) -> str:
        """
        Add a link to the section.
        
        Args:
            section_html: HTML content of section
            url_item: URL item to link
            
        Returns:
            Modified HTML with link added
        """
        # Extract text content
        text = re.sub(r'<[^>]+>', '', section_html)
        
        # Find best anchor text (exact match or closest phrase, max 5 syllables)
        anchor_text = self._find_best_anchor_text(text, url_item)
        
        if not anchor_text:
            return section_html
        
        # Create link
        link_html = f'<a href="{url_item.url}">{anchor_text}</a>'
        
        # Replace first occurrence of anchor text
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(anchor_text) + r'\b'
        modified_html = re.sub(pattern, link_html, section_html, count=1, flags=re.IGNORECASE)
        
        return modified_html
    
    def _find_best_anchor_text(
        self,
        text: str,
        url_item: URLItem,
        max_syllables: int = 5
    ) -> Optional[str]:
        """
        Find best anchor text in the text for this URL.
        
        Args:
            text: Text content
            url_item: URL item
            max_syllables: Maximum syllables (approximately 5 words for Persian)
            
        Returns:
            Best anchor text or None
        """
        # First, try exact title match
        if url_item.title.lower() in text.lower():
            # Find the actual case-preserved match
            match = re.search(re.escape(url_item.title), text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        # Try keywords
        for keyword in url_item.keywords:
            if len(keyword) > 2 and keyword.lower() in text.lower():
                match = re.search(re.escape(keyword), text, re.IGNORECASE)
                if match:
                    return match.group(0)
        
        # Try fuzzy matching with title words
        title_words = url_item.title.split()
        text_words = text.split()
        
        # Find closest matching phrase (up to 5 words)
        best_match = None
        best_ratio = 0.0
        
        for i in range(len(text_words)):
            for length in range(1, min(6, len(text_words) - i + 1)):
                phrase = ' '.join(text_words[i:i+length])
                
                # Check similarity with title
                ratio = difflib.SequenceMatcher(None, phrase.lower(), url_item.title.lower()).ratio()
                
                if ratio > best_ratio and ratio > 0.6:
                    best_ratio = ratio
                    best_match = phrase
        
        return best_match
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about available URLs.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_urls': len(self.urls),
            'by_type': {},
            'sample_urls': {}
        }
        
        for url_item in self.urls:
            url_type = url_item.url_type
            stats['by_type'][url_type] = stats['by_type'].get(url_type, 0) + 1
            
            # Add sample URL
            if url_type not in stats['sample_urls']:
                stats['sample_urls'][url_type] = []
            
            if len(stats['sample_urls'][url_type]) < 3:
                stats['sample_urls'][url_type].append({
                    'url': url_item.url,
                    'title': url_item.title
                })
        
        return stats

