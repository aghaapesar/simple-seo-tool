# Available AI Models

This document lists all AI models configured in the SEO Content Optimizer tool.

## 📊 Summary

- **Total Models**: 18
- **Default Model**: `liara_gpt4o_mini`
- **Providers**: OpenAI, Anthropic (Claude), Google (Gemini), X.AI (Grok), Groq

---

## 🚀 Liara AI Models (Pre-configured)

These models are accessible through Liara's unified API with your existing credentials.

### Latest Models (v2.4.3) ✨

| Model Name | Model ID | Provider | Description |
|------------|----------|----------|-------------|
| `liara_gpt5` | `openai/gpt-5` | OpenAI | Latest GPT-5 model with advanced reasoning |
| `liara_claude_sonnet_45` | `anthropic/claude-sonnet-4.5` | Anthropic | Most advanced Claude model |
| `liara_claude_sonnet_37_thinking` | `anthropic/claude-3.7-sonnet:thinking` | Anthropic | Extended thinking mode for complex tasks |
| `liara_grok4` | `x-ai/grok-4` | X.AI | Latest Grok with real-time knowledge |
| `liara_gemini_25_flash` | `google/gemini-2.5-flash` | Google | Fast and efficient Gemini model |

### Existing Models

| Model Name | Model ID | Provider | Description |
|------------|----------|----------|-------------|
| `liara_gpt4o_mini` | `openai/gpt-4o-mini` | OpenAI | Fast, cost-effective GPT-4 variant (DEFAULT) |

---

## 🔑 Direct Provider Models (Require API Keys)

These models require separate API keys from each provider.

### OpenAI Models

| Model Name | Model ID | Required Key | Description |
|------------|----------|--------------|-------------|
| `openai_gpt4` | `gpt-4` | `OPENAI_API_KEY` | Original GPT-4 |
| `openai_gpt4o` | `gpt-4o` | `OPENAI_API_KEY` | Optimized GPT-4 |

### Anthropic Claude Models

| Model Name | Model ID | Required Key | Description |
|------------|----------|--------------|-------------|
| `claude_opus` | `claude-3-opus-20240229` | `ANTHROPIC_API_KEY` | Most capable Claude |
| `claude_sonnet` | `claude-3-5-sonnet-20241022` | `ANTHROPIC_API_KEY` | Balanced performance |
| `claude_haiku` | `claude-3-haiku-20240307` | `ANTHROPIC_API_KEY` | Fast and lightweight |

### Google Gemini Models

| Model Name | Model ID | Required Key | Description |
|------------|----------|--------------|-------------|
| `gemini_pro` | `gemini-pro` | `GOOGLE_API_KEY` | Gemini Pro for text |
| `gemini_pro_vision` | `gemini-pro-vision` | `GOOGLE_API_KEY` | Gemini with vision |

### Groq Models (Fast Inference)

| Model Name | Model ID | Required Key | Description |
|------------|----------|--------------|-------------|
| `groq_llama3_70b` | `llama3-70b-8192` | `GROQ_API_KEY` | LLaMA 3 70B |
| `groq_llama3_8b` | `llama3-8b-8192` | `GROQ_API_KEY` | LLaMA 3 8B |
| `groq_mixtral` | `mixtral-8x7b-32768` | `GROQ_API_KEY` | Mixtral 8x7B |

---

## 🎯 How to Use

### Using Liara Models (Recommended)

Liara models are pre-configured and ready to use:

```bash
# Run any mode
python3 main.py --mode generation

# When prompted, select a Liara model:
# [1] liara_gpt4o_mini (default)
# [2] liara_gpt5
# [3] liara_claude_sonnet_45
# etc...
```

### Using Direct Provider Models

1. Set environment variables with your API keys:

```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="sk-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"
export GOOGLE_API_KEY="your-key"
export GROQ_API_KEY="gsk-your-key"
```

2. Select the model during operation

---

## 📋 Model Selection by Use Case

### Content Generation (Best Quality)
1. 🥇 **liara_claude_sonnet_45** - Most advanced reasoning
2. 🥈 **liara_gpt5** - Latest OpenAI capabilities
3. 🥉 **liara_claude_sonnet_37_thinking** - Deep thinking mode

### Content Generation (Fast & Efficient)
1. 🥇 **liara_gemini_25_flash** - Very fast
2. 🥈 **liara_gpt4o_mini** - Balanced speed/quality
3. 🥉 **groq_llama3_70b** - Fastest inference

### Keyword Clustering
1. 🥇 **liara_claude_sonnet_45** - Best semantic understanding
2. 🥈 **liara_gpt5** - Excellent clustering
3. 🥉 **liara_grok4** - Real-time knowledge

### Synonym Finding
1. 🥇 **liara_claude_sonnet_37_thinking** - Deep linguistic analysis
2. 🥈 **liara_claude_sonnet_45** - Comprehensive variations
3. 🥉 **liara_gpt5** - Creative alternatives

---

## 🔧 Configuration

All models are configured in `config.yaml`:

```yaml
ai_models:
  default: "liara_gpt4o_mini"
  
  liara_gpt5:
    provider: "openai_compatible"
    api_key: "YOUR_LIARA_API_KEY"
    base_url: "https://ai.liara.ir/api/YOUR_PROJECT_ID/v1"
    model: "openai/gpt-5"
```

---

## 💡 Tips

1. **Start with Liara Models**: No extra setup needed
2. **Test Mode**: Use `--test` flag to try different models quickly
3. **Default Model**: Set your preferred model as default in `config.yaml`
4. **Model Selection**: You can choose different models for different operations
5. **API Costs**: Liara models are billed through Liara's unified pricing

---

## 🆕 Recently Added (v2.4.3)

- ✨ GPT-5
- ✨ Claude Sonnet 4.5
- ✨ Claude 3.7 Sonnet (Thinking)
- ✨ Grok-4
- ✨ Gemini 2.5 Flash

---

## 📞 Support

- For Liara API issues: [liara.ir](https://liara.ir)
- For model-specific questions: Check provider documentation
- For tool usage: See README.md and QUICKSTART.md

---

**Last Updated**: October 21, 2024 (v2.4.3)

