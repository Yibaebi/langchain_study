from langchain_tavily import TavilySearch


def find_linkedin_profile(name_with_unique_info: str):
    """Searches the internet for a profile that matches the search crieteria"""
    search = TavilySearch()
    res = search.run(f"linkedin profile for {name_with_unique_info}")

    return res
