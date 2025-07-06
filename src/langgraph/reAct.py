from langchain.agents import tool
from langchain_tavily import TavilySearch
from langchain_anthropic import ChatAnthropic


@tool
def triple(number: float) -> float:
    """
    Returns the triple of the input number.
    """
    return number * 3


tools = [TavilySearch(max_results=1), triple]
llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)
