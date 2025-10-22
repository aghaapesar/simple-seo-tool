# Word Export Guide - Language Support

This guide explains the enhanced Word document export features with automatic language detection and text direction support.

## 🌍 Language Detection & Text Direction

### Automatic Language Detection

The system automatically detects whether text is Persian/Farsi or English and sets appropriate text direction:

- **Persian Text**: Right-to-left (RTL) alignment
- **English Text**: Left-to-right (LTR) alignment
- **Mixed Content**: Each part gets appropriate direction

### How It Works

1. **Character Analysis**: Counts Persian/Arabic Unicode characters vs Latin characters
2. **Language Decision**: If more Persian characters → Persian, otherwise English
3. **Direction Setting**: RTL for Persian, LTR for English
4. **Word Properties**: Uses Word's native textDirection and bidi properties

## 📝 Supported Content Types

### Headings (H1-H6)
- Automatic language detection
- Proper text direction for each heading
- Maintains heading hierarchy

### Paragraphs
- Language-aware alignment
- RTL for Persian paragraphs
- LTR for English paragraphs

### Lists (Bullet & Numbered)
- Each list item gets proper direction
- Maintains list formatting
- Direction-aware bullet points

### Inline Formatting
- **Bold text**: Direction-aware bold formatting
- **Italic text**: Direction-aware italic formatting
- **Mixed formatting**: Each part gets appropriate direction

## 🔧 Technical Implementation

### LanguageDetector Class

```python
# Detect language
language = LanguageDetector.detect_language("سلام دنیا")  # Returns 'persian'
direction = LanguageDetector.get_text_direction("Hello world")  # Returns 'ltr'
```

### Unicode Ranges

- **Persian/Arabic**: `\u0600` to `\u06FF`
- **English/Latin**: Basic ASCII letters (a-z, A-Z)

### Word XML Properties

- **RTL Direction**: `<w:textDirection w:val="rl"/>`
- **LTR Direction**: `<w:textDirection w:val="lr"/>`
- **Bidirectional**: `<w:bidi/>` for RTL text

## 📊 Examples

### Persian Content
```
Input: "این یک مقاله فارسی است"
Output: Right-aligned paragraph with RTL direction
```

### English Content
```
Input: "This is an English article"
Output: Left-aligned paragraph with LTR direction
```

### Mixed Content
```
Input: "سلام Hello دنیا world"
Output: 
- "سلام" → RTL direction
- "Hello" → LTR direction  
- "دنیا" → RTL direction
- "world" → LTR direction
```

## 🎯 Benefits

### For Persian Content
- ✅ Proper right-to-left text flow
- ✅ Natural reading direction
- ✅ Professional document appearance
- ✅ No text direction confusion

### For English Content
- ✅ Standard left-to-right flow
- ✅ Maintains readability
- ✅ Consistent formatting

### For Mixed Content
- ✅ Each language part gets proper direction
- ✅ Seamless language switching
- ✅ Professional bilingual documents

## 🚀 Usage

### Automatic (Default)
The system automatically detects language and sets direction - no configuration needed!

### Manual Override
If needed, you can modify the `LanguageDetector` class to adjust detection logic.

## 🔍 Troubleshooting

### Text Not Aligning Correctly
- Check if text contains proper Persian/Arabic characters
- Verify Unicode encoding in source content
- Ensure Word document supports RTL languages

### Mixed Content Issues
- Each text run gets individual direction
- Long mixed sentences may need manual review
- Consider splitting very long mixed content

### Performance
- Language detection is fast (character counting)
- Minimal impact on export speed
- Cached results for repeated text

## 📋 Best Practices

### Content Preparation
1. **Clean Text**: Remove unnecessary HTML tags
2. **Proper Encoding**: Use UTF-8 encoding
3. **Language Separation**: Consider separating Persian and English content

### Document Structure
1. **Consistent Language**: Try to keep paragraphs in one language
2. **Clear Separation**: Use headings to separate language sections
3. **Professional Layout**: Review exported documents for proper alignment

## 🆕 Version History

### v2.4.5 (2024-10-22)
- ✅ Added automatic language detection
- ✅ Implemented RTL/LTR direction setting
- ✅ Enhanced mixed content support
- ✅ Improved Word document export quality

---

## 📞 Support

For issues with Word export or language detection:

1. **Check Logs**: Look for direction setting warnings
2. **Test Content**: Try with simple Persian/English text
3. **Word Version**: Ensure Word supports RTL languages
4. **Encoding**: Verify UTF-8 encoding in source content

---

**Last Updated**: October 22, 2024 (v2.4.5)
