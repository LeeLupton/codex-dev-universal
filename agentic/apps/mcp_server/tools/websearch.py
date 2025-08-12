from packages.schema.tool_models import WebSearchIn, WebSearchOut, WebResult


def search(input: WebSearchIn) -> WebSearchOut:
    results = [WebResult(title="Example", url="http://example.com", snippet="demo")]
    return WebSearchOut(results=results)
