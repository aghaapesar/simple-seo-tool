# SEO Content Analysis & Optimization Tool v2.3.2

A powerful, interactive Python application optimized for **Persian/Farsi content** that helps you improve your website's SEO through:
1. **Content Optimization**: Analyze Google Search Console data with Persian-aware AI
2. **SEO Data Collection**: Scrape and audit page titles, meta descriptions, and SEO tags
3. **AI Content Generation** ✨ NEW: Generate SEO-optimized content with multi-model AI support
4. **Internal Linking**: Smart internal linking with semantic analysis
5. **Knowledge Base**: Track content history and avoid duplicates

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Persian Optimized](https://img.shields.io/badge/Persian-Optimized-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🆕 What's New in v2.3.2

### 🔧 Advanced Internal Linking (Latest)
- ✅ **Smart Product Name Linking**: Priority for 2-3 syllable product names (بذر پیاز، کاشت گل)
- ✅ **Semantic Anchor Text**: Intelligent selection of anchor text based on product relevance
- ✅ **Even Link Distribution**: Links spread evenly across content, not just beginning/end
- ✅ **Enhanced Word Export**: Fixed Word document creation with better error handling
- ✅ **Persian Product Recognition**: 50+ Persian product words with syllable-based matching

### 🔧 Bug Fixes & Improvements (v2.3.1)
- ✅ **Enhanced Internal Linking**: Improved semantic matching with Persian word relationships
- ✅ **Fixed Word Export**: Resolved python-docx dependency issue
- ✅ **Better Link Relevance**: More accurate content-to-URL matching
- ✅ **Dynamic Version Management**: Automatic version reading from VERSION file

---

## 🆕 What's New in v2.3.0

### AI Content Generation ✨ NEW
- ✅ **Multi-Model AI Support**: Choose from OpenAI, Claude, Gemini, Grok, and more
- ✅ **Persian SEO Content**: Specialized prompts for natural, SEO-optimized Persian content
- ✅ **Smart Internal Linking**: Automatic internal links based on sitemap analysis
- ✅ **Multiple Export Formats**: Excel, Word (.docx), and editor-ready HTML
- ✅ **Model Selection**: Pick different AI models for different operations
- ✅ **Connection Testing**: Test all AI models before use

### Multi-Model AI Configuration
- ✅ **Configure Multiple Models**: Set up multiple AI providers in one config file
- ✅ **Default Model**: Set a default model for all operations
- ✅ **Per-Operation Selection**: Choose specific models for specific tasks
- ✅ **Supported Providers**: OpenAI, Claude (Anthropic), Gemini (Google), Grok, and OpenAI-compatible APIs

### Internal Linking System
- ✅ **Semantic Matching**: Links based on content relevance
- ✅ **Smart Rules**: 1 link per 300-400 words, no links in headings
- ✅ **Priority System**: Categories > Products > Blog posts
- ✅ **Anchor Text Optimization**: Natural anchor text with 5-syllable limit

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
  - [Mode 1: Content Optimization](#mode-1-content-optimization)
  - [Mode 2: SEO Data Collection](#mode-2-seo-data-collection)
  - [Mode 3: AI Content Generation](#mode-3-ai-content-generation-new)
  - [Multi-Model AI Configuration](#multi-model-ai-configuration)
  - [Troubleshooting](#troubleshooting)
- [مستندات فارسی](#مستندات-فارسی)
  - [شروع سریع](#شروع-سریع)
  - [ویژگی‌ها](#ویژگیها)
  - [نصب](#نصب)
  - [استفاده](#استفاده)
  - [حالت ۱: بهینه‌سازی محتوا](#حالت-۱-بهینهسازی-محتوا-فارسی-بهینهشده-)
  - [حالت ۲: جمع‌آوری داده‌های SEO](#حالت-۲-جمعآوری-دادههای-seo)
  - [حالت ۳: تولید محتوای هوشمند](#حالت-۳-تولید-محتوای-هوشمند-جدید)
  - [پیکربندی چند مدل AI](#پیکربندی-چند-مدل-ai)
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

# AI Content Generation mode ✨ NEW
python3 main.py --mode generation

# Test mode (10 items only)
python3 main.py --mode content --test
```

---

## 🎯 Features

### Mode 1: Content Optimization (Persian-Optimized)
Analyze existing content and find new opportunities
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

### Mode 3: AI Content Generation ✨ NEW

**Purpose**: Generate SEO-optimized Persian content with AI using multiple models and automatic internal linking.

**Workflow**:
1. Run: `python3 main.py --mode generation`
2. System tests all configured AI models
3. Choose to use default model or select per operation
4. **Select Excel file from `output/` folder** (files generated from Mode 1)
5. Enter project name
6. Select AI model for content generation
7. **For each article row**:
   - System shows topic from first column
   - Shows all headings from other columns
   - Ask for confirmation
   - Ask for total word count for entire article
   - Ask for word count per heading
   - Generate content for each heading
   - Generate introduction and conclusion
   - Combine into complete article
8. Optionally add internal links based on sitemap
9. Export to Word and HTML formats

**Note**: 
- Excel files are read from the `output/` folder (files generated by Mode 1)
- First row is treated as headers
- **Column 1**: Article topic (automatically used)
- **Columns 2-6**: Additional data (predictions, clusters, content type, search intent, word count)
- **Columns 7+**: H2 headings (only these are used for content generation)
- Each row represents one complete article

**Excel Structure Example**:
| عنوان پیشنهادی مقاله | پیش‌بینی نمایش | کلاستر کلیدواژه | نوع محتوا | هدف جستجو | تعداد کلمات | هدینگ H2 شماره 1 | هدینگ H2 شماره 2 | ... |
|---------------------|-------------|-------------|---------|---------|-----------|-----------------|-----------------|-----|
| راهنمای کاشت گلها | 1500 | کاشت | راهنما | اطلاعاتی | 2000 | معرفی گل لیلیوم | نحوه کاشت | ... |

**Key Features**:
- **Multi-Model AI Support**: Choose from OpenAI, Claude, Gemini, Grok, and more
- **Persian SEO Optimization**: Content follows Persian SEO best practices
- **Smart Internal Linking**: 
  - 1 link per 300-400 words
  - No links in headings
  - Priority: Categories > Products > Blog posts
  - Semantic anchor text matching (max 5 syllables)
- **Multiple Export Formats**:
  - Excel: With SEO title, meta description, and content
  - Word: Formatted documents with headings and bold text
  - HTML: Editor-ready (no `<html>`, `<head>`, `<body>` tags)

**Generated Content Includes**:
- SEO-optimized title (max 60 characters)
- Meta description (max 160 characters)
- Full HTML content with proper structure (H2, H3, paragraphs, lists)
- Natural Persian writing with E-E-A-T principles
- Random spacing variations for natural appearance

**Example**:
```bash
$ python3 main.py --mode generation

🚀 SEO CONTENT ANALYSIS & OPTIMIZATION TOOL
============================================
Version: 2.3.0 | Multi-Model AI + Content Generation + Internal Linking

[1/6] AI Model Configuration
======================================================================

🔌 Testing AI model connections...
----------------------------------------------------------------------
   Testing liara_gpt4o_mini (openai_compatible)... ✅ Connected
      (Default model)
   Testing claude_sonnet (anthropic)... ✅ Connected
   Testing gemini_pro (gemini)... ✅ Connected
----------------------------------------------------------------------

✅ 3/3 model(s) connected successfully

🤖 AI Model Selection
======================================================================

Default model: liara_gpt4o_mini (openai_compatible)

Would you like to use the default model for all operations?
  [Y] Yes, use default for everything
  [N] No, let me choose for each operation

Your choice (Y/n): Y
✅ Will use liara_gpt4o_mini for all operations

[2/6] Select Input Excel File
======================================================================

📊 FOUND 2 EXCEL FILE(S)
  [1] new_content_nazboo-blog.xlsx (45.2 KB | 2025-10-12)
  [2] improvements_nazboo-blog.xlsx (38.7 KB | 2025-10-12)

Your selection: 1
✅ Selected: new_content_nazboo-blog.xlsx

[3/6] Project Information
======================================================================

📋 PROJECT IDENTIFICATION
Enter a name for this project: nazboo.com
✅ Project name: nazboo.com

📝 Enter main topic/theme for content:
   Main topic: کشاورزی و باغبانی

[4/6] Select AI Model for Content Generation
======================================================================
✅ Using default model: liara_gpt4o_mini

[5/6] Generate Content
======================================================================

📝 Content Generation Settings
======================================================================

Enter approximate word count per heading: 800
✅ Target word count: 800 words per heading

📊 Found 3 heading column(s):
   - عنوان اصلی
   - H2_1
   - H2_2

Generate content for 15 row(s)? (y/n): y

======================================================================
🚀 Starting Content Generation
======================================================================

Generating content: 100%|████████████████| 15/15

======================================================================
✅ Content Generation Complete!
======================================================================
   Total rows: 15
   ✅ Success: 15
   ❌ Failed: 0
   📊 Total words generated: 12,340
   📁 Output: output/content_generated/content_nazboo-blog.xlsx
======================================================================

[6/6] Internal Linking & Export
======================================================================

🔗 Internal Linking
======================================================================

Add internal links to content? (Y/n): y

🗺️  SITEMAP CONFIGURATION
Enter your sitemap URL: https://nazboo.com/sitemap.xml

📥 Downloading sitemap...
✅ Extracted 450 URLs

📊 URL Statistics:
   - category: 25
   - product: 320
   - blog: 85
   - other: 20

🔄 Adding internal links...
Adding links: 100%|████████████████| 15/15

✅ Internal links added and saved to Excel

======================================================================
📄 Export to Word & HTML
======================================================================

Export content to Word and HTML files? (Y/n): y

Exporting files: 100%|████████████████| 15/15

======================================================================
✅ Export Complete!
======================================================================
   📝 Word files: 15
   🌐 HTML files: 15
   📁 Output directory: /path/to/output/documents
======================================================================

======================================================================
🎉 CONTENT GENERATION COMPLETED!
======================================================================
📊 Statistics:
   Total content pieces: 15
   Total words generated: 12,340
   Failed: 0

📁 Output files:
   Excel: output/content_generated/content_nazboo-blog.xlsx
   Documents: output/documents/
```

**Output Files Structure**:
```
output/
├── content_generated/
│   └── content_nazboo-blog.xlsx          # Excel with all content
└── documents/
    ├── content_nazboo.com_1_title.docx   # Word documents
    ├── content_nazboo.com_1_title.html   # HTML files
    ├── content_nazboo.com_2_title.docx
    ├── content_nazboo.com_2_title.html
    └── ...
```

**Excel Output Columns**:
- Original columns from input file
- `SEO_Title`: Optimized title (60 chars)
- `Meta_Description`: Meta description (160 chars)
- `Generated_Content`: Full HTML content with internal links

**Word Document Structure**:
```
SEO Information
---------------
Title: [SEO Title]
Meta Description: [Meta Description]

___________________________________________________________

Content
-------
[Full formatted content with headings, bold text, lists, etc.]
```

**HTML Output** (Editor-Ready):
```html
<!-- SEO Title -->
<!-- بهترین روش‌های کاشت گوجه فرنگی در باغ خانگی -->

<!-- Meta Description -->
<!-- راهنمای کامل کاشت و پرورش گوجه فرنگی با نکات کاربردی برای باغبانان خانگی. -->

<!-- Content Start -->
<h2>مقدمه</h2>
<p>گوجه فرنگی یکی از محبوب‌ترین سبزیجاتی است که...</p>

<h2>انتخاب بذر مناسب</h2>
<p>برای کاشت گوجه فرنگی، انتخاب <strong>بذر با کیفیت</strong> اهمیت زیادی دارد...</p>
<p>می‌توانید از <a href="https://nazboo.com/product-category/seeds/">بذرهای باکیفیت</a> استفاده کنید.</p>

<h3>انواع بذر گوجه فرنگی</h3>
<ul>
  <li>گوجه فرنگی رقم قدیما</li>
  <li><a href="https://nazboo.com/product/tomato-seed-superb/">بذر گوجه فرنگی سوپرب</a></li>
  <li>گوجه فرنگی گیلاسی</li>
</ul>
...
<!-- Content End -->
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

### Multi-Model AI Configuration ✨ NEW

Starting from v2.3.0, you can configure multiple AI models and choose which one to use for each operation.

**Configuration in `config.yaml`**:

```yaml
# Multi-Model AI Configuration
ai_models:
  # Set default model
  default: "liara_gpt4o_mini"
  
  # Configure multiple models
  liara_gpt4o_mini:
    provider: "openai_compatible"
    api_key: "your-liara-api-key"
    base_url: "https://ai.liara.ir/api/YOUR_PROJECT/v1"
    model: "openai/gpt-4o-mini"
    
  openai_gpt4:
    provider: "openai"
    api_key: "env:OPENAI_API_KEY"  # Read from environment variable
    base_url: "https://api.openai.com/v1"
    model: "gpt-4"
  
  claude_sonnet:
    provider: "anthropic"
    api_key: "env:ANTHROPIC_API_KEY"
    model: "claude-3-5-sonnet-20241022"
  
  gemini_pro:
    provider: "gemini"
    api_key: "env:GOOGLE_API_KEY"
    model: "gemini-pro"
  
  grok_llama3_70b:
    provider: "grok"
    api_key: "env:GROK_API_KEY"
    model: "llama3-70b-8192"
```

**Supported Providers**:

| Provider | Type | Models | Configuration |
|----------|------|--------|---------------|
| **OpenAI** | `openai` | GPT-4, GPT-4o, GPT-3.5 | `api_key`, `base_url`, `model` |
| **Claude** | `anthropic` | Claude 3 (Opus, Sonnet, Haiku) | `api_key`, `model` |
| **Gemini** | `gemini` | Gemini Pro, Gemini Pro Vision | `api_key`, `model` |
| **Grok** | `grok` | Llama 3, Mixtral | `api_key`, `model` |
| **Liara.ir** | `openai_compatible` | Any OpenAI-compatible | `api_key`, `base_url`, `model` |
| **Custom** | `openai_compatible` | Any OpenAI-compatible API | `api_key`, `base_url`, `model` |

**Environment Variables**:
You can use `env:VARIABLE_NAME` to read API keys from environment variables:

```bash
# Set environment variables
export OPENAI_API_KEY="sk-your-openai-key"
export ANTHROPIC_API_KEY="sk-ant-your-claude-key"
export GOOGLE_API_KEY="your-google-api-key"
export GROK_API_KEY="gsk_your-grok-key"

# Run the tool
python3 main.py --mode generation
```

**Model Selection Flow**:
1. At startup, system tests all configured models
2. User chooses: "Use default for all" or "Select per operation"
3. If "Select per operation", system prompts for model selection when needed
4. Only connected models are shown in selection

**Example Model Selection**:
```bash
🤖 Select AI Model for: Content Generation
======================================================================

  [1] liara_gpt4o_mini (openai_compatible) [DEFAULT]
  [2] claude_sonnet (anthropic)
  [3] gemini_pro (gemini)

  [0] Use default model (liara_gpt4o_mini)

----------------------------------------------------------------------

Your selection: 2
✅ Selected: claude_sonnet
```

---

### Legacy AI Provider Setup (v2.2.3 and earlier)

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

### Workflow 4: AI Content Generation with Internal Linking ✨ NEW
```bash
# 1. Analyze Search Console and get content ideas
python3 main.py --mode content

# 2. Generate full content with AI
python3 main.py --mode generation
#    - Select the new_content_*.xlsx file
#    - Choose AI model (Claude, GPT-4, Gemini, etc.)
#    - Set word count per article (e.g., 800 words)
#    - Enable internal linking with sitemap

# 3. Review generated content in:
#    - Excel: output/content_generated/
#    - Word docs: output/documents/
#    - HTML files: output/documents/

# 4. Publish content and track results
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

# حالت تولید محتوای هوشمند ✨ جدید
python3 main.py --mode generation

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

### حالت ۳: تولید محتوای هوشمند ✨ جدید

**هدف**: تولید محتوای SEO بهینه‌شده فارسی با هوش مصنوعی، پشتیبانی از چند مدل و لینک‌دهی داخلی خودکار.

**ویژگی‌های کلیدی**:
- **پشتیبانی چند مدل AI**: انتخاب از بین OpenAI، Claude، Gemini، Grok و غیره
- **بهینه‌سازی SEO فارسی**: محتوا با رعایت اصول SEO فارسی
- **لینک‌دهی داخلی هوشمند**:
  - ۱ لینک به ازای هر ۳۰۰-۴۰۰ کلمه
  - عدم لینک در هدینگ‌ها
  - اولویت: دسته‌بندی‌ها > محصولات > مقالات
  - انکر تکست سمنتیک (حداکثر ۵ هجا)
- **خروجی چندگانه**:
  - اکسل: با عنوان SEO، متا دیسکریپشن و محتوا
  - Word: اسناد فرمت‌بندی شده
  - HTML: آماده برای ادیتور (بدون تگ‌های پایه)

**محتوای تولید شده شامل**:
- عنوان بهینه‌شده SEO (حداکثر ۶۰ کاراکتر)
- متا دیسکریپشن (حداکثر ۱۶۰ کاراکتر)
- محتوای کامل HTML با ساختار مناسب (H2, H3, پاراگراف، لیست)
- نگارش طبیعی فارسی با اصول E-E-A-T
- تنوع در فاصله‌گذاری برای طبیعی‌تر بودن

**مراحل اجرا**:
1. اجرا: `python3 main.py --mode generation`
2. سیستم تمام مدل‌های AI پیکربندی شده را تست می‌کند
3. انتخاب استفاده از مدل پیش‌فرض یا انتخاب دستی
4. **انتخاب فایل اکسل از پوشه `output/`** (فایل‌های تولید شده از حالت ۱)
5. وارد کردن نام پروژه
6. انتخاب مدل AI برای تولید محتوا
7. **برای هر ردیف مقاله**:
   - سیستم موضوع را از ستون اول نمایش می‌دهد
   - تمام هدینگ‌ها از ستون‌های دیگر نمایش داده می‌شود
   - درخواست تایید
   - پرسش تعداد کلمات کل مقاله
   - پرسش تعداد کلمات برای هر هدینگ
   - تولید محتوا برای هر هدینگ
   - تولید مقدمه و نتیجه‌گیری
   - ترکیب در یک مقاله کامل
8. اضافه کردن لینک‌های داخلی بر اساس sitemap (اختیاری)
9. خروجی به فرمت‌های Word و HTML

**توجه**: 
- فایل‌های اکسل از پوشه `output/` خوانده می‌شوند (خروجی حالت ۱)
- ردیف اول به عنوان سرستون در نظر گرفته می‌شود
- **ستون ۱**: موضوع مقاله (خودکار استفاده می‌شود)
- **ستون‌های ۲-۶**: داده‌های اضافی (پیش‌بینی، کلاستر، نوع محتوا، هدف جستجو، تعداد کلمات)
- **ستون‌های ۷+**: هدینگ‌های H2 (فقط این‌ها برای تولید محتوا استفاده می‌شوند)
- هر ردیف یک مقاله کامل است

**مثال ساختار اکسل**:
| عنوان پیشنهادی مقاله | پیش‌بینی نمایش | کلاستر کلیدواژه | نوع محتوا | هدف جستجو | تعداد کلمات | هدینگ H2 شماره 1 | هدینگ H2 شماره 2 | ... |
|---------------------|-------------|-------------|---------|---------|-----------|-----------------|-----------------|-----|
| راهنمای کاشت گلها | 1500 | کاشت | راهنما | اطلاعاتی | 2000 | معرفی گل لیلیوم | نحوه کاشت | ... |

**مثال خروجی اکسل**:

| عنوان اصلی | H2_1 | H2_2 | SEO_Title | Meta_Description | Generated_Content |
|-----------|------|------|-----------|-----------------|-------------------|
| راهنمای کاشت گوجه فرنگی | انتخاب بذر | آماده‌سازی خاک | بهترین روش‌های کاشت گوجه فرنگی... | راهنمای کامل کاشت و پرورش... | `<h2>مقدمه</h2><p>...</p>...` |

**ساختار اسناد Word**:
```
اطلاعات SEO
-----------
عنوان: بهترین روش‌های کاشت گوجه فرنگی در باغ خانگی
متا دیسکریپشن: راهنمای کامل کاشت و پرورش گوجه فرنگی با نکات کاربردی...

___________________________________________________________

محتوا
-----
[محتوای کامل با فرمت‌بندی، هدینگ‌ها، متن‌های بولد و غیره]
```

**خروجی HTML** (آماده برای ادیتور):
```html
<!-- SEO Title -->
<!-- بهترین روش‌های کاشت گوجه فرنگی در باغ خانگی -->

<!-- Meta Description -->
<!-- راهنمای کامل کاشت و پرورش گوجه فرنگی با نکات کاربردی -->

<!-- Content Start -->
<h2>مقدمه</h2>
<p>گوجه فرنگی یکی از محبوب‌ترین سبزیجات...</p>

<h2>انتخاب بذر مناسب</h2>
<p>برای کاشت موفق، <strong>انتخاب بذر باکیفیت</strong> ضروری است...</p>
<p>می‌توانید از <a href="https://example.com/category/seeds/">بذرهای باکیفیت</a> استفاده کنید.</p>
...
<!-- Content End -->
```

---

### پیکربندی چند مدل AI

از نسخه v2.3.0، می‌توانید چندین مدل AI را پیکربندی کرده و برای هر عملیات یکی را انتخاب کنید.

**پیکربندی در `config.yaml`**:

```yaml
ai_models:
  # مدل پیش‌فرض
  default: "liara_gpt4o_mini"
  
  # پیکربندی چند مدل
  liara_gpt4o_mini:
    provider: "openai_compatible"
    api_key: "کلید-API-لیارا"
    base_url: "https://ai.liara.ir/api/پروژه/v1"
    model: "openai/gpt-4o-mini"
    
  claude_sonnet:
    provider: "anthropic"
    api_key: "env:ANTHROPIC_API_KEY"
    model: "claude-3-5-sonnet-20241022"
  
  gemini_pro:
    provider: "gemini"
    api_key: "env:GOOGLE_API_KEY"
    model: "gemini-pro"
```

**تنظیم متغیرهای محیطی**:
```bash
export OPENAI_API_KEY="کلید-OpenAI"
export ANTHROPIC_API_KEY="کلید-Claude"
export GOOGLE_API_KEY="کلید-Google"
export GROK_API_KEY="کلید-Grok"
```

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

