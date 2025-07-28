import os
import json
import argparse
from textwrap import dedent

try:
    import requests
except ImportError:
    requests = None

try:
    import openai
except ImportError:
    openai = None

SEARCH_API_URL = "https://serpapi.com/search"


def search_web(query, api_key, num_results=5):
    if requests is None:
        raise RuntimeError("The requests package is required but not installed.")
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results,
        "hl": "en",
    }
    response = requests.get(SEARCH_API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    organic = data.get("organic_results", [])
    snippets = [res.get("snippet", "") for res in organic]
    return "\n".join(snippets)


def generate_article(prompt, length, api_key=None):
    if openai is None:
        raise RuntimeError("The openai package is required but not installed.")
    openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
    system_prompt = dedent(
        f"""\
        You are an assistant that writes SEO friendly articles in Traditional Chinese.
        The article must be roughly {length} characters long.
        Provide clear formatting with headings and paragraphs.
        At the end, include a section titled 'Meta Information' with
        bullet points for the meta title and meta description.
        """
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2048,
    )
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Generate SEO optimized articles.")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--keywords", required=True, help="Comma separated keywords")
    parser.add_argument(
        "--length",
        type=int,
        default=800,
        help="Approximate character length of the article",
    )
    parser.add_argument(
        "--search-api-key",
        default=os.getenv("SERP_API_KEY"),
        help="API key for SerpAPI (environment variable SERP_API_KEY)",
    )
    parser.add_argument(
        "--openai-api-key",
        default=os.getenv("OPENAI_API_KEY"),
        help="API key for OpenAI (environment variable OPENAI_API_KEY)",
    )
    args = parser.parse_args()

    if not args.search_api_key:
        raise RuntimeError("SerpAPI key is required.")
    if not args.openai_api_key:
        raise RuntimeError("OpenAI API key is required.")

    search_snippets = search_web(args.keywords, args.search_api_key)
    prompt = f"Title: {args.title}\nKeywords: {args.keywords}\n\nContext from search results:\n{search_snippets}\n\nWrite the article:"
    article = generate_article(prompt, args.length, args.openai_api_key)
    print(article)


if __name__ == "__main__":
    main()
