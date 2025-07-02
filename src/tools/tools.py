from langchain_tavily import TavilySearch


def find_linkedin_profile(name_with_unique_info: str):
    """Searches the internet for a profile that matches the search crieteria"""
    search = TavilySearch(max_results=5)
    res = search.invoke(f"linkedin profile for {name_with_unique_info}")

    return res
