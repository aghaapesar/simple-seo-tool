# Feature Documentation - SEO Content Optimizer v2.0

Comprehensive guide to all features and capabilities.

---

## 📋 Table of Contents

1. [Operational Modes](#operational-modes)
2. [Interactive Features](#interactive-features)
3. [Sitemap Management](#sitemap-management)
4. [File Management](#file-management)
5. [Test Mode](#test-mode)
6. [AI Integration](#ai-integration)
7. [Resume Capability](#resume-capability)
8. [Progress Tracking](#progress-tracking)

---

## 🎮 Operational Modes

### Mode 1: Content Optimization

**Purpose**: Analyze Search Console data to improve existing content and discover new opportunities.

**Input**: Excel files from Google Search Console  
**Output**: Two Excel files per input file
- `improvements_[filename].xlsx` - Suggestions for existing pages
- `new_content_[filename].xlsx` - New article ideas with outlines

**Process**:
1. Load Search Console queries
2. Identify high-potential opportunities (position > 10, high impressions)
3. Match queries to existing URLs from sitemap
4. Generate AI-powered improvement suggestions for matched pages
5. Cluster unmatched queries into new content topics
6. Create structured article outlines with H2/H3 headings

**Command**:
```bash
python3 main.py --mode content
```

**Use Cases**:
- Monthly content audits
- Finding quick wins (positions 11-20)
- Discovering content gaps
- Generating data-driven content strategies

---

### Mode 2: SEO Data Collection

**Purpose**: Scrape and audit all pages in your sitemap for SEO data.

**Input**: Sitemap URL  
**Output**: One Excel file per sitemap
- `seo_data_[domain].xlsx` - Complete SEO audit data

**Collected Data**:
- Page URL
- `<title>` tag
- `<meta name="description">` tag
- First `<h1>` tag
- `<link rel="canonical">` URL
- Open Graph tags (`og:title`, `og:description`)
- Twitter Card tags (`twitter:title`, `twitter:description`)

**Process**:
1. Download sitemap(s)
2. Extract all URLs
3. Scrape each page for SEO elements
4. Save results with status tracking
5. Support resume for interrupted sessions

**Command**:
```bash
python3 main.py --mode scraping
```

**Use Cases**:
- Complete site SEO audits
- Finding missing/duplicate titles
- Identifying thin or missing meta descriptions
- Checking canonical tag consistency
- Social media tag verification

---

## 🖱️ Interactive Features

### File Selection

**Feature**: Interactive selection of Excel files from `input/` folder.

**How it Works**:
```
📊 FOUND 2 EXCEL FILE(S)
  [1] example-blog.xlsx (94.5 KB | 2025-10-11 14:32)
  [2] example-product.xlsx (102.1 KB | 2025-10-11 14:30)

Selection options:
  - Enter numbers separated by commas (e.g., 1,3)
  - Enter 'all' to select all files
  - Enter 'finish' or 'exit' to quit

Your selection: 1,2
```

**Features**:
- Display file size and modification date
- Multi-select support (comma-separated)
- Select all option
- Clear exit command

---

### Mode Selection

**Feature**: Interactive prompt to choose operational mode if not specified via CLI.

**How it Works**:
```
Please select operational mode:

  [1] Content Optimization
      Analyze Search Console data for content improvements
      Input: Excel files from Google Search Console
      Output: Improvement suggestions + New content ideas

  [2] SEO Data Collection
      Scrape page titles and meta tags from sitemap
      Input: Sitemap URL
      Output: Excel with SEO data for all pages

Your selection (1 or 2): 
```

**Trigger**: Launched automatically when running `python3 main.py` without `--mode` flag.

---

## 🗺️ Sitemap Management

### Interactive URL Input

**Feature**: Prompt user for sitemap URL with validation.

**How it Works**:
```
🗺️  SITEMAP CONFIGURATION
Enter your sitemap URL (e.g., https://example.com/sitemap.xml): 
```

**Validation**:
- ❌ Rejects empty input
- ❌ Requires http:// or https:// prefix
- ✅ Accepts valid URLs

---

### Automatic Caching

**Feature**: Downloaded sitemaps are cached locally to avoid re-downloads.

**Cache Location**: `sitemaps/` folder

**Filename Format**: `{domain}_{hash}.xml`

**How it Works**:
```
✅ Using cached sitemap: example.com_a3f2d1b9c8e7.xml
   Download again? (y/N): 
```

**Benefits**:
- Faster re-runs
- Reduces server load
- Saves bandwidth
- User can force re-download if needed

---

### Retry Logic (10 Attempts)

**Feature**: Automatic retry with exponential backoff for failed downloads.

**How it Works**:
```
📥 Downloading sitemap: https://example.com/sitemap.xml
   Attempt 1/10... ✅ Success!
```

If fails:
```
   Attempt 1/10... ❌ Failed: Connection timeout
   Waiting 2s before retry...
   Attempt 2/10... ❌ Failed: Connection timeout
   Waiting 4s before retry...
   ...
   Attempt 10/10... ❌ Failed: Connection timeout

❌ All 10 download attempts failed!

Do you want to try again? (y/N): 
```

**Backoff Strategy**: 2^attempt seconds, capped at 30s

**User Control**: After all attempts fail, user can manually retry or abort.

---

### Sitemap Index Support

**Feature**: Detect sitemap indices and let user select which sub-sitemaps to download.

**How it Works**:
```
🔗 This is a sitemap index containing 5 sub-sitemaps

📋 FOUND 5 SUB-SITEMAPS
  [1] posts - https://example.com/sitemap-posts.xml
  [2] pages - https://example.com/sitemap-pages.xml
  [3] products - https://example.com/sitemap-products.xml
  [4] categories - https://example.com/sitemap-categories.xml
  [5] tags - https://example.com/sitemap-tags.xml

Selection options:
  - Enter numbers separated by commas (e.g., 1,3,5)
  - Enter 'all' to download all sitemaps
  - Enter 'none' to skip

Your selection: 1,3
```

**Features**:
- Automatic detection of `<sitemapindex>` elements
- Extract readable names from URLs
- Selective download
- Combined URL extraction from selected sitemaps

---

## 📁 File Management

### Organized Folder Structure

```
SEOContentAnalysis/
├── input/                    # User places Excel files here
│   └── processed/           # Auto-moved after processing (optional)
├── sitemaps/                 # Cached sitemap downloads
│   ├── example.com_hash1.xml
│   └── blog.com_hash2.xml
├── output/                   # Generated Excel reports
│   ├── improvements_file1.xlsx
│   ├── new_content_file1.xlsx
│   └── seo_data_domain.xlsx
├── main.py
├── config.yaml
└── seo_optimizer.log        # Detailed logs
```

**Benefits**:
- Clean separation of inputs/outputs
- Easy to find results
- Prevents accidental overwriting
- Automatic cleanup options

---

### Backup Creation

**Feature**: Automatic backup of input Excel files before processing.

**How it Works**:
```
📋 Creating backup: example-blog_backup.xlsx
✅ Backup created
```

**Location**: Same folder as original file

**Purpose**: Safety net in case of processing errors or data corruption.

---

## 🧪 Test Mode

### Purpose

Quick validation with limited data before running full analysis.

### Limits

- **Content Optimization**: 10 queries
- **SEO Data Collection**: 10 pages

### Activation

```bash
# Via CLI flag
python3 main.py --mode content --test
python3 main.py --mode scraping --test

# Indicated in output
🧪 TEST MODE ENABLED: Will process only 10 items
```

### Use Cases

1. **First-Time Setup**: Verify everything works before processing thousands of items
2. **New Sitemap**: Test a new site's sitemap structure
3. **API Testing**: Ensure AI provider is responding correctly
4. **Quick Preview**: See output format before full run
5. **Debugging**: Isolate issues with smaller dataset

### Output

Same format as full mode, just limited data.

---

## 🤖 AI Integration

### Multi-Provider Support

**Supported Providers**:
1. OpenAI (GPT-4, GPT-4o-mini, etc.)
2. Azure OpenAI
3. Anthropic (Claude)
4. OpenAI-Compatible APIs (Liara.ir, LM Studio, Ollama, etc.)

### JSON Mode

**Feature**: Forces AI to return structured JSON for reliable parsing.

**Implementation**: Automatically includes "json" in prompts when using OpenAI-compatible APIs.

**Example Response**:
```json
{
  "primary_improvements": [
    "Add FAQ section with common questions",
    "Expand introduction with more context",
    "Include comparison table"
  ],
  "recommended_keywords": [
    "keyword 1",
    "keyword 2"
  ],
  "priority_level": "high"
}
```

### Rate Limiting

**Feature**: Configurable queries-per-second (QPS) to respect API limits.

**Config**:
```yaml
ai:
  qps: 1.0  # 1 request per second
```

**Implementation**: Automatic delay between requests based on QPS setting.

### Retry Logic

**Feature**: Automatic retry for failed API calls.

**Config**:
```yaml
ai:
  max_retries: 3
  retry_base_delay: 1.5  # seconds
```

**Strategy**: Exponential backoff (1.5s → 3s → 6s)

---

## 🔄 Resume Capability

### SEO Data Collection Mode

**Feature**: Continue scraping from where you left off if interrupted.

**How it Works**:

First run:
```
🔄 Scraping batch: 1 to 50 of 1,250
Scraping pages: 100%|███████████| 50/50
✅ Batch complete. Scraped: 50/1,250

⏸️  Scraped 50/1,250 pages. Continue? (Y/n): n

⏹️  Scraping paused. 1,200 URLs remaining.
   Run again to resume from where you left off.
```

Second run (same sitemap):
```
📊 Found existing data: 50 URLs already scraped
📋 URLs to scrape: 1,200 (Total: 1,250)

🔄 Scraping batch: 51 to 100 of 1,200
```

**Implementation**:
- Excel file stores all scraped URLs
- On restart, loads existing file
- Skips URLs already present
- Continues from next unscraped URL

**Benefits**:
- No lost work if interrupted (Ctrl+C, network failure, etc.)
- Can pause and resume anytime
- Flexible batch processing for large sites

---

## 📊 Progress Tracking

### Section Headers

**Feature**: Clear visual separators for each processing stage.

**Example**:
```
======================================================================
[1/7] Loading Search Console Data
======================================================================
```

### Real-Time Status Messages

**Feature**: Descriptive messages with emoji indicators.

**Status Types**:
- ✅ Success (green checkmark)
- ❌ Error (red X)
- ⚠️ Warning (yellow warning)
- 📥 Downloading
- 🔄 Processing
- 💾 Saving
- 🧪 Test Mode
- ⏸️ Paused
- 📊 Statistics

**Example**:
```
📥 Downloading sitemap...
   Attempt 1/10... ✅ Success!
✅ Extracted 1,250 URLs from sitemap

🔄 Processing existing URLs...
   📌 Matched to existing pages: 45
   ✨ New content opportunities: 32

💾 Saving results...
   ✅ Created: improvements_blog.xlsx
   ✅ Created: new_content_blog.xlsx
```

### Progress Bars

**Feature**: Visual progress indicators for long-running operations.

**Library**: `tqdm`

**Example**:
```
Scraping pages: 100%|████████████████████| 50/50 [00:42<00:00,  1.18it/s]
Processing sitemaps: 100%|█████████████████| 5/5 [00:15<00:00,  3.12s/it]
```

**Used For**:
- Page scraping
- AI processing of multiple URLs
- Sitemap downloads

### Statistics Summary

**Feature**: Final statistics after completion.

**Example (Content Optimization)**:
```
======================================================================
🎉 ALL FILES PROCESSED SUCCESSFULLY!
======================================================================
📁 Output directory: /path/to/output
📊 Processed 2 file(s)
✅ Generated 4 report(s)
```

**Example (SEO Data Collection)**:
```
======================================================================
📊 SCRAPING STATISTICS
======================================================================
  ✅ Successful: 48
  ❌ Errors: 2
  ⏱️  Timeouts: 0
  📄 Total: 50
----------------------------------------------------------------------
  💾 Output file: seo_data_example.com.xlsx
======================================================================
```

---

## 🔐 Security & Privacy

### Local Processing

- All scraping and file processing happens locally
- Only AI API calls go external
- Sitemaps cached locally
- No data sent to third parties (except configured AI provider)

### API Key Safety

- Keys stored in `config.yaml` (gitignored)
- Never logged in plain text
- Only last 10 chars shown in connection test

### Backup Protection

- Original files never modified
- Backups created before processing
- Resume functionality prevents data loss

---

## 🚀 Performance Optimization

### Caching

- Sitemaps cached to avoid re-downloads
- Existing scraped data reused on resume
- Reduces API calls and bandwidth

### Batch Processing

- Configurable batch sizes
- User-controlled pauses
- Memory-efficient for large sites

### Parallel Operations

- Could be extended with async processing (future enhancement)
- Currently sequential for reliability and rate limit compliance

---

## 📝 Logging

### Log File

**Location**: `seo_optimizer.log`

**Format**:
```
2025-10-11 14:32:15,123 - __main__ - INFO - SEO Content Optimizer initialized
2025-10-11 14:32:20,456 - src.data_loader - INFO - Loaded 1000 queries
2025-10-11 14:32:25,789 - src.sitemap_manager - INFO - Downloaded sitemap
```

###Levels

- **INFO**: Normal operations
- **WARNING**: Non-fatal issues (e.g., single page scrape failed)
- **ERROR**: Recoverable errors (e.g., API retry)
- **DEBUG**: Detailed diagnostic info (with `-v` flag)

### Viewing Logs

```bash
# View recent logs
tail -f seo_optimizer.log

# Search for errors
grep ERROR seo_optimizer.log

# View with verbose mode
python3 main.py --mode content -v
```

---

## 💡 Best Practices

### Content Optimization Mode

1. **Monthly cadence**: Run monthly to track improvements
2. **Focus on quick wins**: Target positions 11-20 first
3. **Implement top 10**: Don't overwhelm yourself, start with top opportunities
4. **Track results**: Re-export Search Console data after 30 days

### SEO Data Collection Mode

1. **Start with test mode**: Verify sitemap structure first
2. **Use manageable batches**: 50-100 pages for large sites
3. **Resume capability**: Pause anytime, no pressure to finish
4. **Fix and re-scrape**: After fixing issues, scrape again to verify

### General

1. **Test mode first**: Always test before full run
2. **Review AI suggestions**: AI provides ideas, you make final decisions
3. **Version control**: Keep old Excel outputs for comparison
4. **Regular audits**: Schedule quarterly comprehensive audits

---

**For more information, see [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)**

