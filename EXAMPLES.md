# Usage Examples & Workflow

This guide provides real-world examples and workflows for using the SEO Content Optimizer.

---

## 📊 Example 1: Basic Analysis

### Scenario
You have a blog with 200 queries in Google Search Console, and you want to find content opportunities.

### Workflow

1. **Export Data from Google Search Console**
   - Filter: Last 3 months
   - Export all queries (not filtered by page)
   - Save as `blog_queries_q4_2024.xlsx`

2. **Configure the tool**
```yaml
app:
  sitemap_url: "https://yourblog.com/sitemap.xml"
  min_position: 10
  input_excel_path: "blog_queries_q4_2024.xlsx"
```

3. **Run analysis**
```bash
python main.py -i blog_queries_q4_2024.xlsx
```

4. **Review results**
   - Check `existing_content_improvements.xlsx` for pages ranking 11-20
   - Check `new_content_suggestions.xlsx` for new article ideas

### Expected Output
- 20-30 existing pages with improvement suggestions
- 10-15 new content ideas clustered by topic

---

## 📊 Example 2: E-commerce Site Optimization

### Scenario
E-commerce site with 1000+ product pages. Want to improve product descriptions and category pages.

### Workflow

1. **Filter Search Console Data**
   - Export queries for specific sections
   - Or export all and filter position > 15

2. **Configure for high-traffic focus**
```yaml
app:
  min_position: 15  # Focus on queries further from page 1
  clustering_threshold: 0.8  # Stricter clustering for product-focused content
```

3. **Run with verbose logging**
```bash
python main.py -i products_queries.xlsx -v
```

4. **Analyze results**
   - Improvement suggestions → Update product descriptions
   - Keyword clusters → Create new category pages

---

## 📊 Example 3: Multi-language Site

### Scenario
Website with English and Spanish versions. Analyze each separately.

### Workflow

1. **Filter by language in Search Console**
   - Export English queries → `queries_en.xlsx`
   - Export Spanish queries → `queries_es.xlsx`

2. **Create separate configs**

`config_en.yaml`:
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  # ... API settings
app:
  sitemap_url: "https://example.com/en/sitemap.xml"
  input_excel_path: "queries_en.xlsx"
  output_directory: "output/en"
```

`config_es.yaml`:
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  # ... API settings
app:
  sitemap_url: "https://example.com/es/sitemap.xml"
  input_excel_path: "queries_es.xlsx"
  output_directory: "output/es"
```

3. **Run separately**
```bash
python main.py -c config_en.yaml
python main.py -c config_es.yaml
```

---

## 📊 Example 4: Local Business SEO

### Scenario
Local service business (e.g., plumber, lawyer) wanting to rank for local queries.

### Workflow

1. **Export geo-specific data**
   - Filter by country/region in Search Console
   - Focus on "near me" and location-based queries

2. **Configure for local SEO**
```yaml
app:
  sitemap_url: "https://localbusiness.com/sitemap.xml"
  min_position: 5  # Even position 6-10 matters for local
  max_headings_per_article: 6  # Shorter, local-focused content
```

3. **AI prompts will focus on**
   - Local intent keywords
   - Service area coverage
   - Local landing pages

---

## 📊 Example 5: Content Gap Analysis

### Scenario
Competitor analysis - find topics they rank for but you don't.

### Workflow

1. **Gather competitor queries** (manual or tools)
   - Create `competitor_queries.xlsx` with same format
   - Columns: Query, Clicks (set to 0), Impressions (estimated), CTR, Position (estimated)

2. **Run analysis**
```bash
python main.py -i competitor_queries.xlsx
```

3. **Focus on new_content_suggestions.xlsx**
   - These are topics you're missing
   - AI provides structure to create competitive content

---

## 🔄 Monthly Workflow

### Week 1: Data Collection
```bash
# Export fresh data from Search Console
# Name with date: queries_2024_10.xlsx
```

### Week 2: Analysis
```bash
# Run analysis
python main.py -i queries_2024_10.xlsx

# Compare with previous month
# Track improvements
```

### Week 3-4: Implementation
- Implement top 10 improvements from existing content
- Create 3-5 new articles from suggestions
- Track in project management tool

### Next Month: Measure Results
- Re-export data
- Compare rankings and traffic
- Iterate

---

## 💡 Pro Tips

### 1. Filtering Input Data
Before importing to the tool, filter Excel data:
- Remove branded queries (your brand name)
- Remove low-volume queries (< 10 impressions)
- Focus on specific sections if large site

### 2. Customizing AI Output
After getting suggestions, you can:
- Adjust H2 headings to match brand voice
- Combine similar article ideas
- Add brand-specific sections

### 3. Batch Processing
```bash
# Process multiple files
for file in data/*.xlsx; do
  python main.py -i "$file"
done
```

### 4. Integration with CMS
- Export improvement suggestions
- Import to your CMS via API or CSV
- Automate content briefs for writers

### 5. A/B Testing
- Implement AI suggestions on 50% of pages
- Compare performance after 30 days
- Roll out to remaining pages if successful

---

## 🔧 Advanced Configuration Examples

### High-Volume Site (10k+ queries)
```yaml
ai:
  qps: 2.0  # Faster processing if API allows
  temperature: 0.0  # Consistent results

app:
  min_position: 15  # Focus on biggest opportunities
  clustering_threshold: 0.8  # Stricter clustering
```

### Quality-Focused Site
```yaml
ai:
  qps: 0.5  # Slower, more thoughtful processing
  temperature: 0.3  # Slightly more creative suggestions
  
app:
  max_headings_per_article: 10  # Comprehensive outlines
```

### Budget-Conscious (minimize API calls)
```yaml
ai:
  qps: 0.3  # Slower to avoid rate limits
  max_retries: 2  # Fewer retries
  
# Pre-filter Excel to top 100 queries before processing
```

---

## 📈 Success Metrics

Track these metrics monthly:

1. **Queries moving from page 2 to page 1**
   - Target: 20% of improved pages

2. **New content ranking within 3 months**
   - Target: 50% of new articles on page 1-3

3. **Impressions increase**
   - Target: 30% increase in 3 months

4. **CTR improvement**
   - Target: 15% average CTR increase

---

## 🎯 Use Case Checklist

- [ ] Blog content optimization
- [ ] E-commerce product & category pages
- [ ] Local business SEO
- [ ] SaaS feature pages
- [ ] News & magazine sites
- [ ] Affiliate content sites
- [ ] Portfolio & agency sites
- [ ] Educational content
- [ ] Documentation sites
- [ ] Community & forum sites

---

**Each use case may require different configuration. Experiment and iterate!**

