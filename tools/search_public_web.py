import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def websearch(query: str) -> str:
    """
    Search the public internet for information that may change over time or is available from public websites, including current software releases, public documentation, and external technical information.

Returns a list of public search results containing titles, URLs, and content excerpts. Use those results to answer the user's question, making clear when the evidence is incomplete.




    """

    results = tavily.search(
        query=query,
        max_results=5
    )

    if not results.get("results"):
        return "No useful web results were found."

    output = []

    for result in results["results"]:
        output.append(
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('url', '')}\n"
            f"Content: {result.get('content', '')}"
        )

    return "\n\n---\n\n".join(output)