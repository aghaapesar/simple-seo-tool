"""
AI Processor Module

Handles AI integration for content suggestions using multiple providers.
Supports OpenAI, Azure OpenAI, Anthropic, and OpenAI-compatible endpoints.
"""

import json
import time
import logging
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp
from openai import OpenAI, AzureOpenAI
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class AIProcessor:
    """Process content suggestions using AI with multi-provider support."""
    
    def __init__(self, config: Dict):
        """
        Initialize AI processor with configuration.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        self.ai_config = config.get('ai', {})
        self.provider = self.ai_config.get('provider', 'openai_compatible')
        self.model = self.ai_config.get('model', 'gpt-4o-mini')
        self.temperature = self.ai_config.get('temperature', 0.0)
        self.timeout = self.ai_config.get('timeout_seconds', 60)
        self.max_retries = self.ai_config.get('max_retries', 3)
        self.retry_base_delay = self.ai_config.get('retry_base_delay', 1.5)
        self.qps = self.ai_config.get('qps', 1.0)
        self.response_json = self.ai_config.get('response_json', True)
        
        # Initialize client based on provider
        self.client = self._initialize_client()
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0 / self.qps if self.qps > 0 else 0
    
    def _initialize_client(self):
        """Initialize AI client based on provider configuration."""
        try:
            if self.provider == 'openai':
                api_key = self.ai_config.get('openai_api_key')
                base_url = self.ai_config.get('openai_base_url')
                return OpenAI(api_key=api_key, base_url=base_url)
                
            elif self.provider == 'azure':
                api_key = self.ai_config.get('azure_api_key')
                endpoint = self.ai_config.get('azure_endpoint')
                api_version = self.ai_config.get('azure_api_version')
                return AzureOpenAI(
                    api_key=api_key,
                    api_version=api_version,
                    azure_endpoint=endpoint
                )
                
            elif self.provider == 'anthropic':
                api_key = self.ai_config.get('anthropic_api_key')
                return Anthropic(api_key=api_key)
                
            elif self.provider == 'openai_compatible':
                api_key = self.ai_config.get('compatible_api_key')
                base_url = self.ai_config.get('compatible_base_url')
                return OpenAI(api_key=api_key, base_url=base_url)
            
            else:
                raise ValueError(f"Unsupported AI provider: {self.provider}")
                
        except Exception as e:
            logger.error(f"Error initializing AI client: {str(e)}")
            raise
    
    def _rate_limit(self):
        """Implement rate limiting for API calls."""
        if self.min_request_interval > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_request_interval:
                time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _call_api_with_retry(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Call AI API with retry logic.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            AI response text
        """
        for attempt in range(self.max_retries):
            try:
                self._rate_limit()
                
                if self.provider == 'anthropic':
                    return self._call_anthropic(prompt, system_prompt)
                else:
                    return self._call_openai_compatible(prompt, system_prompt)
                    
            except Exception as e:
                logger.warning(f"API call attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    delay = self.retry_base_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"All {self.max_retries} attempts failed")
                    raise
    
    def _call_openai_compatible(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call OpenAI-compatible API."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        # Build request parameters
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "timeout": self.timeout
        }
        
        # Add JSON mode if supported and requested
        if self.response_json and self.provider in ['openai', 'openai_compatible']:
            params["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**params)
        
        return response.choices[0].message.content
    
    def _call_anthropic(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Anthropic Claude API."""
        params = {
            "model": self.model,
            "max_tokens": 4096,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            params["system"] = system_prompt
        
        response = self.client.messages.create(**params)
        
        return response.content[0].text
    
    def cluster_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Cluster keywords into thematic groups for content creation.
        
        Args:
            keywords: List of search queries to cluster
            
        Returns:
            List of cluster dictionaries with structure:
            {
                "main_topic": str,
                "keywords": List[str],
                "suggested_title": str,
                "h2_headings": List[str]
            }
        """
        logger.info(f"Clustering {len(keywords)} keywords using AI...")
        
        # Prepare prompt
        keywords_list = "\n".join([f"- {kw}" for kw in keywords[:100]])  # Limit to avoid token issues
        
        system_prompt = """شما یک متخصص استراتژی محتوای SEO برای زبان فارسی هستید. وظیفه شما گروه‌بندی کوئری‌های جستجو در کلاسترهای موضوعی است که برای تولید مقالات مجزا منطقی باشند. 

**نکات مهم:**
- تمام خروجی‌ها باید کاملاً به زبان فارسی باشند
- از کلمات انگلیسی استفاده نکنید
- به الگوهای جستجوی فارسی و نگارش‌های مختلف توجه کنید
- intent کاربران ایرانی را در نظر بگیرید
- خروجی را فقط به صورت JSON معتبر برگردانید"""
        
        prompt = f"""**تحلیل کوئری‌های جستجو و تولید کلاسترهای محتوایی:**

**کوئری‌های ورودی:**
{keywords_list}

**وظیفه:**
این کوئری‌های جستجو را بر اساس تشابه معنایی و intent کاربر در کلاسترهای موضوعی گروه‌بندی کن. برای هر کلاستر، اطلاعات زیر را تولید کن:

1. **موضوع اصلی کلاستر** (به فارسی)
2. **کلیدواژه‌های مرتبط** از لیست ورودی
3. **عنوان پیشنهادی مقاله (H1)** - بهینه شده برای SEO فارسی، حداکثر ۶۰ کاراکتر
4. **ساختار هدینگ‌های H2** - بین ۵ تا ۸ عنوان، به فارسی و مطابق با search intent
5. **متا دیسکریپشن** - حداکثر ۱۶۰ کاراکتر، جذاب و شامل کلیدواژه اصلی
6. **نوع محتوا** - یکی از: راهنما/آموزش/مقایسه/لیست/تحلیل/نقد/بررسی
7. **Search Intent** - یکی از: اطلاعاتی/تجاری/معاملاتی/ناوبری

**فرمت خروجی JSON (فقط این خروجی را برگردان):**
{{
  "clusters": [
    {{
      "main_topic": "موضوع اصلی به فارسی",
      "keywords": ["کلیدواژه۱", "کلیدواژه۲"],
      "article_title": "عنوان مقاله بهینه شده برای SEO",
      "meta_description": "توضیحات متا جذاب و کوتاه",
      "h2_headings": ["هدینگ ۱", "هدینگ ۲", "هدینگ ۳"],
      "content_type": "راهنما",
      "search_intent": "اطلاعاتی",
      "recommended_word_count": 1500,
      "target_audience": "مخاطبان ایرانی",
      "content_focus": "تمرکز بر نیازهای کاربران فارسی‌زبان"
    }}
  ]
}}

**نکات مهم:**
- تعداد کلاسترها را بر اساس تشابه معنایی تعیین کن (نه تعداد ثابت)
- هر کلیدواژه فقط در یک کلاستر باشد
- حداقل ۲ کلیدواژه در هر کلاستر، اما کیفیت مهم‌تر از تعداد است
- در هدینگ‌ها به الگوهای جستجوی فارسی توجه کن
- فقط کلیدواژه‌های لیست ورودی را استفاده کن"""
        
        try:
            response = self._call_api_with_retry(prompt, system_prompt)
            
            # Parse JSON response
            result = json.loads(response)
            clusters = result.get('clusters', [])
            
            # Validate and enhance clusters
            enhanced_clusters = []
            for cluster in clusters:
                # Ensure required fields exist
                enhanced_cluster = {
                    'main_topic': cluster.get('main_topic', 'موضوع کلی'),
                    'keywords': cluster.get('keywords', []),
                    'article_title': cluster.get('article_title', ''),
                    'suggested_title': cluster.get('article_title', ''),  # Fallback
                    'meta_description': cluster.get('meta_description', ''),
                    'h2_headings': cluster.get('h2_headings', []),
                    'content_type': cluster.get('content_type', 'راهنما'),
                    'search_intent': cluster.get('search_intent', 'اطلاعاتی'),
                    'recommended_word_count': cluster.get('recommended_word_count', 1500),
                    'target_audience': cluster.get('target_audience', 'مخاطبان ایرانی'),
                    'content_focus': cluster.get('content_focus', 'تمرکز بر نیازهای کاربران فارسی‌زبان')
                }
                
                # Ensure at least one keyword exists
                if enhanced_cluster['keywords']:
                    enhanced_clusters.append(enhanced_cluster)
                else:
                    logger.warning(f"Skipping cluster with no keywords: {enhanced_cluster['main_topic']}")
            
            logger.info(f"Created {len(enhanced_clusters)} valid keyword clusters")
            return enhanced_clusters
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {str(e)}")
            logger.error(f"Response was: {response[:500]}")
            # Return empty list instead of raising to avoid complete failure
            return []
        except Exception as e:
            logger.error(f"Error clustering keywords: {str(e)}")
            # Return empty list instead of raising to avoid complete failure
            return []
    
    def generate_content_improvements(
        self, 
        url: str, 
        keywords: List[str], 
        position: float,
        impressions: int
    ) -> Dict[str, Any]:
        """
        Generate content improvement suggestions for existing URLs.
        
        Args:
            url: Existing URL to improve
            keywords: Target keywords for the URL
            position: Current average position
            impressions: Current impressions
            
        Returns:
            Dictionary with improvement suggestions
        """
        logger.info(f"Generating improvement suggestions for {url}")
        
        keywords_str = ", ".join(keywords[:10])  # Limit to top keywords
        
        system_prompt = """شما یک متخصص بهینه‌سازی محتوای SEO برای زبان فارسی هستید. وظیفه شما ارائه پیشنهادات مشخص و عملی برای بهبود عملکرد محتوا در نتایج جستجوی گوگل است. 

**نکات مهم:**
- تمام خروجی‌ها باید کاملاً به زبان فارسی باشند
- از کلمات انگلیسی استفاده نکنید
- به ویژگی‌های خاص الگوریتم گوگل برای محتوای فارسی توجه کنید
- رفتار کاربران ایرانی را در نظر بگیرید
- بهترین شیوه‌های SEO فارسی را اعمال کنید
- خروجی را فقط به صورت JSON معتبر برگردانید"""
        
        prompt = f"""**تحلیل و بهینه‌سازی محتوای موجود:**

**اطلاعات صفحه:**
- آدرس: {url}
- کلیدواژه‌های رتبه‌بندی شده: {keywords_str}
- میانگین موقعیت: {position:.1f}
- مجموع نمایش‌ها (Impressions): {impressions:,}

**وظیفه:**
این صفحه را تحلیل کن و پیشنهادات مشخص برای بهبود رتبه و افزایش CTR ارائه کن. در نظر بگیر که:
- محتوا به زبان فارسی است
- کاربران ایرانی مخاطب هستند
- الگوریتم گوگل برای فارسی ویژگی‌های خاصی دارد
- هدف بهبود از موقعیت {position:.1f} به صفحه اول (۱-۱۰) است

**فرمت خروجی JSON (فقط این خروجی را برگردان):**
{{
  "url": "{url}",
  "main_keyword": "کلیدواژه اصلی پیشنهادی",
  "current_position": {position:.1f},
  "improvement_priority": "بالا/متوسط/پایین",
  "analysis": {{
    "current_strength": "نقاط قوت فعلی محتوا",
    "main_weakness": "اصلی‌ترین ضعف محتوا"
  }},
  "primary_improvements": [
    "پیشنهاد بهبود ۱ - مشخص و عملی",
    "پیشنهاد بهبود ۲ - قابل اجرا",
    "پیشنهاد بهبود ۳ - با اولویت بالا"
  ],
  "content_enhancements": {{
    "add_sections": ["بخش پیشنهادی ۱", "بخش پیشنهادی ۲"],
    "recommended_h2_headings": ["هدینگ H2 پیشنهادی ۱", "هدینگ H2 پیشنهادی ۲"],
    "recommended_word_count": 2000,
    "add_elements": ["عناصر مورد نیاز: FAQ, جدول مقایسه، تصاویر"]
  }},
  "keyword_strategy": {{
    "primary_keywords": ["کلیدواژه اصلی ۱", "کلیدواژه اصلی ۲"],
    "lsi_keywords": ["LSI فارسی ۱", "LSI فارسی ۲", "LSI فارسی ۳"],
    "long_tail_keywords": ["عبارت طولانی ۱", "عبارت طولانی ۲"],
    "keyword_density_target": "1-2%"
  }},
  "technical_seo": {{
    "title_tag_suggestion": "عنوان پیشنهادی - حداکثر ۶۰ کاراکتر",
    "meta_description_suggestion": "توضیحات متا پیشنهادی - حداکثر ۱۶۰ کاراکتر",
    "url_optimization": "پیشنهاد بهینه‌سازی URL",
    "schema_markup": "نوع Schema پیشنهادی"
  }},
  "content_gaps": [
    "موضوع یا بخش از دست رفته ۱",
    "موضوع یا بخش از دست رفته ۲"
  ],
  "internal_linking": {{
    "suggested_anchor_texts": ["متن لینک داخلی ۱", "متن لینک داخلی ۲"],
    "target_pages": ["صفحات مرتبط برای لینک"]
  }},
  "user_experience": {{
    "improve_readability": "پیشنهاد بهبود خوانایی",
    "visual_elements": "عناصر بصری مورد نیاز",
    "cta_suggestion": "دکمه یا CTA پیشنهادی"
  }},
  "estimated_impact": {{
    "potential_position_improvement": "۵-۱۰ رتبه",
    "estimated_ctr_increase": "۲۰-۳۰٪",
    "implementation_difficulty": "آسان/متوسط/سخت",
    "persian_seo_focus": "تمرکز بر الگوریتم‌های گوگل برای محتوای فارسی"
  }}
}}

**نکات تحلیل:**
- تمرکز بر نیاز کاربران ایرانی و search intent فارسی
- بررسی رقبا در SERP فارسی
- توجه به Featured Snippet و People Also Ask
- پیشنهادات باید کاملاً عملی و قابل اجرا باشند
- طول محتوا را بر اساس استانداردهای محتوای فارسی تعیین کن"""
        
        try:
            response = self._call_api_with_retry(prompt, system_prompt)
            
            result = json.loads(response)
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {str(e)}")
            # Return fallback structure
            return {
                "primary_improvements": ["Optimize content for target keywords"],
                "content_gaps": ["Analysis unavailable"],
                "recommended_keywords": keywords[:5],
                "technical_suggestions": ["Review content structure"],
                "priority_level": "medium"
            }
        except Exception as e:
            logger.error(f"Error generating improvements: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test AI API connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            logger.info(f"Testing connection to {self.provider}...")
            
            # Include 'json' in prompt for providers that require it when using JSON mode
            test_prompt = "Respond with a simple json object containing only 'status': 'OK' if you can read this message."
            response = self._call_api_with_retry(test_prompt)
            
            if response and len(response) > 0:
                logger.info("Connection test successful!")
                return True
            else:
                logger.error("Connection test failed: Empty response")
                return False
                
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

