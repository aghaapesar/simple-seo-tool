# SEO Content Analysis & Optimization Tool v2.2.3

A powerful, interactive Python application optimized for **Persian/Farsi content** that helps you improve your website's SEO through:
1. **Content Optimization**: Analyze Google Search Console data with Persian-aware AI
2. **SEO Data Collection**: Scrape and audit page titles, meta descriptions, and SEO tags
3. **Knowledge Base**: Track content history and avoid duplicates

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Persian Optimized](https://img.shields.io/badge/Persian-Optimized-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🆕 What's New in v2.2.3

### Persian Language Optimization 🇮🇷 (Enhanced)
- ✅ **Persian-Aware AI Prompts**: Specialized prompts for Farsi content analysis
- ✅ **LSI Keywords**: Persian-specific related keywords suggestions
- ✅ **Search Intent**: Understanding Iranian user behavior and intent
- ✅ **Content Structure**: H2/H3 headings optimized for Persian SEO
- ✅ **Persian URL Decoding**: Proper handling of Persian URLs in scraping mode
- ✅ **Fully Persian Excel Output**: All column headers and content in Persian

### Smart Clustering & Fallback Strategy 🔄
- ✅ **Intelligent Duplicate Detection**: Prevents repetitive content with adjustable thresholds
- ✅ **Fallback Clustering**: Multiple retry strategies when clustering fails
- ✅ **User-Guided Recovery**: Interactive options to adjust clustering parameters
- ✅ **Test Mode Support**: Clustering works in test mode with limited data
- ✅ **Threshold Adjustment**: Lower duplicate detection threshold on demand

### Knowledge Base System 🧠
- ✅ **Project Memory**: Track content history for each project
- ✅ **Duplicate Detection**: Automatically detect similar content to avoid repetition
- ✅ **Performance Tracking**: Compare predicted vs actual metrics
- ✅ **Smart Suggestions**: Learn from past performance to improve predictions

### Previous Features (v2.0)
- ✅ **Interactive Mode**: User-friendly prompts and selections
- ✅ **Dual Modes**: Content optimization + SEO data collection
- ✅ **Smart Sitemap Management**: Automatic caching, retry logic, selective downloads
- ✅ **Multi-File Support**: Process multiple Excel files in one run
- ✅ **Test Mode**: Quick validation with 10-item limits
- ✅ **Resume Capability**: Continue interrupted scraping sessions
- ✅ **Progress Tracking**: Real-time progress bars and status messages
- ✅ **Organized Structure**: Separate folders for input, output, and sitemaps

---

## 📋 Table of Contents

- [English Documentation](#english-documentation)
  - [Quick Start](#quick-start)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Modes](#modes)
  - [Troubleshooting](#troubleshooting)
- [مستندات فارسی](#مستندات-فارسی)
  - [شروع سریع](#شروع-سریع)
  - [ویژگی‌ها](#ویژگیها)
  - [نصب](#نصب)
  - [استفاده](#استفاده)
  - [حالت‌های اجرا](#حالتهای-اجرا)
  - [رفع مشکلات](#رفع-مشکلات)

---

# English Documentation

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API
Edit `config.yaml` with your AI provider credentials:
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  compatible_base_url: "https://ai.liara.ir/api/YOUR_PROJECT_ID/v1"
  compatible_api_key: "YOUR_API_KEY"
```

### 3. Prepare Your Data
- Copy Excel files from Google Search Console to `input/` folder
- Have your sitemap URL ready

### 4. Run the Tool
```bash
# Interactive mode (recommended for first time)
python3 main.py

# Content optimization mode directly
python3 main.py --mode content

# SEO data collection mode
python3 main.py --mode scraping

# Test mode (10 items only)
python3 main.py --mode content --test
```

---

## 🎯 Features

### Mode 1: Content Optimization (Persian-Optimized)
- **Search Console Analysis**: Load and analyze Google Search Console exports
- **Persian-Aware AI**: Specialized analysis for Farsi content and Iranian users
- **LSI Keywords**: Persian-specific related keywords (کلیدواژه‌های مرتبط فارسی)
- **Search Intent Analysis**: Understanding Iranian user search behavior
- **Comprehensive Suggestions**: 
  - Content improvements with Persian SEO best practices
  - H2/H3 headings optimized for Farsi queries
  - Meta descriptions (حداکثر ۱۶۰ کاراکتر)
  - FAQ suggestions based on Persian search patterns
  - Internal linking with Persian anchor texts
- **Knowledge Base Integration**: 
  - Track all generated content
  - Avoid duplicate topics automatically
  - Learn from performance over time

### Mode 2: SEO Data Collection
- **Page Scraping**: Extract titles, meta descriptions, H1s from all pages
- **Batch Processing**: Scrape pages in controlled batches with pause/resume
- **Progress Tracking**: Real-time progress bars and statistics
- **Error Handling**: Automatic retry logic and graceful error management
- **Resume Capability**: Pick up where you left off if interrupted

### Common Features
- **Interactive Sitemap Management**:
  - Automatic caching (no re-downloads)
  - 10-retry logic with exponential backoff
  - Sitemap index support with selective downloads
  - User prompts for manual retry
  
- **Smart File Handling**:
  - Multi-file selection from `input/` directory
  - File metadata display (size, date)
  - Automatic backup creation
  
- **Test Mode**: Validate with 10-item limits before full run
- **Comprehensive Logging**: Detailed logs saved to `seo_optimizer.log`
- **Multiple AI Providers**: OpenAI, Azure, Anthropic, or compatible APIs

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection for AI API calls

### Setup
```bash
# Create project directory
cd SEOContentAnalysis

# Install dependencies
pip install -r requirements.txt

# Create config from sample
cp config.sample.yaml config.yaml

# Edit config.yaml with your credentials
nano config.yaml
```

### Directory Structure
```
SEOContentAnalysis/
├── input/              # Place your Excel files here
├── sitemaps/           # Downloaded sitemaps (auto-cached)
├── output/             # Generated Excel reports
├── logs/               # Application logs
├── knowledge_base/     # Project memory & content history ✨ NEW
├── main.py             # Main application
├── config.yaml         # Your configuration
└── src/                # Source modules
    ├── knowledge_base.py  # Knowledge base system ✨ NEW
    └── ...
```

---

## 🎮 Usage

### Mode 1: Content Optimization

**Purpose**: Analyze Search Console data to improve existing content and find new opportunities.

**Workflow**:
1. Export data from Google Search Console (Performance → Export)
2. Copy Excel file(s) to `input/` folder
3. Run: `python3 main.py --mode content`
4. **Enter project name** (e.g., example.com) - used for knowledge base ✨
5. Select files when prompted
6. Enter sitemap URL when requested
7. Wait for Persian-optimized AI analysis to complete
8. Review results in `output/` folder

**What Happens Behind the Scenes**:
- AI analyzes with Persian language understanding
- Knowledge base checks for duplicate content
- Suggestions include Persian LSI keywords
- Content structure optimized for Iranian users
- All generated content tracked for future reference

**Output Files**:
- `improvements_[filename].xlsx` - Suggestions for existing pages
- `new_content_[filename].xlsx` - Ideas for new articles

**Example**:
```bash
$ python3 main.py --mode content

🚀 SEO CONTENT ANALYSIS & OPTIMIZATION TOOL
============================================
Version: 2.1 | Persian AI + Knowledge Base

📋 PROJECT IDENTIFICATION
Enter a name for this project: example.com
✅ Project name: example.com

📊 FOUND 2 EXCEL FILE(S)
  [1] example-blog.xlsx (94.5 KB | 2025-10-11)
  [2] example-product.xlsx (102.1 KB | 2025-10-11)

Your selection: 1,2

🗺️  SITEMAP CONFIGURATION
Enter your sitemap URL: https://example.com/sitemap.xml

[Processing with Persian-optimized AI...]

✅ Knowledge base: No duplicate content found
✅ Generated 15 improvement suggestions
✅ Created 8 new content ideas with Persian structure
```

---

### Mode 2: SEO Data Collection

**Purpose**: Scrape and audit all pages in your sitemap for SEO data.

**Workflow**:
1. Run: `python3 main.py --mode scraping`
2. Enter sitemap URL when prompted
3. Choose batch size (e.g., 50 pages at a time)
4. Review each batch, continue or pause
5. Results saved to `output/seo_data_[domain].xlsx`

**Collected Data**:
- Page URL
- Title tag
- Meta description
- H1 heading
- Canonical URL
- Open Graph tags (title, description)
- Twitter Card tags

**Example**:
```bash
$ python3 main.py --mode scraping --test

🔍 MODE: SEO Data Collection
🧪 TEST MODE: Will scrape only 10 pages

Enter sitemap URL: https://example.com/sitemap.xml

📥 Downloading sitemap...
✅ Extracted 1,250 URLs

How many pages per batch? 10

🔄 Scraping batch: 1 to 10 of 10
Scraping pages: 100%|███████████| 10/10

✅ SCRAPING COMPLETED!
📁 Output: output/seo_data_example.com.xlsx
```

---

### Test Mode

Test mode limits processing to 10 items for quick validation:

```bash
# Test content optimization
python3 main.py --mode content --test

# Test SEO scraping
python3 main.py --mode scraping --test
```

**When to use**:
- First time setup
- Testing new sitemaps
- Validating configuration
- Quick checks before full run

---

## ⚙️ Configuration

### AI Provider Setup

**OpenAI**:
```yaml
ai:
  provider: openai
  model: gpt-4o-mini
  openai_api_key: "sk-your-key"
  openai_base_url: "https://api.openai.com/v1"
```

**Liara.ir (OpenAI-Compatible)**:
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  compatible_base_url: "https://ai.liara.ir/api/PROJECT_ID/v1"
  compatible_api_key: "your-key"
```

**Azure OpenAI**:
```yaml
ai:
  provider: azure
  model: gpt-4o-mini
  azure_endpoint: "https://resource.openai.azure.com"
  azure_api_key: "your-key"
  azure_deployment: "gpt-4o-mini"
```

### App Settings

```yaml
app:
  min_position: 10              # Minimum position for opportunities
  clustering_threshold: 0.7     # Keyword clustering similarity
  max_headings_per_article: 8   # Max H2/H3 suggestions
  output_directory: "output"    # Output folder
```

---

## 🔧 Troubleshooting

### "No Excel files found"
**Solution**: Copy your Search Console Excel files to the `input/` folder:
```bash
cp ~/Downloads/search_console_data.xlsx input/
```

### "Sitemap download failed"
**Solution**: The tool will retry 10 times automatically. Check:
- Internet connection
- Sitemap URL is correct and accessible
- No firewall blocking requests

### "API key not configured"
**Solution**: Edit `config.yaml` and add your actual API key:
```yaml
compatible_api_key: "actual-key-not-placeholder"
```

### "Missing required columns"
**Solution**: Ensure Excel export includes: `Top queries`, `Clicks`, `Impressions`, `CTR`, `Position`

### Scraping interrupted
**Solution**: Just run again! The tool will resume from where it stopped:
```bash
python3 main.py --mode scraping
# Select same sitemap, it will skip already scraped pages
```

---

## 📊 Example Workflows

### Workflow 1: Monthly Content Audit
```bash
# 1. Export fresh Search Console data
# 2. Run analysis
python3 main.py --mode content

# 3. Implement top 10 suggestions
# 4. Track results next month
```

### Workflow 2: Complete SEO Audit
```bash
# 1. Scrape all pages
python3 main.py --mode scraping

# 2. Export data, identify issues
# 3. Fix missing/duplicate titles
# 4. Re-scrape to verify fixes
```

### Workflow 3: New Content Strategy
```bash
# 1. Analyze Search Console
python3 main.py --mode content

# 2. Review new_content_*.xlsx
# 3. Create articles based on AI outlines
# 4. Track rankings in 30 days
```

---

# مستندات فارسی

## 🚀 شروع سریع

### ۱. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### ۲. پیکربندی API
فایل `config.yaml` را ویرایش کنید:
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  compatible_base_url: "https://ai.liara.ir/api/شناسه_پروژه/v1"
  compatible_api_key: "کلید_API_شما"
```

### ۳. آماده‌سازی داده
- فایل‌های اکسل را در پوشه `input/` کپی کنید
- آدرس sitemap خود را آماده داشته باشید

### ۴. اجرای برنامه
```bash
# حالت تعاملی (پیشنهادی برای اولین بار)
python3 main.py

# مستقیم حالت بهینه‌سازی محتوا
python3 main.py --mode content

# حالت جمع‌آوری داده‌های SEO
python3 main.py --mode scraping

# حالت تست (۱۰ آیتم)
python3 main.py --mode content --test
```

### ۵. ویژگی‌های جدید v2.1 ✨

**تحلیل فارسی بهینه‌شده:**
- AI با درک عمیق از زبان فارسی
- کلیدواژه‌های LSI مخصوص فارسی
- ساختار محتوا بر اساس الگوهای جستجوی ایرانی
- توجه به Featured Snippet فارسی

**پایگاه دانش هوشمند:**
```bash
# در اولین اجرا، نام پروژه را وارد کنید
Project name: example.com

# سیستم خودکار:
# ✅ تمام محتوای تولید شده را ذخیره می‌کند
# ✅ از تولید محتوای تکراری جلوگیری می‌کند
# ✅ عملکرد پیش‌بینی‌ها را پیگیری می‌کند
# ✅ مدل را با زمان بهبود می‌دهد
```

**مشاهده پایگاه دانش:**
```bash
ls knowledge_base/example.com/
# metadata.json              # اطلاعات کلی
# content_history.json       # محتوای تولید شده
# performance_metrics.json   # عملکرد
# keyword_clusters.json      # کلاسترها
```

---

## 🎯 ویژگی‌ها

### حالت ۱: بهینه‌سازی محتوا (فارسی بهینه‌شده) 🇮🇷
- **تحلیل Search Console**: بارگذاری و تحلیل داده‌های گوگل
- **شناسایی فرصت‌ها**: یافتن کلیدواژه‌های پرپتانسیل
- **AI فارسی**: 
  - درک عمیق از زبان فارسی و نگارش‌های مختلف
  - تحلیل search intent کاربران ایرانی
  - کلیدواژه‌های LSI مخصوص فارسی
  - توجه به الگوهای جستجوی محلی
- **پیشنهادات جامع**:
  - عنوان و متا دیسکریپشن بهینه (۶۰ و ۱۶۰ کاراکتر)
  - ساختار H2/H3 مطابق با جستجوهای فارسی
  - سوالات متداول (FAQ) بومی‌سازی شده
  - Internal linking با anchor text فارسی
  - Schema markup پیشنهادی
- **پایگاه دانش هوشمند**:
  - ذخیره خودکار تمام محتوای تولید شده
  - جلوگیری از تولید محتوای تکراری
  - یادگیری از عملکرد گذشته

### حالت ۲: جمع‌آوری داده‌های SEO
- **Scraping صفحات**: استخراج تایتل، توضیحات، H1
- **پردازش دسته‌ای**: دانلود با کنترل و قابلیت توقف/ادامه
- **پیگیری پیشرفت**: نوار پیشرفت و آمار real-time
- **مدیریت خطا**: تلاش مجدد خودکار
- **قابلیت ادامه**: ادامه از جایی که متوقف شده

### ویژگی‌های مشترک
- **مدیریت هوشمند Sitemap**:
  - ذخیره خودکار (بدون دانلود مجدد)
  - ۱۰ بار تلاش با backoff
  - پشتیبانی از sitemap index
  - انتخاب دستی کاربر

- **مدیریت فایل**:
  - انتخاب چند فایل از `input/`
  - نمایش اطلاعات فایل
  - پشتیبان‌گیری خودکار

- **حالت تست**: محدود به ۱۰ آیتم برای اعتبارسنجی
- **گزارش‌دهی**: ذخیره logs در `seo_optimizer.log`
- **چند ارائه‌دهنده AI**: OpenAI، Azure، Anthropic، لیارا

---

## 📦 نصب

### پیش‌نیازها
- Python 3.8 یا بالاتر
- pip
- اتصال اینترنت برای API

### راه‌اندازی
```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# ایجاد فایل پیکربندی
cp config.sample.yaml config.yaml

# ویرایش و افزودن کلید API
nano config.yaml
```

### ساختار پوشه‌ها
```
SEOContentAnalysis/
├── input/              # فایل‌های اکسل را اینجا قرار دهید
├── sitemaps/           # sitemap های دانلود شده
├── output/             # گزارش‌های خروجی
├── main.py             # برنامه اصلی
├── config.yaml         # پیکربندی شما
└── src/                # ماژول‌های منبع
```

---

## 🎮 استفاده

### حالت ۱: بهینه‌سازی محتوا

**هدف**: تحلیل داده‌های Search Console برای بهبود محتوای موجود و یافتن فرصت‌های جدید.

**مراحل**:
1. Export از Google Search Console (Performance → Export)
2. کپی فایل اکسل به پوشه `input/`
3. اجرا: `python3 main.py --mode content`
4. انتخاب فایل‌ها
5. وارد کردن آدرس sitemap
6. منتظر تحلیل AI
7. بررسی نتایج در `output/`

**فایل‌های خروجی**:
- `improvements_[filename].xlsx` - پیشنهادات برای صفحات موجود
- `new_content_[filename].xlsx` - ایده برای مقالات جدید

---

### حالت ۲: جمع‌آوری داده‌های SEO

**هدف**: استخراج و بررسی داده‌های SEO تمام صفحات سایت.

**مراحل**:
1. اجرا: `python3 main.py --mode scraping`
2. وارد کردن آدرس sitemap
3. انتخاب اندازه دسته (مثلا ۵۰ صفحه)
4. بررسی هر دسته و ادامه یا توقف
5. نتایج در `output/seo_data_[domain].xlsx`

**داده‌های جمع‌آوری شده**:
- آدرس URL
- تگ Title
- Meta description
- سرفصل H1
- Canonical URL
- تگ‌های Open Graph
- تگ‌های Twitter Card

---

### حالت تست

برای اعتبارسنجی سریع با ۱۰ آیتم:

```bash
# تست بهینه‌سازی محتوا
python3 main.py --mode content --test

# تست scraping
python3 main.py --mode scraping --test
```

**چه زمانی استفاده کنیم**:
- راه‌اندازی اولیه
- تست sitemap جدید
- بررسی پیکربندی
- چک سریع قبل از اجرای کامل

---

## 🔧 رفع مشکلات

### "هیچ فایل اکسلی پیدا نشد"
**راه‌حل**: فایل‌ها را در پوشه `input/` قرار دهید:
```bash
cp ~/Downloads/search_console_data.xlsx input/
```

### "دانلود sitemap ناموفق بود"
**راه‌حل**: برنامه ۱۰ بار تلاش می‌کند. بررسی کنید:
- اتصال اینترنت
- صحت آدرس sitemap
- فایروال

### "کلید API پیکربندی نشده"
**راه‌حل**: `config.yaml` را ویرایش کنید:
```yaml
compatible_api_key: "کلید-واقعی-نه-placeholder"
```

### Scraping متوقف شد
**راه‌حل**: دوباره اجرا کنید! برنامه از جایی که متوقف شده ادامه می‌دهد.

---

## 📄 مجوز

MIT License

---

**ساخته شده با ❤️ برای بهبود SEO**

