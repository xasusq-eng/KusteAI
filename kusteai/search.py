from duckduckgo_search import DDGS


class WebSearch:
    def search(self, query: str, max_results: int = 5) -> list[dict]:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))



def format_search_results(results: list[dict]) -> str:
    if not results:
        return "Ничего не найдено."

    lines = []
    for idx, item in enumerate(results, start=1):
        title = item.get("title", "Без заголовка")
        href = item.get("href", "")
        body = item.get("body", "")
        lines.append(f"{idx}. {title}\n{href}\n{body}")

    return "\n\n".join(lines)
