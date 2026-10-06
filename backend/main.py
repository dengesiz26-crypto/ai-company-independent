from __future__ import annotations

import httpx
from bs4 import BeautifulSoup


async def search_web(query: str, limit: int = 5) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=18.0, headers={"User-Agent": "Mozilla/5.0"}) as client:
            response = await client.get("https://duckduckgo.com/html/", params={"q": query})
            response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results: list[dict] = []
        for index, entry in enumerate(soup.select(".result")[:limit], start=1):
            title = entry.select_one(".result__title")
            link = entry.select_one(".result__a")
            snippet = entry.select_one(".result__snippet")
            results.append({
                "rank": index,
                "title": title.get_text(" ", strip=True) if title else f"Result {index}",
                "url": link.get("href") if link else "",
                "snippet": snippet.get_text(" ", strip=True) if snippet else "",
            })
        return results
    except Exception:
        return [{
            "rank": 1,
            "title": query,
            "url": "https://www.google.com/search?q=" + query.replace(" ", "+"),
            "snippet": "Live external search failed. The app kept a fallback result so the workflow continues.",
        }]


async def read_page(url: str) -> dict:
    async with httpx.AsyncClient(timeout=20.0, headers={"User-Agent": "Mozilla/5.0"}) as client:
        response = await client.get(url)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()
    text = " ".join(soup.stripped_strings)
    return {"url": url, "text": text[:8000]}


__all__ = ["search_web", "read_page"]


path="backend/app/research.py" 
