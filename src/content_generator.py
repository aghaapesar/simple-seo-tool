"""
Content Generator - AI-Powered Content Generation

This module generates SEO-optimized content based on Excel output files.
Features:
- Read topics and headings from Excel files
- Generate content for each heading with custom word counts
- Generate introduction and conclusion
- Support for multiple AI models
- Save content to Excel, Word, and HTML formats
"""

import logging
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json
import re

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generates SEO-optimized content for headings."""
    
    # Persian SEO content generation prompt for headings
    HEADING_PROMPT_TEMPLATE = """
**نقش شما:** 
تو یک استراتژیست و متخصص تولید محتوای SEO هستی که برای وب‌سایت‌های ایرانی در فروشگاه‌های اینترنتی فعالیت می‌کنی. تخصص اصلی تو، ایجاد اقتدار موضوعی (Topical Authority) و تبدیل خواننده به خریدار از طریق محتوای هدفمند است.
 
**ورودی‌های پروژه:** 
- **نام وب‌سایت:** {project_name}
- **موضوع اصلی مقاله:** {main_topic}
- **هدینگ فعلی:** {current_heading}
- **هدینگ‌های مرتبط در این مقاله:** {related_headings}

**دستورالعمل:**
محتوای تخصصی، کامل و کاربردی را **فقط برای هدینگ "{current_heading}"** بنویس.

**الزامات:**
- طول محتوا: حدود {word_count} کلمه
- لحن: حرفه‌ای، مثبت و جذاب
- بهینه‌سازی SEO: استفاده طبیعی از کلمات کلیدی
- ساختار: شامل زیرعناوین H3 در صورت نیاز، پاراگراف‌ها، لیست‌ها
- E-E-A-T: تخصص، تجربه، اعتبار و اعتمادپذیری
- تنوع در جملات: ترکیب جملات کوتاه و بلند
- طبیعی بودن: عبارات محاوره‌ای ملایم، مثال‌های عملی
- **مهم:** بدون نتیجه‌گیری یا جمع‌بندی برای این بخش - فقط محتوای اصلی

**خروجی:**
فقط متن محتوا را برای این هدینگ بنویس (بدون ذکر خود هدینگ و بدون نتیجه‌گیری). محتوا باید با تگ‌های HTML فرمت‌بندی شود:
- برای زیرعناوین از <h3> استفاده کن
- برای تاکید از <strong> استفاده کن  
- برای لیست‌ها از <ul> و <li> استفاده کن

همچنین، در متن نهایی، به صورت تصادفی (حدود ۲۰-۳۰% موارد) برخی نیم‌فاصله‌ها را حذف کن و با فاصله معمولی جایگزین کن.

محتوا را بنویس:
"""

    # Introduction prompt
    INTRO_PROMPT_TEMPLATE = """
**نقش شما:** 
متخصص تولید محتوای SEO برای وب‌سایت‌های ایرانی.

**ورودی‌ها:**
- **نام وب‌سایت:** {project_name}
- **موضوع مقاله:** {main_topic}
- **هدینگ‌های مقاله:** {all_headings}
- **خلاصه محتوای تولید شده:** {content_summary}

**دستورالعمل:**
یک مقدمه جذاب و حرفه‌ای برای این مقاله بنویس.

**الزامات:**
- طول: 150-200 کلمه
- جذب خواننده از همان ابتدا
- معرفی موضوع و اهمیت آن
- اشاره به آنچه در مقاله خواهد آمد
- بهینه‌سازی SEO با کلمات کلیدی اصلی

**خروجی:**
فقط متن مقدمه با فرمت HTML (بدون تگ <h2>، فقط <p> و <strong>).
"""

    # Conclusion prompt  
    CONCLUSION_PROMPT_TEMPLATE = """
**نقش شما:** 
متخصص تولید محتوای SEO برای وب‌سایت‌های ایرانی.

**ورودی‌ها:**
- **نام وب‌سایت:** {project_name}
- **موضوع مقاله:** {main_topic}
- **هدینگ‌های مقاله:** {all_headings}
- **خلاصه محتوای تولید شده:** {content_summary}

**دستورالعمل:**
یک نتیجه‌گیری قوی و کاربردی برای این مقاله بنویس.

**الزامات:**
- طول: 100-150 کلمه
- جمع‌بندی نکات کلیدی
- ارائه توصیه‌های نهایی
- دعوت به اقدام (CTA) در صورت مناسب بودن
- خاتمه قوی و به یادماندنی

**خروجی:**
فقط متن نتیجه‌گیری با فرمت HTML (بدون تگ <h2>، فقط <p> و <strong>).
"""
    
    def __init__(self, config: Dict):
        """
        Initialize Content Generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        logger.info("✅ Content Generator initialized")
    
    def read_excel_with_headers(self, excel_path: str) -> pd.DataFrame:
        """
        Read Excel file with proper header detection.
        
        Args:
            excel_path: Path to Excel file
            
        Returns:
            DataFrame with headers from first row
        """
        try:
            # Read with first row as header
            df = pd.read_excel(excel_path, header=0)
            logger.info(f"📊 Read {len(df)} rows from {Path(excel_path).name}")
            logger.info(f"📋 Columns: {list(df.columns)}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to read Excel file: {e}")
            raise
    
    def extract_topic_and_headings(self, row: pd.Series) -> Tuple[str, List[str]]:
        """
        Extract main topic and headings from a row.
        
        Args:
            row: DataFrame row
            
        Returns:
            Tuple of (main_topic, list of headings)
        """
        # First column is main topic
        main_topic = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
        
        # Find heading columns (columns that start with "هدینگ H2")
        headings = []
        for i in range(len(row)):
            column_name = str(row.index[i])
            value = row.iloc[i]
            
            # Check if this is a heading column
            if "هدینگ H2" in column_name and pd.notna(value) and str(value).strip():
                headings.append(str(value).strip())
        
        return main_topic, headings
    
    def generate_heading_content(
        self,
        project_name: str,
        main_topic: str,
        current_heading: str,
        related_headings: List[str],
        word_count: int,
        ai_client: Any,
        model_name: str,
        provider: str,
        content_instructions: str = ""
    ) -> str:
        """
        Generate content for a single heading.
        
        Args:
            project_name: Project/website name
            main_topic: Main topic of article
            current_heading: Current heading to generate content for
            related_headings: Other headings in article
            word_count: Target word count
            ai_client: AI client instance
            model_name: Model name
            provider: Provider type
            content_instructions: Additional instructions for content generation
            
        Returns:
            Generated HTML content
        """
        # Format related headings
        related_text = "\n".join([f"  - {h}" for h in related_headings if h != current_heading])
        
        # Build prompt
        prompt = self.HEADING_PROMPT_TEMPLATE.format(
            project_name=project_name,
            main_topic=main_topic,
            current_heading=current_heading,
            related_headings=related_text,
            word_count=word_count
        )
        
        # Add content instructions if provided
        if content_instructions:
            prompt += f"\n\n**دستورالعمل اضافی:**\n{content_instructions}\n\n"
        
        logger.info(f"  🤖 Generating content for: {current_heading[:50]}... ({word_count} words)")
        
        try:
            # Generate content based on provider
            if provider in ["openai", "openai_compatible", "grok"]:
                response = ai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are an expert Persian SEO content writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                content = response.choices[0].message.content.strip()
                
            elif provider == "anthropic":
                response = ai_client.messages.create(
                    model=model_name,
                    max_tokens=4000,
                    temperature=0.7,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text.strip()
            
            else:
                raise ValueError(f"Unsupported provider: {provider}")
            
            return content
            
        except Exception as e:
            logger.error(f"  ❌ Failed to generate content: {e}")
            raise
    
    def generate_introduction(
        self,
        project_name: str,
        main_topic: str,
        all_headings: List[str],
        content_summary: str,
        ai_client: Any,
        model_name: str,
        provider: str
    ) -> str:
        """Generate introduction for article."""
        headings_text = "\n".join([f"  - {h}" for h in all_headings])
        
        prompt = self.INTRO_PROMPT_TEMPLATE.format(
            project_name=project_name,
            main_topic=main_topic,
            all_headings=headings_text,
            content_summary=content_summary
        )
        
        logger.info(f"  📝 Generating introduction...")
        
        try:
            if provider in ["openai", "openai_compatible", "grok"]:
                response = ai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are an expert Persian SEO content writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content.strip()
                
            elif provider == "anthropic":
                response = ai_client.messages.create(
                    model=model_name,
                    max_tokens=1000,
                    temperature=0.7,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            logger.error(f"  ❌ Failed to generate introduction: {e}")
            raise
    
    def generate_conclusion(
        self,
        project_name: str,
        main_topic: str,
        all_headings: List[str],
        content_summary: str,
        ai_client: Any,
        model_name: str,
        provider: str
    ) -> str:
        """Generate conclusion for article."""
        headings_text = "\n".join([f"  - {h}" for h in all_headings])
        
        prompt = self.CONCLUSION_PROMPT_TEMPLATE.format(
            project_name=project_name,
            main_topic=main_topic,
            all_headings=headings_text,
            content_summary=content_summary
        )
        
        logger.info(f"  📝 Generating conclusion...")
        
        try:
            if provider in ["openai", "openai_compatible", "grok"]:
                response = ai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are an expert Persian SEO content writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
                return response.choices[0].message.content.strip()
                
            elif provider == "anthropic":
                response = ai_client.messages.create(
                    model=model_name,
                    max_tokens=800,
                    temperature=0.7,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            logger.error(f"  ❌ Failed to generate conclusion: {e}")
            raise
    
    def ensure_content_harmony(
        self,
        heading_contents: List[str],
        headings: List[str],
        main_topic: str,
        ai_client: Any,
        model_name: str,
        provider: str
    ) -> List[str]:
        """
        Check and ensure content harmony across all headings.
        
        Args:
            heading_contents: List of generated content for each heading
            headings: List of headings
            main_topic: Main topic
            ai_client: AI client instance
            model_name: Model name
            provider: Provider type
            
        Returns:
            List of harmonized content
        """
        # Build harmony check prompt
        content_preview = ""
        for i, (heading, content) in enumerate(zip(headings, heading_contents), 1):
            # Get first 150 chars of content for preview
            text_only = re.sub(r'<[^>]+>', '', content)
            preview = text_only[:150] + "..." if len(text_only) > 150 else text_only
            content_preview += f"{i}. **{heading}**: {preview}\n"
        
        harmony_prompt = f"""
**نقش شما:** 
متخصص ویرایش و بررسی هماهنگی محتوا.

**موضوع مقاله:** {main_topic}

**محتوای تولید شده:**
{content_preview}

**دستورالعمل:**
این محتوا را از نظر هماهنگی بررسی کن. آیا:
1. لحن نوشتاری در همه بخش‌ها یکسان است؟
2. سبک نگارش ثابت است؟
3. ارتباط منطقی بین بخش‌ها وجود دارد؟
4. تکرار غیرضروری اطلاعات نیست؟

**خروجی:**
فقط "OK" بنویس اگر محتوا هماهنگ است.
اگر مشکلی وجود دارد، شماره بخش و توضیح کوتاه بده (مثال: "بخش 2: لحن خیلی رسمی‌تر از بقیه است").
"""
        
        try:
            if provider in ["openai", "openai_compatible", "grok"]:
                response = ai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a content harmony expert."},
                        {"role": "user", "content": harmony_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                result = response.choices[0].message.content.strip()
            
            elif provider == "anthropic":
                response = ai_client.messages.create(
                    model=model_name,
                    max_tokens=500,
                    temperature=0.3,
                    messages=[
                        {"role": "user", "content": harmony_prompt}
                    ]
                )
                result = response.content[0].text.strip()
            
            elif provider == "gemini":
                response = ai_client.generate_content(
                    harmony_prompt,
                    generation_config={
                        'temperature': 0.3,
                        'max_output_tokens': 500
                    }
                )
                result = response.text.strip()
            
            else:
                logger.warning(f"Unknown provider: {provider}")
                return heading_contents
            
            # Log harmony check result
            if result.upper() == "OK":
                logger.info("✅ Content harmony confirmed")
            else:
                logger.warning(f"⚠️ Harmony note: {result}")
            
            return heading_contents
            
        except Exception as e:
            logger.error(f"Harmony check failed: {e}")
            return heading_contents
    
    def generate_article_interactive(
        self,
        row_index: int,
        main_topic: str,
        headings: List[str],
        project_name: str,
        ai_model,
        total_rows: int,
        content_instructions: str = ""
    ) -> Dict[str, Any]:
        """
        Generate complete article interactively for one row.
        
        Args:
            row_index: Current row index (0-based)
            main_topic: Main topic from first column
            headings: List of headings
            project_name: Project name
            ai_model: AI model to use
            total_rows: Total number of rows
            content_instructions: Additional instructions for content generation
            
        Returns:
            Dictionary with article data
        """
        print(f"\n{'='*70}")
        print(f"📝 Article {row_index + 1} of {total_rows}")
        print(f"{'='*70}")
        print(f"\n📌 Topic: {main_topic}")
        print(f"\n📋 Headings ({len(headings)}):")
        for i, h in enumerate(headings, 1):
            print(f"   {i}. {h}")
        
        # Confirm
        print(f"\n{'-'*70}")
        confirm = input(f"Generate content for this article? (Y/n): ").strip().lower()
        if confirm in ['n', 'no']:
            print("⏭️  Skipped")
            return None
        
        # Get total word count
        while True:
            try:
                total_words_input = input(f"\nEnter total word count for entire article (e.g., 1500): ").strip()
                total_words = int(total_words_input)
                if total_words < 100:
                    print("❌ Minimum 100 words required")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        print(f"✅ Total: {total_words} words")
        
        # Get word count for each heading
        heading_word_counts = []
        remaining_words = total_words
        
        print(f"\n{'='*70}")
        print(f"📊 Word Distribution (Total: {total_words} words)")
        print(f"{'='*70}")
        
        for i, heading in enumerate(headings):
            print(f"\n[{i+1}/{len(headings)}] {heading}")
            print(f"   Remaining: {remaining_words} words")
            
            while True:
                try:
                    suggestion = remaining_words // (len(headings) - i)
                    word_input = input(f"   Word count (suggested: {suggestion}): ").strip()
                    
                    if not word_input:
                        word_count = suggestion
                    else:
                        word_count = int(word_input)
                    
                    if word_count > remaining_words:
                        print(f"   ❌ Exceeds remaining words ({remaining_words})")
                        continue
                    
                    if word_count < 50:
                        print(f"   ❌ Minimum 50 words per heading")
                        continue
                    
                    heading_word_counts.append(word_count)
                    remaining_words -= word_count
                    print(f"   ✅ Allocated: {word_count} words")
                    break
                    
                except ValueError:
                    print("   ❌ Invalid number")
        
        # Generate content for each heading
        ai_client = ai_model.get_client()
        heading_contents = []
        
        print(f"\n{'='*70}")
        print(f"🚀 Generating Content")
        print(f"{'='*70}\n")
        
        for i, (heading, word_count) in enumerate(zip(headings, heading_word_counts)):
            content = self.generate_heading_content(
                project_name=project_name,
                main_topic=main_topic,
                current_heading=heading,
                related_headings=headings,
                word_count=word_count,
                ai_client=ai_client,
                model_name=ai_model.config.get('model', ''),
                provider=ai_model.provider,
                content_instructions=content_instructions
            )
            heading_contents.append(content)
            print(f"  ✅ [{i+1}/{len(headings)}] {heading[:40]}...")
        
        # Generate introduction
        content_summary = f"این مقاله شامل {len(headings)} بخش است: " + "، ".join(headings[:3])
        if len(headings) > 3:
            content_summary += f" و {len(headings) - 3} بخش دیگر"
        
        intro = self.generate_introduction(
            project_name=project_name,
            main_topic=main_topic,
            all_headings=headings,
            content_summary=content_summary,
            ai_client=ai_client,
            model_name=ai_model.config.get('model', ''),
            provider=ai_model.provider
        )
        print(f"  ✅ Introduction generated")
        
        # Generate conclusion
        conclusion = self.generate_conclusion(
            project_name=project_name,
            main_topic=main_topic,
            all_headings=headings,
            content_summary=content_summary,
            ai_client=ai_client,
            model_name=ai_model.config.get('model', ''),
            provider=ai_model.provider
        )
        print(f"  ✅ Conclusion generated")
        
        # Ensure content harmony
        print(f"\n  🔍 Checking content harmony...")
        heading_contents = self.ensure_content_harmony(
            heading_contents=heading_contents,
            headings=headings,
            main_topic=main_topic,
            ai_client=ai_client,
            model_name=ai_model.config.get('model', ''),
            provider=ai_model.provider
        )
        print(f"  ✅ Content harmony verified")
        
        # Combine all content
        full_content = f"{intro}\n\n"
        
        for heading, content in zip(headings, heading_contents):
            full_content += f"<h2>{heading}</h2>\n{content}\n\n"
        
        full_content += f"<h2>نتیجه‌گیری</h2>\n{conclusion}"
        
        # Generate SEO title and meta
        seo_title = main_topic[:60] if len(main_topic) <= 60 else main_topic[:57] + "..."
        meta_desc = f"{main_topic} - راهنمای کامل"[:160]
        
        result = {
            'main_topic': main_topic,
            'headings': headings,
            'seo_title': seo_title,
            'meta_description': meta_desc,
            'full_content': full_content,
            'word_count': sum(heading_word_counts) + 350  # approximate with intro/conclusion
        }
        
        print(f"\n✅ Article completed: ~{result['word_count']} words\n")
        
        return result
