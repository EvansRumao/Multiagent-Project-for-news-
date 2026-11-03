from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str)-> str:
    """search the web for recent and reliable information on a topicand return the Title, URL, and Snippet """
    response = tavily_client.search(query,max_results=5)
    results = []
    for r in response['results']:
        results.append(
             f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
         )
    
    return "\n----\n".join(results)

    


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"




#print(web_search.invoke("What is the latest news on war"))
#print(scrape_url.invoke("https://abc7ny.com/post/us-iran-war-news-israels-benjamin-netanyahu-wants-donald-trump-administration-carry-new-strikes-officials-tell-ap/20009648/"))