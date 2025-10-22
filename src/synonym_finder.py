"""
Synonym Finder - Find all semantic equivalents for keywords

This module uses AI to find all possible semantic equivalents for keywords including:
- Persian synonyms
- Finglish variations
- English keyboard typing
- Common misspellings
- Abbreviations
- Related terms
"""

import logging
import pandas as pd
from typing import Dict, List, Any
from pathlib import Path
import json
import re

logger = logging.getLogger(__name__)


class SynonymFinder:
    """Find semantic equivalents for keywords using AI."""
    
    SYNONYM_PROMPT_TEMPLATE = """
شما یک متخصص زبان‌شناسی و تحلیلگر معنایی هستید. وظیفه شما شناسایی تمام معادل‌های معنایی ممکن برای کلمه زیر است:

**کلمه اصلی:** {keyword}

برای این کلمه، تمام معادل‌های ممکن را در دسته‌بندی‌های زیر استخراج کنید:

## دسته‌بندی مترادف‌ها:

1. **مترادف‌های فارسی مستقیم**: کلمات فارسی با معنی دقیقاً مشابه یا نزدیک
   مثال برای "گوشی": تلفن، موبایل، تلفن همراه

2. **فینگلیش استاندارد**: نوشتار فارسی با حروف انگلیسی (تمام حالت‌های رایج)
   مثال برای "گوشی": gooshi, gushi, gooshi, gushy

3. **تایپ با کیبورد انگلیسی (QWERTY Layout)**: وقتی کاربر فارسی می‌نویسد ولی کیبوردش روی انگلیسی است
   مثال برای "گوشی": ',ad (گ=غ=', و=] یا و، ش=a، ی=d)
   
4. **اختصارات و اصطلاحات عامیانه**: فرم‌های کوتاه‌شده یا محاوره‌ای

5. **غلط‌های املایی رایج**: اشتباهات تایپی متداول
   مثال: گوشی -> گوشئ، گوش، گوشیی

6. **معادل انگلیسی**: ترجمه مستقیم به انگلیسی
   مثال برای "گوشی": mobile, phone, smartphone, cellphone

7. **مخفف‌ها**: حروف اختصاری رایج
   مثال: mobile -> mob, ph

8. **واژگان مرتبط**: کلماتی که در همان حوزه معنایی استفاده می‌شوند
   مثال برای "گوشی": تلفن هوشمند، اسمارت فون، موبایل فون

**خروجی:**
خروجی را به صورت JSON با ساختار زیر برگردان:

{{
  "persian_synonyms": ["مترادف1", "مترادف2", ...],
  "finglish_standard": ["gooshi", "gushi", ...],
  "english_keyboard_typing": ["',ad", "y,ad", ...],
  "colloquial_abbreviations": ["اختصار1", "اختصار2", ...],
  "common_misspellings": ["غلط1", "غلط2", ...],
  "english_equivalents": ["mobile", "phone", ...],
  "abbreviations": ["mob", "ph", ...],
  "related_terms": ["واژه مرتبط1", "واژه مرتبط2", ...]
}}

**نکات مهم:**
- حداقل 3-5 مورد برای هر دسته (اگر موجود باشد)
- تمام حالت‌های رایج را شامل شود
- دقت در کیبورد mapping فارسی-انگلیسی
- غلط‌های املایی واقعاً رایج را شامل شود

خروجی JSON را بنویس:
"""
    
    def __init__(self, config: Dict):
        """
        Initialize Synonym Finder.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        logger.info("✅ Synonym Finder initialized")
    
    def find_synonyms(
        self,
        keyword: str,
        ai_client: Any,
        model_name: str,
        provider: str
    ) -> Dict[str, List[str]]:
        """
        Find all semantic equivalents for a keyword using AI.
        
        Args:
            keyword: The keyword to find synonyms for
            ai_client: AI client instance
            model_name: AI model name
            provider: Provider type (openai, anthropic, etc.)
            
        Returns:
            Dictionary with categorized synonyms
        """
        # Build prompt
        prompt = self.SYNONYM_PROMPT_TEMPLATE.format(keyword=keyword)
        
        logger.info(f"  🔍 Finding synonyms for: {keyword}")
        
        try:
            # Generate synonyms based on provider
            if provider in ["openai", "openai_compatible", "grok"]:
                response = ai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a linguistic expert specializing in Persian language and SEO keyword variations."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=2000
                )
                result_text = response.choices[0].message.content.strip()
                
            elif provider == "anthropic":
                response = ai_client.messages.create(
                    model=model_name,
                    max_tokens=2000,
                    temperature=0.5,
                    messages=[{"role": "user", "content": prompt}]
                )
                result_text = response.content[0].text.strip()
            
            else:
                raise ValueError(f"Unsupported provider: {provider}")
            
            # Parse JSON response
            try:
                # Extract JSON from markdown code blocks if present
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', result_text, re.DOTALL)
                if json_match:
                    result_text = json_match.group(1)
                
                synonyms = json.loads(result_text)
                
                # Validate structure
                expected_keys = [
                    'persian_synonyms',
                    'finglish_standard',
                    'english_keyboard_typing',
                    'colloquial_abbreviations',
                    'common_misspellings',
                    'english_equivalents',
                    'abbreviations',
                    'related_terms'
                ]
                
                for key in expected_keys:
                    if key not in synonyms:
                        synonyms[key] = []
                
                logger.info(f"    ✅ Found {sum(len(v) for v in synonyms.values())} total variations")
                return synonyms
                
            except json.JSONDecodeError as e:
                logger.error(f"    ❌ Failed to parse JSON: {e}")
                # Return empty structure
                return {key: [] for key in expected_keys}
        
        except Exception as e:
            logger.error(f"    ❌ Failed to find synonyms: {e}")
            raise
    
    def process_excel_file(
        self,
        excel_path: str,
        ai_model,
        output_dir: str = "output/synonyms"
    ) -> str:
        """
        Process Excel file and find synonyms for all keywords.
        
        Args:
            excel_path: Path to input Excel file
            ai_model: AI model to use
            output_dir: Output directory
            
        Returns:
            Path to output Excel file
        """
        # Read Excel
        df = pd.read_excel(excel_path)
        
        logger.info(f"📊 Read {len(df)} keywords from {Path(excel_path).name}")
        
        # Get AI client
        ai_client = ai_model.get_client()
        
        # Process each row
        results = []
        
        print(f"\n{'='*70}")
        print(f"🔍 Finding Synonyms")
        print(f"{'='*70}\n")
        
        from tqdm import tqdm
        
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing keywords"):
            # Get keyword from first column
            keyword = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
            
            if not keyword.strip():
                logger.warning(f"  Row {idx}: Empty keyword, skipping")
                continue
            
            try:
                # Find synonyms
                synonyms = self.find_synonyms(
                    keyword=keyword,
                    ai_client=ai_client,
                    model_name=ai_model.config.get('model', ''),
                    provider=ai_model.provider
                )
                
                # Build result row
                result_row = {
                    'کلمه اصلی': keyword,
                    'مترادف‌های فارسی': ', '.join(synonyms.get('persian_synonyms', [])),
                    'فینگلیش': ', '.join(synonyms.get('finglish_standard', [])),
                    'کیبورد انگلیسی': ', '.join(synonyms.get('english_keyboard_typing', [])),
                    'اختصارات عامیانه': ', '.join(synonyms.get('colloquial_abbreviations', [])),
                    'غلط‌های املایی': ', '.join(synonyms.get('common_misspellings', [])),
                    'معادل انگلیسی': ', '.join(synonyms.get('english_equivalents', [])),
                    'مخفف‌ها': ', '.join(synonyms.get('abbreviations', [])),
                    'واژگان مرتبط': ', '.join(synonyms.get('related_terms', []))
                }
                
                results.append(result_row)
                
            except Exception as e:
                logger.error(f"  Row {idx} failed: {e}")
                # Add empty row
                results.append({
                    'کلمه اصلی': keyword,
                    'مترادف‌های فارسی': '',
                    'فینگلیش': '',
                    'کیبورد انگلیسی': '',
                    'اختصارات عامیانه': '',
                    'غلط‌های املایی': '',
                    'معادل انگلیسی': '',
                    'مخفف‌ها': '',
                    'واژگان مرتبط': ''
                })
        
        # Create DataFrame
        results_df = pd.DataFrame(results)
        
        # Save to Excel
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        output_file = output_path / f"synonyms_{Path(excel_path).stem}.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            results_df.to_excel(writer, index=False, sheet_name='Synonyms')
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Synonyms']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if cell.value and len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 60)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        logger.info(f"✅ Saved synonyms: {output_file.name}")
        
        return str(output_file)

