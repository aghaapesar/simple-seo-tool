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
        used_urls = set()  # Track URLs that have already been linked
        
        # Add links to sections with even distribution
        modified_sections = []
        
        # First pass: identify all potential link locations
        potential_links = []
        for i, section in enumerate(sections):
            if section['type'] == 'heading':
                continue  # Skip headings
            
            # Find best match for this section
            best_url = self._find_best_url_for_section(
                section['content'],
                priority_urls,
                link_distribution,
                max_links - len(potential_links)
            )
            
            if best_url and best_url.url not in used_urls:
                match_score = self._calculate_match_score(section['content'].lower(), best_url)
                potential_links.append({
                    'section_index': i,
                    'url': best_url,
                    'score': match_score,
                    'content': section['content']
                })
        
        # Sort by score (best matches first)
        potential_links.sort(key=lambda x: x['score'], reverse=True)
        
        # Select links with even distribution across content
        selected_links = self._select_links_with_even_distribution(
            potential_links, max_links, len(sections)
        )
        
        # Second pass: add selected links
        link_indices = {link['section_index'] for link in selected_links}
        
        for i, section in enumerate(sections):
            if section['type'] == 'heading':
                # Never add links to headings
                modified_sections.append(section['content'])
                continue
            
            if i in link_indices:
                # This section was selected for linking
                selected_link = next(link for link in selected_links if link['section_index'] == i)
                
                # Add link
                modified_content = self._add_link_to_section(
                    section['content'],
                    selected_link['url']
                )
                
                if modified_content != section['content']:
                    # Link was added
                    modified_sections.append(modified_content)
                    links_added += 1
                    link_distribution[selected_link['url'].url_type] += 1
                    used_urls.add(selected_link['url'].url)  # Mark URL as used
                    logger.info(f"      ✓ Added {selected_link['url'].url_type} link: {selected_link['url'].title[:40]}")
                    logger.debug(f"         URL: {selected_link['url'].url}")
                    logger.debug(f"         Match score: {selected_link['score']:.2f}")
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
        
        # Return best match if score is good enough (lowered threshold for more links)
        if scored_urls and scored_urls[0][0] > 0.15:
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
        
        # Check exact phrase matches first (highest priority)
        title_lower = url_item.title.lower()
        if title_lower in text:
            score += 0.8
        
        # Check if title words appear in text
        title_words = title_lower.split()
        for word in title_words:
            if len(word) > 2 and word in text:
                score += 0.3
        
        # Check if keywords appear in text
        for keyword in url_item.keywords:
            keyword_lower = keyword.lower()
            if len(keyword_lower) > 2:
                if keyword_lower in text:
                    score += 0.4
                # Partial word matches
                elif any(word in text for word in keyword_lower.split() if len(word) > 2):
                    score += 0.2
        
        # Check URL path for relevant terms
        url_path = url_item.url.lower()
        for word in title_words:
            if word in url_path and word in text:
                score += 0.2
        
        # Semantic similarity bonus for Persian content
        if self._has_semantic_similarity(text, url_item):
            score += 0.3
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def _has_semantic_similarity(self, text: str, url_item: URLItem) -> bool:
        """
        Check for semantic similarity between text and URL item.
        
        Args:
            text: Text content
            url_item: URL item
            
        Returns:
            True if semantically similar
        """
        # Common Persian word relationships
        semantic_groups = {
            'گل': ['گل', 'گیاه', 'کاشت', 'بذر', 'گلخانه', 'باغچه'],
            'بذر': ['بذر', 'کاشت', 'گیاه', 'گل', 'نهال', 'دانه'],
            'کاشت': ['کاشت', 'بذر', 'گیاه', 'گل', 'آبیاری', 'خاک'],
            'آبیاری': ['آبیاری', 'آب', 'گیاه', 'کاشت', 'باغچه'],
            'خاک': ['خاک', 'کاشت', 'گیاه', 'باغچه', 'کود'],
            'کود': ['کود', 'خاک', 'گیاه', 'کاشت', 'باغچه'],
            'باغچه': ['باغچه', 'گیاه', 'کاشت', 'آبیاری', 'خاک']
        }
        
        # Check if any semantic group appears in both text and URL
        for group_words in semantic_groups.values():
            text_has_group = any(word in text for word in group_words)
            title_has_group = any(word in url_item.title.lower() for word in group_words)
            
            if text_has_group and title_has_group:
                return True
        
        return False
    
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
        # Check if this URL is already linked in this section
        if url_item.url in section_html:
            logger.debug(f"      ⚠️  URL already exists in section, skipping: {url_item.url}")
            return section_html
        
        # Extract text content
        text = re.sub(r'<[^>]+>', '', section_html)
        
        # Find best anchor text (exact match or closest phrase, max 5 syllables)
        anchor_text = self._find_best_anchor_text(text, url_item)
        
        if not anchor_text:
            return section_html
        
        # Create link
        link_html = f'<a href="{url_item.url}">{anchor_text}</a>'
        
        # Replace first occurrence of anchor text that's not already in a link
        # Use word boundaries to avoid partial matches
        # Make sure we're not replacing text that's already inside an <a> tag
        pattern = r'(?<!</?a[^>]*>)\b' + re.escape(anchor_text) + r'\b(?![^<]*</a>)'
        modified_html = re.sub(pattern, link_html, section_html, count=1, flags=re.IGNORECASE)
        
        return modified_html
    
    def _find_best_anchor_text(
        self,
        text: str,
        url_item: URLItem,
        max_syllables: int = 5
    ) -> Optional[str]:
        """
        Find best anchor text with priority for product names (2-3 syllable words).
        
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
        
        # Priority: Product names (first 2-3 words, 2-3 syllables)
        title_words = url_item.title.split()
        text_lower = text.lower()
        
        # Try 2-3 syllable phrases first (product names)
        for word_count in [2, 3]:  # First 2-3 words are usually product name
            if len(title_words) >= word_count:
                phrase = ' '.join(title_words[:word_count])
                if phrase in text_lower:
                    match = re.search(re.escape(phrase), text, re.IGNORECASE)
                    if match:
                        return match.group(0)
        
        # Try semantic matches (2-3 syllable product words)
        best_semantic = self._find_semantic_anchor_text(text, title_words)
        if best_semantic:
            return best_semantic
        
        # Try keywords (prioritize longer ones)
        sorted_keywords = sorted(url_item.keywords, key=len, reverse=True)
        for keyword in sorted_keywords:
            if len(keyword) > 2 and keyword.lower() in text_lower:
                match = re.search(re.escape(keyword), text, re.IGNORECASE)
                if match:
                    return match.group(0)
        
        # Try 4-5 words if 2-3 didn't work
        for word_count in [4, 5]:
            if len(title_words) >= word_count:
                phrase = ' '.join(title_words[:word_count])
                if phrase in text_lower:
                    match = re.search(re.escape(phrase), text, re.IGNORECASE)
                    if match:
                        return match.group(0)
        
        # Fallback: fuzzy matching with title words
        text_words = text.split()
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
    
    def _find_semantic_anchor_text(self, text: str, title_words: list) -> Optional[str]:
        """
        Find semantic anchor text based on 2-3 syllable product words.
        
        Args:
            text: Text content
            title_words: Title words
            
        Returns:
            Best semantic anchor text or None
        """
        # Persian 2-3 syllable words that are likely product names
        product_words = {
            # 2 syllables
            'بذر', 'کاشت', 'آبیاری', 'گل', 'گیاه', 'خاک', 'کود', 'نهال', 
            'دانه', 'تخم', 'باغ', 'گلخانه', 'باغچه', 'بوته', 'شاخه',
            
            # 3 syllables  
            'پیاز', 'گوجه', 'هویج', 'کاهو', 'کلم', 'فلفل', 'خیار', 
            'بادمجان', 'کدو', 'اسفناج', 'جعفری', 'شوید', 'ریحان', 
            'نعناع', 'لیلیوم', 'بگونیا', 'آفتابگردان', 'گل‌رز', 'یاسمن'
        }
        
        # Check for high-priority product words
        for word in title_words:
            if word.lower() in product_words and word.lower() in text.lower():
                # Try to find phrase with this word
                word_index = title_words.index(word)
                # Try 2-word phrase starting with this word
                if word_index + 1 < len(title_words):
                    phrase = f"{word} {title_words[word_index + 1]}"
                    if phrase.lower() in text.lower():
                        match = re.search(re.escape(phrase), text, re.IGNORECASE)
                        if match:
                            return match.group(0)
                # Return just the word if no phrase found
                match = re.search(re.escape(word), text, re.IGNORECASE)
                if match:
                    return match.group(0)
        
        return None
    
    def _select_links_with_even_distribution(
        self, 
        potential_links: List[Dict], 
        max_links: int, 
        total_sections: int
    ) -> List[Dict]:
        """
        Select links with even distribution across content.
        
        Args:
            potential_links: List of potential link locations with scores
            max_links: Maximum number of links to add
            total_sections: Total number of content sections
            
        Returns:
            Selected links with even distribution
        """
        if not potential_links or max_links <= 0:
            return []
        
        selected = []
        used_indices = set()
        
        # Calculate target distribution
        target_spacing = total_sections / max_links if max_links > 0 else total_sections
        
        # Sort by score (best matches first)
        sorted_links = sorted(potential_links, key=lambda x: x['score'], reverse=True)
        
        for target_position in range(0, total_sections, int(target_spacing)):
            # Find best link near this position
            best_link = None
            best_distance = float('inf')
            
            for link in sorted_links:
                if link['section_index'] in used_indices:
                    continue
                
                distance = abs(link['section_index'] - target_position)
                if distance < best_distance:
                    best_distance = distance
                    best_link = link
            
            if best_link and len(selected) < max_links:
                selected.append(best_link)
                used_indices.add(best_link['section_index'])
        
        # If we still need more links, add the best remaining ones
        while len(selected) < max_links and len(selected) < len(potential_links):
            for link in sorted_links:
                if link['section_index'] not in used_indices:
                    selected.append(link)
                    used_indices.add(link['section_index'])
                    break
            else:
                break  # No more links available
        
        return selected
    
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

