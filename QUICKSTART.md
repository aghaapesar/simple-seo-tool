# Quick Start Guide - SEO Content Optimizer v2.1

Get started in 5 minutes with Persian-optimized AI! / شروع در ۵ دقیقه با AI بهینه‌شده برای فارسی!

---

## 🚀 English Quick Start

### Step 1: Install Dependencies
```bash
cd SEOContentAnalysis
pip3 install -r requirements.txt
```

**Note**: Use `pip3` on macOS/Linux, `pip` on Windows.

---

### Step 2: Configure API Key

Edit `config.yaml` and add your AI provider credentials:

**For Liara.ir users:**
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  compatible_base_url: "https://ai.liara.ir/api/YOUR_PROJECT_ID/v1"
  compatible_api_key: "YOUR_ACTUAL_API_KEY"
```

**For OpenAI users:**
```yaml
ai:
  provider: openai
  model: gpt-4o-mini
  openai_api_key: "sk-YOUR_ACTUAL_KEY"
  openai_base_url: "https://api.openai.com/v1"
```

---

### Step 3: Test Connection
```bash
python3 test_connection.py
```

You should see:
```
✅ Connection test PASSED!
✅ Clustering successful!
```

---

### Step 4: What's New in v2.1? ✨

**Persian Language Optimization 🇮🇷**
- AI understands Farsi content deeply
- Persian LSI keywords (کلیدواژه‌های LSI فارسی)
- Content structure for Iranian users
- Search intent analysis for Persian queries

**Knowledge Base System 🧠**
- Tracks all generated content automatically
- Prevents duplicate content creation
- Learns from past performance
- Project-specific memory

---

### Step 5: Choose Your Mode

The tool has **two modes**:

#### Mode A: Content Optimization (Improve Rankings)
**What it does**: Analyzes Google Search Console data to find content improvement opportunities.

**When to use**: Monthly content audits, finding quick wins, generating new article ideas.

**Input**: Excel files from Google Search Console  
**Output**: Improvement suggestions + New content ideas

```bash
python3 main.py --mode content
```

#### Mode B: SEO Data Collection (Site Audit)
**What it does**: Scrapes all pages in your sitemap to extract SEO data (titles, meta descriptions, etc.)

**When to use**: Complete site audits, finding duplicate/missing titles, SEO health checks.

**Input**: Sitemap URL  
**Output**: Excel with SEO data for all pages

```bash
python3 main.py --mode scraping
```

---

### Step 6: Run Your First Analysis

Let's try **Content Optimization Mode** with Persian AI:

#### 5a. Export Google Search Console Data
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Select your property
3. Performance → Search Results
4. Click **Export** → **Download Excel**

#### 5b. Move File to Input Folder
```bash
# Copy your Excel file to input/ folder
cp ~/Downloads/Queries*.xlsx input/
```

#### 5c. Run in Test Mode (10 queries only)
```bash
python3 main.py --mode content --test
```

**You'll be prompted to**:
1. **Enter project name** (e.g., `example.com`) - for knowledge base tracking ✨
2. Select Excel file(s) from `input/` folder
3. Enter your sitemap URL (e.g., `https://yoursite.com/sitemap.xml`)

The tool will:
- ✅ Create/load knowledge base for your project
- ✅ Download and cache your sitemap
- ✅ Analyze 10 queries with Persian-aware AI (test mode)
- ✅ Check for duplicate content automatically
- ✅ Generate Persian-optimized suggestions
- ✅ Create Excel reports in `output/` folder
- ✅ Save all generated content to knowledge base

#### 5d. Check Results
```bash
ls -lh output/
```

You should see:
- `improvements_*.xlsx` - Suggestions for existing pages
- `new_content_*.xlsx` - New article ideas

---

### Step 7: Run Full Analysis

Once test mode works, run the full analysis:

```bash
python3 main.py --mode content
```

This will:
- Process **all queries** in your Excel file(s)
- Use **Persian-optimized AI** for all suggestions
- Track everything in **knowledge base**
- Avoid duplicate content automatically

**Pro Tip**: Run this monthly to track improvements and build your knowledge base!

---

## 🔍 Try SEO Data Collection Mode

Want to audit all pages on your site?

### Test Mode (10 pages)
```bash
python3 main.py --mode scraping --test
```

### Full Scrape
```bash
python3 main.py --mode scraping
```

**You'll be prompted to**:
1. Enter sitemap URL
2. Choose batch size (e.g., 50 pages per batch)
3. After each batch, decide to continue or pause

**Output**: `output/seo_data_yourdomain.xlsx`

Contains:
- URL
- Title
- Meta Description
- H1
- Canonical URL
- Open Graph tags
- Twitter Card tags

---

## 📁 Folder Structure

```
SEOContentAnalysis/
├── input/              # 📥 Put your Excel files here
├── sitemaps/           # 🗺️  Downloaded sitemaps (auto-cached)
├── output/             # 📊 Generated reports appear here
├── logs/               # 📝 Application logs
├── knowledge_base/     # 🧠 Project memory (NEW v2.1) ✨
│   └── {project}/      # Separate folder per project
├── main.py             # ▶️  Run this
├── config.yaml         # ⚙️  Your API configuration
└── test_connection.py  # 🧪 Test AI connection
```

---

## 🎯 Common Commands

```bash
# Interactive mode (asks you to choose)
python3 main.py

# Content optimization (direct)
python3 main.py --mode content

# SEO scraping (direct)
python3 main.py --mode scraping

# Test mode (10 items only)
python3 main.py --mode content --test
python3 main.py --mode scraping --test

# Test AI connection
python3 test_connection.py

# Verbose logging
python3 main.py --mode content -v
```

---

## ⚠️ Troubleshooting

### "No Excel files found"
➡️ **Solution**: Move your Excel files to `input/` folder
```bash
cp ~/Downloads/yourfile.xlsx input/
```

### "Sitemap download failed"
➡️ **Solution**: Check your sitemap URL is correct
```bash
# Test manually
curl https://yoursite.com/sitemap.xml
```

The tool will retry 10 times automatically.

### "API connection failed"
➡️ **Solution**: Check `config.yaml` has real API keys (not placeholders)
```bash
python3 test_connection.py
```

### "Missing columns in Excel"
➡️ **Solution**: Export must include these columns:
- Top queries (or Query)
- Clicks
- Impressions
- CTR
- Position

---

## 🎉 You're Ready!

Now you can:
- ✅ Analyze Search Console data for improvements
- ✅ Generate AI-powered content suggestions
- ✅ Scrape your entire site for SEO audits
- ✅ Pause and resume long operations

**For more details**, see [README.md](README.md)

---

# 🚀 راهنمای سریع فارسی

## مرحله ۱: نصب وابستگی‌ها
```bash
cd SEOContentAnalysis
pip3 install -r requirements.txt
```

---

## مرحله ۲: پیکربندی کلید API

فایل `config.yaml` را ویرایش کنید:

**برای کاربران لیارا:**
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  compatible_base_url: "https://ai.liara.ir/api/شناسه_پروژه/v1"
  compatible_api_key: "کلید_واقعی_API"
```

---

## مرحله ۳: تست اتصال
```bash
python3 test_connection.py
```

باید ببینید:
```
✅ Connection test PASSED!
✅ Clustering successful!
```

---

## مرحله ۴: انتخاب حالت

ابزار دو حالت دارد:

### حالت الف: بهینه‌سازی محتوا (بهبود رتبه‌بندی)
**کاربرد**: تحلیل داده‌های Search Console برای یافتن فرصت‌های بهبود

**ورودی**: فایل‌های اکسل از Google Search Console  
**خروجی**: پیشنهادات بهبود + ایده‌های محتوای جدید

```bash
python3 main.py --mode content
```

### حالت ب: جمع‌آوری داده‌های SEO (بررسی سایت)
**کاربرد**: استخراج تایتل، توضیحات و تگ‌های SEO تمام صفحات

**ورودی**: آدرس Sitemap  
**خروجی**: اکسل با داده‌های SEO تمام صفحات

```bash
python3 main.py --mode scraping
```

---

## مرحله ۵: اولین تحلیل

بیایید **حالت بهینه‌سازی محتوا** را امتحان کنیم:

### ۵الف. Export از Google Search Console
1. به [Google Search Console](https://search.google.com/search-console) بروید
2. Performance → Search Results
3. Export → Download Excel

### ۵ب. انتقال فایل به پوشه Input
```bash
cp ~/Downloads/Queries*.xlsx input/
```

### ۵ج. اجرا در حالت تست (۱۰ کوئری)
```bash
python3 main.py --mode content --test
```

**از شما پرسیده می‌شود**:
1. انتخاب فایل اکسل از پوشه `input/`
2. آدرس sitemap سایت

ابزار:
- ✅ Sitemap را دانلود و ذخیره می‌کند
- ✅ ۱۰ کوئری را تحلیل می‌کند (حالت تست)
- ✅ پیشنهادات AI تولید می‌کند
- ✅ گزارش‌های اکسل در `output/` ایجاد می‌کند

### ۵د. بررسی نتایج
```bash
ls -lh output/
```

باید ببینید:
- `improvements_*.xlsx` - پیشنهادات برای صفحات موجود
- `new_content_*.xlsx` - ایده‌های مقاله جدید

---

## مرحله ۶: اجرای کامل

وقتی حالت تست کار کرد، تحلیل کامل را اجرا کنید:

```bash
python3 main.py --mode content
```

این همه کوئری‌ها را پردازش می‌کند.

---

## 🔍 امتحان حالت جمع‌آوری داده‌های SEO

می‌خواهید تمام صفحات سایت را بررسی کنید؟

### حالت تست (۱۰ صفحه)
```bash
python3 main.py --mode scraping --test
```

### Scrape کامل
```bash
python3 main.py --mode scraping
```

**خروجی**: `output/seo_data_domain.xlsx`

شامل:
- آدرس
- تایتل
- توضیحات متا
- H1
- Canonical URL
- تگ‌های Open Graph
- تگ‌های Twitter Card

---

## 📁 ساختار پوشه‌ها

```
SEOContentAnalysis/
├── input/              # 📥 فایل‌های اکسل را اینجا بگذارید
├── sitemaps/           # 🗺️  Sitemap های دانلود شده
├── output/             # 📊 گزارش‌های تولید شده
├── main.py             # ▶️  این را اجرا کنید
├── config.yaml         # ⚙️  پیکربندی API شما
└── test_connection.py  # 🧪 تست اتصال AI
```

---

## 🎯 دستورات رایج

```bash
# حالت تعاملی (سوال می‌کند)
python3 main.py

# بهینه‌سازی محتوا (مستقیم)
python3 main.py --mode content

# جمع‌آوری SEO (مستقیم)
python3 main.py --mode scraping

# حالت تست (۱۰ آیتم)
python3 main.py --mode content --test
python3 main.py --mode scraping --test

# تست اتصال AI
python3 test_connection.py

# گزارش‌دهی دقیق
python3 main.py --mode content -v
```

---

## ⚠️ رفع مشکلات

### "هیچ فایل اکسلی پیدا نشد"
➡️ **راه‌حل**: فایل‌ها را به `input/` منتقل کنید
```bash
cp ~/Downloads/yourfile.xlsx input/
```

### "دانلود sitemap ناموفق بود"
➡️ **راه‌حل**: آدرس sitemap را بررسی کنید
```bash
curl https://yoursite.com/sitemap.xml
```

ابزار به طور خودکار ۱۰ بار تلاش می‌کند.

### "اتصال API ناموفق بود"
➡️ **راه‌حل**: `config.yaml` را با کلید واقعی پر کنید
```bash
python3 test_connection.py
```

---

## 🎉 آماده‌اید!

حالا می‌توانید:
- ✅ داده‌های Search Console را تحلیل کنید
- ✅ پیشنهادات محتوای AI دریافت کنید
- ✅ کل سایت را برای SEO بررسی کنید
- ✅ عملیات طولانی را متوقف و ادامه دهید

**برای جزئیات بیشتر**: [README.md](README.md)
