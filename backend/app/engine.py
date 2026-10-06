from __future__ import annotations

import httpx
from bs4 import BeautifulSoup


async def search_web(query: str, limit: int = 5) -> list[dict]:
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    async with httpx.AsyncClient(timeout=20.0, headers={"User-Agent": "Mozilla/5.0"}) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    items: list[dict] = []
    for index, result in enumerate(soup.select(".result")[:limit], start=1):
        title = result.select_one(".result__title")
        link = result.select_one(".result__a")
        snippet = result.select_one(".result__snippet")
        items.append({
            "rank": index,
            "title": title.get_text(" ", strip=True) if title else f"Result {index}",
            "url": link.get("href") if link else "",
            "snippet": snippet.get_text(" ", strip=True) if snippet else "",
        })
    return items


async def read_page(url: str) -> dict:
    async with httpx.AsyncClient(timeout=20.0, headers={"User-Agent": "Mozilla/5.0"}) as client:
        response = await client.get(url)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()
    text = " ".join(soup.stripped_strings)
    return {"url": url, "text": text[:8000]}
