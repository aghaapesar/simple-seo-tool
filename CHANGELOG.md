# Changelog - SEO Content Optimizer

All notable changes to this project will be documented in this file.

## v2.4.5 (2024-10-22)

### ✨ Enhanced Word Document Export with Language Support

**Persian/English Text Direction Support:**
- **Automatic Language Detection**: Detects Persian vs English text in content
- **Smart Text Direction**: Automatically sets RTL for Persian text, LTR for English text
- **Mixed Content Support**: Handles Persian-English mixed content properly
- **Paragraph-Level Direction**: Each paragraph gets appropriate text direction
- **Run-Level Direction**: Individual text runs get proper direction based on content

**Technical Implementation:**
- **LanguageDetector Class**: New class for detecting text language using Unicode ranges
- **Direction Setting**: Automatic RTL/LTR direction based on Persian/Arabic character detection
- **Word XML Properties**: Uses Word's native textDirection and bidi properties
- **Error Handling**: Graceful fallback to default alignment if direction setting fails

**Features Added:**
- **Persian Text**: Automatically right-aligned with RTL direction
- **English Text**: Left-aligned with LTR direction  
- **Mixed Content**: Each part gets appropriate direction
- **Headings**: Proper direction for all heading levels
- **Lists**: Direction-aware bullet and numbered lists
- **Inline Formatting**: Bold/italic text with proper direction

**Impact:**
- ✅ Persian content displays correctly in Word documents
- ✅ English content maintains proper left-to-right flow
- ✅ Mixed Persian-English content renders properly
- ✅ No more text direction confusion in exported documents
- ✅ Professional document appearance for both languages

**Technical Details:**
- Enhanced `HTMLToWordConverter` with language detection
- Added `LanguageDetector` class for text analysis
- Implemented `_set_paragraph_direction()` and `_set_run_direction()` methods
- Added RTL/LTR direction setting for both paragraphs and text runs
- Improved inline formatting with direction-aware text runs

---

## v2.4.4 (2024-10-22)

### 🐛 Bug Fix: GPT-5 Connection Test

**Fixed GPT-5 Connection Test Failure:**
- **Issue**: GPT-5 requires minimum 16 tokens for `max_output_tokens` parameter
- **Previous value**: Test was using 5 tokens (insufficient for GPT-5)
- **New value**: Increased to 20 tokens for compatibility with all models
- **Affected methods** (All 4 test methods updated):
  - `_test_openai()` - OpenAI direct connection
  - `_test_openai_compatible()` - OpenAI-compatible APIs (Liara, etc.)
  - `_test_anthropic()` - Claude models
  - `_test_groq()` - Groq models

**Impact:**
- ✅ All 6 Liara AI models now pass connection tests
- ✅ GPT-5 is now fully functional and ready to use
- ✅ Improved compatibility with future models that may have higher minimum token requirements

**Error Fixed:**
```
Error code: 400 - Invalid 'max_output_tokens': integer below minimum value. 
Expected a value >= 16, but got 5 instead.
```

**Technical Details:**
- Updated `max_tokens` parameter from 5 to 20 in connection test methods
- Added comments explaining the minimum token requirement
- Ensures compatibility with both older models (GPT-4, Claude) and newer models (GPT-5)

---

## v2.4.3 (2024-10-21)

### ✨ New AI Models Configuration

**Latest AI Models Added:**
- **GPT-5**: `liara_gpt5` - OpenAI's latest model via Liara
- **Claude Sonnet 4.5**: `liara_claude_sonnet_45` - Anthropic's advanced reasoning model
- **Claude 3.7 Sonnet Thinking**: `liara_claude_sonnet_37_thinking` - Extended thinking mode
- **Grok-4**: `liara_grok4` - X.AI's latest model
- **Gemini 2.5 Flash**: `liara_gemini_25_flash` - Google's fast and efficient model

**Model Configuration:**
- All models accessible through Liara's unified API
- Uses existing API key and base URL
- Models categorized into two sections:
  - **Liara AI Models**: Pre-configured with Liara credentials
  - **Direct Provider Models**: Require separate API keys

**Available Models in Selection Menu:**
1. `liara_gpt4o_mini` - GPT-4o Mini (default)
2. `liara_gpt5` - GPT-5 ✨ NEW
3. `liara_claude_sonnet_45` - Claude Sonnet 4.5 ✨ NEW
4. `liara_claude_sonnet_37_thinking` - Claude 3.7 Sonnet (Thinking) ✨ NEW
5. `liara_grok4` - Grok-4 ✨ NEW
6. `liara_gemini_25_flash` - Gemini 2.5 Flash ✨ NEW
7. And 13 more models...

**Impact:**
- Access to latest and most powerful AI models
- All models available for content generation, clustering, and synonym finding
- Easy model selection during each operation
- Better quality content with advanced models

**Technical Details:**
- Updated `config.yaml` with 5 new model configurations
- Updated `config.sample.yaml` for new users
- All models use `openai_compatible` provider for unified API access
- Organized models into logical categories for better readability
- Created `AI_MODELS.md` - comprehensive model documentation with use case recommendations

**Documentation:**
- New file: `AI_MODELS.md` - Complete guide to all 18 available models
- Includes model comparison, use case recommendations, and configuration examples
- Detailed tables for quick reference
- Setup instructions for both Liara and direct provider models

---

## v2.4.2 (2024-10-21)

### ✨ Enhanced User Experience

**Flexible Folder Selection for Content Generation (Mode 3):**
- **User Choice**: Users can now choose between `input/` or `output/` folders for Excel file selection
- **Interactive Selection**: Added prompt to select source folder before file selection
  - Option 1: `output/` - Files generated from content optimization mode
  - Option 2: `input/` - User's own Excel files
- **Default Behavior**: Defaults to `output/` folder (press Enter for quick selection)
- **Better Guidance**: Improved error messages with suggestions for both folder options

**Simplified Synonym Finder (Mode 5):**
- **Default to input/**: Synonym finder now defaults to `input/` folder (standard location)
- **Cleaner UI**: Removed redundant folder choice prompt
- **Automatic Detection**: Scans `input/` folder automatically for Excel files

**Impact:**
- Users have full flexibility to use any Excel files from any folder
- No need to move files between folders
- Works with both generated files and custom Excel files
- Better user experience with clear folder selection options

**Technical Details:**
- Enhanced `run_content_generation()` in `main.py` with folder selection prompt
- Simplified `run_synonym_finder()` to use default `input/` folder
- Added conditional help messages based on selected folder

---

## v2.4.1 (2024-10-21)

### 🐛 Bug Fixes

**File Selector Module:**
- **Fixed incorrect directory path in error messages**
  - When using custom directories (e.g., `output/` for content generation mode)
  - Error message now correctly displays the actual searched directory
  - Previously showed default `input/` directory even when searching elsewhere
  - Issue: Lines 109-124 in `file_selector.py` restored original directory before showing error
  - Fix: Now uses `search_dir` variable to show correct path in error messages

**Impact:**
- Users no longer confused about which directory to place files in
- Clear guidance when files are not found in the expected location
- Better user experience for Mode 3 (Content Generation) and Mode 5 (Synonym Finder)

**Technical Details:**
- Refactored `select_files_interactive()` method in `src/file_selector.py`
- Introduced `search_dir` variable to track actual search directory
- Preserved directory state management while fixing error message accuracy
- Added English comments explaining input/output behavior

---

## v2.4.0 (2024-10-13)

### ✨ New Mode 5: Keyword Synonym Finder 🔍

**Major Feature:**
- Find all semantic equivalents for keywords using AI
- Support for 8 categories of variations:
  1. Persian synonyms (مترادف‌های فارسی)
  2. Finglish standard (گوشی → gooshi, gushi)
  3. English keyboard typing (گوشی → ',ad)
  4. Colloquial abbreviations (اختصارات عامیانه)
  5. Common misspellings (غلط‌های املایی رایج)
  6. English equivalents (معادل انگلیسی)
  7. Abbreviations (مخفف‌ها)
  8. Related terms (واژگان مرتبط)

**How it Works:**
- Read keywords from Excel file (column 1)
- AI generates all possible variations
- Output Excel with 9 columns (original + 8 variation types)
- Comprehensive keyword coverage for SEO

**Use Cases:**
- Optimize content for all search variations
- Cover different ways users might search
- Improve keyword coverage
- Content localization and variations

### 📝 Content Generation Improvements

**Enhanced Prompts:**
- Stronger emphasis on NO conclusion per heading
- Clear instruction that conclusion comes ONLY at end
- Prevent phrases like "در نتیجه", "خلاصه" in section endings
- Added <p> tag instruction for clean HTML
- Improved conclusion prompt for comprehensive summary

**Result:**
- Clean, flowing content without multiple conclusions
- Single comprehensive conclusion at article end
- Better HTML rendering in browser

### 🔗 Internal Linking Improvements

**Duplicate Link Prevention:**
- Added final cleanup pass to remove duplicate URL links
- Keeps only first occurrence of each URL
- Replaces duplicate links with plain anchor text
- Better protection against same URL with different anchor texts

---

## v2.3.3 (2024-10-13)

### Added
- **New Mode 4: Internal Linking Only** 🔗
  - Standalone internal linking for existing content files
  - Supports HTML, Word (.docx), and text files
  - Interactive file selection from output/documents folder
  - Automatic link distribution and relevance checking
  - Preserves original file structure while adding internal links

### Enhanced
- **Content Generation Instructions**
  - Users can now provide additional content generation instructions
  - Instructions are automatically included in AI prompts
  - Supports custom structure requirements (FAQ, step-by-step guides, etc.)

### Fixed
- **Internal Linking Improvements**
  - Fixed KeyError for 'other' URL type in link distribution
  - Enhanced semantic matching for Persian content
  - Improved anchor text selection with 2-3 syllable product name priority
  - Even distribution of links throughout content (not just beginning/end)
  - One link per destination page limit implemented
  - Better relevance scoring with exact matches and keyword bonuses

### Technical
- Added comprehensive content harmony checking
- Enhanced error handling and user feedback
- Improved file export status reporting
- Better debugging and logging for internal linking process

## [2.3.2] - 2024-10-13

### 🔗 Advanced Internal Linking System

#### Smart Product Name Linking
- **2-3 Syllable Priority**: First 2-3 words of product names get highest priority for linking
- **Product Name Recognition**: 50+ Persian product words with syllable-based matching
- **Semantic Anchor Text**: Intelligent selection based on product relevance and context
- **Example**: "بذر پیاز سفید گرانوله" → links "بذر پیاز" (not "سفید")

#### Even Link Distribution
- **Content-Wide Spacing**: Links distributed evenly across entire content, not clustered
- **Two-Pass Algorithm**: First identifies all potential links, then selects for even distribution
- **Target Spacing**: Calculates optimal spacing based on content length and link count
- **Quality Preservation**: Maintains high-quality matches while ensuring even spread

#### Enhanced Word Export
- **Better Error Handling**: Added detailed logging for Word export process
- **Progress Feedback**: Real-time status updates during document creation
- **Exception Recovery**: Graceful handling of export failures with clear error messages

### Technical Improvements
- Enhanced `_find_best_anchor_text()` with product name prioritization
- Added `_find_semantic_anchor_text()` for 2-3 syllable product word matching
- Implemented `_select_links_with_even_distribution()` for optimal link placement
- Improved Persian product word database with syllable classification

---

## [2.3.1] - 2024-10-13

### 🔧 Bug Fixes & Improvements

#### Internal Linking System Enhancement
- **Improved Semantic Matching**: Enhanced algorithm for better content-to-URL relevance
- **Persian Word Relationships**: Added semantic groups for Persian content (گل، بذر، کاشت، آبیاری، خاک، کود، باغچه)
- **Better Phrase Matching**: Exact phrase matches now get 0.8 score (was lower)
- **Partial Word Support**: Added support for partial keyword matches (0.2 score)
- **URL Path Relevance**: URLs with matching terms in path get bonus points
- **Lowered Threshold**: Reduced matching threshold from 0.3 to 0.15 for more links
- **Debug Information**: Added detailed logging for link match scores and URLs

#### Word Export Fix
- **Fixed Missing Dependency**: Installed python-docx package (was causing ModuleNotFoundError)
- **Word Document Creation**: Fixed Word export functionality that was completely broken
- **Document Exporter**: Now fully functional for creating .docx files

#### Version Management
- **Dynamic Version Reading**: main.py now reads version from VERSION file automatically
- **Version File Update**: Updated VERSION file to 2.3.1
- **Banner Update**: Application banner now shows current version dynamically

### Technical Details
- Enhanced `_calculate_match_score()` method with better Persian language support
- Added `_has_semantic_similarity()` method for context-aware linking
- Improved debug logging throughout internal linking process
- Fixed python-docx import error in DocumentExporter

---

## [2.3.0] - 2024-10-12

### 🔧 Updates & Improvements (2024-10-13)

#### Content Generation Workflow Redesign
- **Automatic Topic Reading**: Main topic automatically read from first column (no manual input)
- **Header Detection**: First row treated as column headers
- **Interactive Word Count**: Ask for total article words, then distribute per heading
- **Per-Heading Generation**: Generate content for each heading separately with custom word counts
- **Introduction & Conclusion**: Automatically generated based on article content
- **Complete Articles**: Each row becomes one complete article with intro, body, and conclusion

#### Fixes
- Fixed: Content generation now reads Excel files from `output/` folder instead of `input/`
- Fixed: File selector shows files from output directory for Mode 3
- Improved: Better user guidance when no files are found

#### User Experience
- **Excel Structure**:
  - Row 1: Column headers
  - Column 1: Article topic (automatically used)
  - Columns 2-6: Additional data (predictions, clusters, content type, search intent, word count)
  - Columns 7+: H2 headings (only these used for content generation)
  - Each row = One complete article
- **Smart Column Detection**: Automatically identifies heading columns by "هدینگ H2" pattern
- **Interactive Process**: Confirm each article, set word counts, review progress
- **Smart Prompts**: Separate prompts for headings, introduction, and conclusion

### 🎉 Major Features

#### AI Content Generation System ✨ NEW
- **Content Generator**: Full Persian SEO content generation from Excel headings
- **Multi-Format Export**: Automatic export to Excel, Word (.docx), and HTML formats
- **Smart Content Prompt**: Specialized Persian SEO prompt with E-E-A-T principles
- **Natural Writing**: Random spacing variations for natural appearance
- **Batch Processing**: Process multiple headings in one run with progress tracking

#### Multi-Model AI Support 🤖 NEW
- **Multiple Provider Support**: OpenAI, Claude (Anthropic), Gemini (Google), Grok
- **Model Configuration**: Configure unlimited AI models in `config.yaml`
- **Connection Testing**: Test all configured models before use
- **Default Model**: Set a default model for all operations
- **Per-Operation Selection**: Choose different models for different tasks
- **Environment Variables**: Support for `env:VAR_NAME` to read API keys securely

#### Smart Internal Linking System 🔗 NEW
- **Sitemap Analysis**: Parse and categorize URLs from sitemap
- **URL Categorization**: Automatic detection of categories, products, blogs
- **Semantic Matching**: Links based on content relevance
- **Smart Rules Implementation**:
  - 1 link per 300-400 words
  - No links in headings
  - Priority system: Categories > Products > Blog posts
  - Anchor text optimization (max 5 syllables)
- **Fuzzy Matching**: Intelligent anchor text selection with similarity matching

#### Document Export System 📄 NEW
- **Word Export**: Formatted .docx documents with proper structure
- **HTML Export**: Editor-ready HTML (no wrapper tags)
- **SEO Information**: Separate title and meta description sections
- **Batch Export**: Export all generated content at once
- **Structure Preservation**: Maintains headings, bold text, lists, links

### 🛠️ New Modules

- `src/ai_model_manager.py`: Multi-provider AI model management
- `src/content_generator.py`: AI content generation engine
- `src/internal_linker.py`: Smart internal linking system
- `src/document_exporter.py`: Word and HTML export functionality

### 🔧 Configuration Changes

- Added `ai_models` section in `config.yaml` for multi-model configuration
- Legacy `ai` section maintained for backward compatibility
- Support for environment variable API keys with `env:` prefix

### 📦 Dependencies

- Added `python-docx>=0.8.11` for Word document generation
- Added `google-generativeai>=0.3.0` for Gemini support

### 🎨 User Interface

- New mode selection option: "AI Content Generation"
- Interactive model selection interface
- Progress bars for content generation and export
- Connection status display for all configured models
- Comprehensive statistics after content generation

### 📝 Content Generation Features

- Custom word count per heading
- Persian-aware content structure
- SEO title generation (max 60 chars)
- Meta description generation (max 160 chars)
- HTML content with proper tags (H2, H3, p, strong, ul, li, a)
- JSON response parsing with fallback
- Error handling and retry logic

### 🔗 Internal Linking Features

- URL type detection (category, product, blog, other)
- Semantic relevance scoring
- Anchor text extraction from URLs
- Distribution balancing (equal spread across types)
- Section-based link placement (avoid headers)
- Statistics reporting

### 📊 Export Features

- Excel: Combined output with SEO info and content
- Word: Formatted documents with sections
- HTML: Clean output for CMS/editors
- Batch processing with error handling
- Safe filename generation from titles

### 🐛 Bug Fixes

- Fixed pandas import in main.py for content generation
- Improved error messages for missing dependencies
- Better handling of malformed JSON responses from AI

### 📖 Documentation

- Complete README update with Mode 3 documentation
- Persian documentation for new features
- Configuration examples for all supported providers
- Workflow examples for content generation
- Troubleshooting section updates

### 🚀 Performance

- Parallel processing support for content generation
- Efficient sitemap parsing and caching
- Optimized internal link matching algorithms

---

## [2.2.3] - 2024-10-11

### 🔄 Smart Clustering & Fallback Strategy
- **Intelligent Duplicate Detection**: Improved threshold system (default 0.95, adjustable to 0.85)
- **Fallback Clustering**: Multiple retry strategies when all clusters are filtered as duplicates
- **User-Guided Recovery**: Interactive options to adjust clustering parameters
- **Test Mode Support**: Clustering now works properly in test mode with limited data
- **Threshold Adjustment**: Option to lower duplicate detection threshold on demand

### 🐛 Bug Fixes
- Fixed issue where all clusters were being filtered as duplicates
- Fixed empty output folder when clustering fails
- Improved duplicate detection algorithm to be less aggressive
- Added proper fallback when no unique clusters are found

### 🎯 Clustering Improvements
- Better duplicate detection with weighted similarity scoring
- More lenient threshold for title similarity (0.8 weight vs 0.3 for keywords)
- Interactive retry options for failed clustering attempts
- Support for different AI parameters when retrying

### 📊 User Experience
- Clear error messages when clustering fails
- Interactive recovery options instead of silent failures
- Test mode properly limits clustering data
- Better feedback on clustering success/failure

---

## [2.2.0] - 2024-10-11

### 🎯 Persian Language Optimization (Enhanced)
- **Complete Persian AI Prompts**: All AI prompts rewritten specifically for Persian content
- **Persian Search Intent**: Focus on Iranian user behavior and search patterns  
- **Farsi SEO Best Practices**: Optimized for Google's algorithms for Persian content
- **Localized Output**: All suggestions and recommendations in Persian
- **Persian URL Decoding**: Proper handling of Persian URLs in scraping mode
- **Fully Persian Excel Output**: All column headers and content in Persian

### 🔧 Technical Improvements
- **URL Encoding Fix**: Added `_decode_persian_url()` method to properly display Persian URLs
- **Enhanced AI Prompts**: Improved prompts for better Persian content suggestions
- **Excel Localization**: All Excel column headers now in Persian
- **Better Error Handling**: Improved error messages and logging

### 📊 Output Improvements
- **Persian Column Headers**: Excel files now have Persian column names
- **Enhanced Content Suggestions**: More detailed and actionable suggestions
- **Better Keyword Clustering**: Improved clustering for Persian keywords
- **Comprehensive Analysis**: More detailed analysis for existing content

### 🐛 Bug Fixes
- Fixed Persian URL encoding issues in scraping mode
- Improved AI response parsing for Persian content
- Better handling of Persian characters in Excel output
- Enhanced error messages for Persian users

### 📚 Documentation Updates
- Updated README.md for v2.2
- Enhanced Persian documentation sections
- Added troubleshooting for Persian-specific issues
- Updated examples with Persian content

### 🔄 Migration Notes
- No breaking changes from v2.1
- All existing configurations remain compatible
- Enhanced Persian support is automatic
- Excel output format improved but backward compatible

### 📈 Performance
- Faster Persian URL processing
- Improved AI response times for Persian prompts
- Better memory usage for large Persian datasets
- Enhanced caching for Persian content analysis

### 🎯 Use Cases Enhanced
- **Persian E-commerce**: Better product content optimization
- **Persian Blogs**: Improved article suggestions and structure
- **Persian News Sites**: Enhanced content clustering and suggestions
- **Persian Educational Sites**: Better learning content optimization

### 🔒 Privacy & Security
- No changes to data handling
- All Persian content processed locally
- Enhanced logging for Persian content debugging
- Better error reporting for Persian-specific issues

---

## [2.1.0] - 2025-10-11

### 🎉 Persian Language & Knowledge Base Release

Major update focusing on Persian/Farsi content optimization and intelligent project memory.

---

### ✨ New Features

#### Persian Language Optimization 🇮🇷
- **Persian-Aware AI Prompts**
  - Complete rewrite of AI prompts in Persian
  - Deep understanding of Farsi content nuances
  - Recognition of different Persian spellings and variations
  - Analysis of Iranian user search behavior and intent
  
- **Comprehensive Persian SEO Analysis**
  - LSI keywords specific to Persian language
  - H2/H3 headings optimized for Farsi search patterns
  - Meta descriptions with character limits (60 for title, 160 for description)
  - FAQ suggestions based on Persian "People Also Ask"
  - Internal linking with proper Persian anchor texts
  - Schema markup recommendations for Persian content
  
- **Enhanced Content Suggestions**
  - Content type classification (راهنما/آموزش/مقایسه/لیست/تحلیل)
  - Search intent analysis (informational/commercial/transactional)
  - Recommended word count based on Persian content standards
  - Technical SEO suggestions for Farsi pages
  - User experience improvements for Iranian audience

#### Knowledge Base System 🧠
- **Project Memory** (`src/knowledge_base.py` - 450+ lines)
  - Track content generation history per project
  - Store metadata, clusters, and performance metrics
  - Separate directory for each project in `knowledge_base/`
  - JSON-based storage for easy access and portability
  
- **Duplicate Detection**
  - Automatic detection of similar content titles
  - Hash-based exact duplicate matching
  - Similarity scoring (configurable threshold)
  - Prevention of repetitive content suggestions
  
- **Performance Tracking**
  - Store predicted impressions vs actual results
  - Track improvement suggestions and their outcomes
  - Build training data for CTR prediction models
  - Historical analysis for better future predictions
  
- **Smart Analytics**
  - Content generation statistics
  - Keyword usage tracking
  - Performance metrics export
  - Comprehensive JSON reports

#### Interactive Project Management
- **Project Name Input**
  - Interactive prompt for project identification
  - Name validation and confirmation
  - Used as key for knowledge base organization
  
- **Knowledge Base Integration in Workflow**
  - Automatic loading of project history
  - Real-time duplicate checking during generation
  - Seamless saving of all generated content
  - Progress messages for knowledge base operations

---

### 🔧 Improvements

#### AI Processor
- Completely rewritten prompts for Persian content (`src/ai_processor.py`)
- System prompts now in Farsi with cultural context
- Enhanced JSON structure with more fields:
  - `meta_description`
  - `content_type`
  - `search_intent`
  - `recommended_word_count`
  - `lsi_keywords`
  - `internal_linking`
  - `user_experience`
  - `estimated_impact`

#### Main Application
- Added `get_project_name_interactive()` function
- Knowledge base initialization in SEOContentOptimizer class
- Import of KnowledgeBase module
- Updated banner to show v2.1
- Enhanced workflow messages

#### Documentation
- Brand names replaced with generic examples throughout
- README.md updated with v2.1 features (Persian AI + Knowledge Base)
- QUICKSTART.md enhanced with new workflow steps
- CHANGELOG.md (this file) with detailed v2.1 notes
- All examples now use "example" instead of specific brand names

#### Project Structure
- New `knowledge_base/` directory with .gitkeep
- `knowledge_base/README.md` explaining directory purpose
- Updated `.gitignore` to exclude knowledge base data (except structure)
- Better organization of project artifacts

---

### 📁 New Files

#### Core Modules
- `src/knowledge_base.py` (450+ lines)
  - KnowledgeBase class with full functionality
  - Project-specific data management
  - Duplicate detection algorithms
  - Performance tracking methods
  - Export and reporting functions

#### Documentation
- `knowledge_base/README.md`
  - Explains knowledge base directory structure
  - Usage guidelines
  - Data storage format

#### Configuration
- `.gitkeep` files in new directories
- Updated `.gitignore` patterns

---

### 🌍 Localization

#### Persian Content Focus
- All AI prompts now in Persian
- Understanding of Farsi-specific SEO challenges
- Recognition of Iranian search patterns
- Local content recommendations
- Cultural context in suggestions

#### Bilingual Documentation
- README maintains English + Persian sections
- Both sections updated with v2.1 features
- Examples in both languages
- Clear indicators for Persian-optimized features

---

### 🔄 Migration Notes (v2.0 → v2.1)

#### No Breaking Changes
- All v2.0 features remain intact
- New features are additive
- Existing workflows continue to work
- Knowledge base is optional (auto-created)

#### New Workflow Steps
1. Run application as before
2. **NEW**: Enter project name when prompted
3. Continue with file selection (as before)
4. AI now uses Persian-optimized prompts
5. **NEW**: Knowledge base auto-saves everything
6. Review enhanced output with Persian insights

#### First Run
```bash
python3 main.py --mode content

# You'll see:
📋 PROJECT IDENTIFICATION
Enter a name for this project: example.com
✅ Project name: example.com

# Knowledge base auto-created at:
# knowledge_base/example.com/
```

---

### 📊 Statistics

- **New Lines of Code**: ~500 (knowledge_base.py)
- **Updated Modules**: 3 (ai_processor.py, main.py, .gitignore)
- **Documentation Updates**: 4 files (README, QUICKSTART, CHANGELOG, PROJECT_STRUCTURE)
- **New Directories**: 1 (knowledge_base/)
- **Test Coverage**: Manual testing completed

---

### 🎯 Use Cases Enhanced

#### For Persian Content Creators
- Create SEO-optimized Farsi content
- Get culturally relevant suggestions
- Understand Iranian user intent
- Track all content in one place

#### For SEO Professionals
- Manage multiple projects efficiently
- Avoid duplicate content automatically
- Track performance predictions
- Build knowledge over time

#### For Agencies
- Separate knowledge base per client
- Consistent quality across projects
- Historical data for reporting
- Scalable content strategy

---

### 🔐 Privacy & Data

#### Knowledge Base Storage
- All data stored locally
- JSON format for transparency
- Easy to backup and migrate
- No external data transmission

#### Git Safety
- `knowledge_base/` directory in .gitignore
- Only structure files (.gitkeep, README) tracked
- Sensitive project data never committed

---

## [2.0.0] - 2025-10-11

### 🎉 Major Release - Complete Redesign

This version represents a complete overhaul with focus on user experience, interactivity, and new capabilities.

---

### ✨ New Features

#### Dual Operational Modes
- **Content Optimization Mode**: Existing functionality enhanced with better UX
- **SEO Data Collection Mode**: NEW - Scrape page titles, meta tags, and SEO elements from sitemaps

#### Interactive User Interface
- **File Selection**: Visual, interactive selection from `input/` folder
  - Multi-select support (comma-separated numbers)
  - File metadata display (size, date)
  - "Select all" and "finish" commands
  
- **Mode Selection**: Interactive prompt if mode not specified via CLI
  - Clear descriptions of each mode
  - User-friendly selection interface
  
- **Sitemap Management**: Complete redesign
  - Interactive URL input with validation
  - Automatic caching (no re-downloads)
  - 10-retry logic with exponential backoff
  - User prompts for manual retry after failures
  - Sitemap index detection with selective sub-sitemap downloads

#### Test Mode
- Limit processing to 10 items (queries or pages)
- Available in both operational modes
- Perfect for validation before full runs
- Activated via `--test` flag

#### Resume Capability
- SEO scraping can be paused and resumed
- Existing scraped pages are skipped automatically
- No lost work if interrupted (Ctrl+C, crash, etc.)
- Progress saved after each batch

#### Enhanced Progress Tracking
- Real-time progress bars using `tqdm`
- Detailed status messages with emoji indicators
- Section headers for each processing stage
- Statistics summaries at completion
- Clear error messages with suggested fixes

#### Organized Folder Structure
- `input/` - Place Excel files here
- `sitemaps/` - Cached sitemap downloads
- `output/` - Generated Excel reports
- Automatic directory creation
- Prevents file conflicts

#### Page Scraping (New Module)
- Extract title, meta description, H1, canonical URL
- Open Graph tags (og:title, og:description)
- Twitter Card tags (twitter:title, twitter:description)
- Batch processing with configurable sizes
- User-controlled pause/continue
- Error handling with status tracking
- Separate output files per sitemap/domain

---

### 🔧 Improvements

#### Data Loader
- Better column name detection
  - Supports "Top queries" → "Query" mapping
  - Case-insensitive matching
  - Multiple alternative names for each column
- Improved error messages with available columns listed
- More robust Excel parsing

#### Sitemap Manager (New Module)
- Smart caching with MD5 hash filenames
- Domain-based readable filenames
- Retry logic with exponential backoff
- Sitemap index support
- Progress tracking for multiple sitemaps
- User control at every step

#### File Selector (New Module)
- Automatic detection of `.xlsx` and `.xls` files
- Metadata display (size, modification date)
- Sorted by modification time (newest first)
- Multi-select with validation
- Clear user prompts and error handling

#### AI Processor
- Fixed "json" keyword requirement for OpenAI-compatible APIs
- Better error messages
- More robust JSON parsing with fallbacks

#### Terminal Output
- Colored output with ANSI codes (via test_connection.py pattern)
- Consistent emoji usage for status indicators
- Section dividers for clarity
- Step indicators (e.g., [1/7])
- Real-time progress updates

#### Logging
- More descriptive log messages
- Better error context
- Success confirmations
- File paths in logs for traceability

---

### 🏗️ Architecture Changes

#### New Modules
- `src/sitemap_manager.py` - Interactive sitemap downloading and caching
- `src/file_selector.py` - Interactive Excel file selection
- `src/page_scraper.py` - Web page scraping for SEO data

#### Refactored main.py
- Complete rewrite with modular design
- Two clear operational modes
- Enhanced error handling
- Better separation of concerns
- Comprehensive docstrings and comments

#### Configuration Changes
- Removed `sitemap_url` from required config (now interactive)
- `input_excel_path` optional (interactive file selection)
- Added test mode settings
- Better documentation in sample config

---

### 📚 Documentation

#### New Files
- `FEATURES.md` - Comprehensive feature documentation
- `CHANGELOG.md` - This file
- `README_NEW.md` → `README.md` - Completely rewritten

#### Updated Files
- `QUICKSTART.md` - Fully updated for v2.0
- `EXAMPLES.md` - Updated with new workflows
- `config.sample.yaml` - Better comments and examples

#### README Highlights
- Dual-mode documentation
- Step-by-step workflows
- Troubleshooting section expanded
- Use case examples
- Configuration examples for all providers

---

### 🐛 Bug Fixes

- Fixed column name matching for Google Search Console exports
- Fixed API JSON mode requirements for Liara.ir and compatible APIs
- Improved error handling for missing files
- Better validation for user inputs
- Fixed sitemap download timeout handling

---

### 🔄 Breaking Changes

#### Command Line Interface
**Old (v1.x)**:
```bash
python main.py -i search_console_data.xlsx
```

**New (v2.0)**:
```bash
# Interactive (recommended)
python3 main.py

# Or specify mode
python3 main.py --mode content
python3 main.py --mode scraping

# Test mode
python3 main.py --mode content --test
```

#### File Organization
- Excel files must now be in `input/` folder
- Sitemaps cached in `sitemaps/` folder
- Output remains in `output/` folder

#### Configuration
- `sitemap_url` no longer required (interactive input)
- `input_excel_path` no longer required (interactive selection)

---

### 📦 Dependencies

#### Added
- `beautifulsoup4>=4.12.0` - For HTML parsing in page scraper

#### Updated
- All existing dependencies to latest compatible versions

---

### ⚡ Performance

- Sitemap caching reduces redundant downloads
- Resume capability prevents duplicate work
- Batch processing for memory efficiency
- Rate limiting respects API quotas

---

### 🔐 Security

- API keys never logged in plain text
- Config file in `.gitignore`
- Local processing, minimal external calls
- Backup creation before processing

---

### 🎯 Migration Guide (v1.x → v2.0)

#### Step 1: Update Files
```bash
git pull  # or download new version
pip3 install -r requirements.txt
```

#### Step 2: Move Excel Files
```bash
mkdir -p input
mv your_search_console_data.xlsx input/
```

#### Step 3: Update config.yaml
- Remove or comment out `sitemap_url` (now interactive)
- Remove or comment out `input_excel_path` (now interactive)

#### Step 4: Run New Interface
```bash
python3 main.py
```

Follow interactive prompts!

---

### 📊 Statistics

- **Lines of Code**: ~2,500+ (from ~800)
- **New Modules**: 3 (sitemap_manager, file_selector, page_scraper)
- **Documentation Pages**: 5 (README, QUICKSTART, FEATURES, CHANGELOG, EXAMPLES)
- **Test Coverage**: Manual testing completed for all features

---

### 🙏 Acknowledgments

- Built for SEO professionals and content marketers
- Inspired by feedback from v1.x users
- Designed for ease of use and reliability

---

### 📅 Future Roadmap

#### Planned for v2.1
- [ ] Async page scraping for faster performance
- [ ] Export to CSV in addition to Excel
- [ ] Scheduled runs (cron integration)
- [ ] Email notifications on completion

#### Under Consideration
- [ ] Web UI (Flask/Streamlit)
- [ ] Integration with Google Search Console API (direct)
- [ ] Multi-language support in AI prompts
- [ ] Custom AI prompt templates
- [ ] Historical tracking and comparison

---

### 🐛 Known Issues

None currently. Please report issues via GitHub or email.

---

### 📞 Support

- **Documentation**: See README.md, QUICKSTART.md, FEATURES.md
- **Logs**: Check `seo_optimizer.log` for debugging
- **Test**: Use `--test` flag for validation
- **Connection**: Run `test_connection.py` to verify AI setup

---

## [1.0.0] - 2025-10-11 (Earlier Version)

### Initial Release
- Basic Search Console data analysis
- AI-powered content suggestions
- Keyword clustering
- Excel output generation
- Support for multiple AI providers

---

**For detailed feature documentation, see [FEATURES.md](FEATURES.md)**

