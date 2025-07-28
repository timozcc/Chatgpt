# Chatgpt

This repository includes a simple Python script for generating SEO friendly articles.

## Requirements

- Python 3.11+
- `requests` and `openai` packages (install via `pip install requests openai`)
- API keys for [SerpAPI](https://serpapi.com/) and [OpenAI](https://openai.com/)

Due to the environment, dependencies may need to be installed manually.

## Usage

Run the script with the desired title, keywords, and length:

```bash
python3 seo_article_generator.py \
  --title "My Article" \
  --keywords "example,seo" \
  --length 800 \
  --search-api-key YOUR_SERP_API_KEY \
  --openai-api-key YOUR_OPENAI_API_KEY
```

The program searches the web for the provided keywords and uses the OpenAI API to
generate a unique article. At the end of the article, meta information is
included for SEO optimization. The generated article is written in Traditional
Chinese.
