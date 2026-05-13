from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from requests.exceptions import ConnectionError, Timeout

import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic.
    Returns Titles, URLs and snippets.
    """

    try:
        results = tavily.search(
            query=query,
            max_results=2,
            search_depth="basic"
        )

        out = []

        if not results.get("results"):
            return "No search results found."

        for r in results["results"]:
            out.append(
                f"Title: {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Snippet: {r['content'][:150]}\n"
            )

        return "\n----\n".join(out)
    except ConnectionError:
        return "Tavily connection failed. Please check internet/API status."

    except Timeout:
        return "Tavily request timed out. Please try again."

    except Exception as e:

        if "rate limit" in str(e).lower():
            return "Tavily API rate limit exceeded."

        if "quota" in str(e).lower():
            return "Tavily API quota exceeded."

        return f"Search Error: {str(e)}"



@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a given URL.
    """

    try:
        resp = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:1200]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
