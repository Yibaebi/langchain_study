from langchain_anthropic import ChatAnthropic
from langchain import hub
from langchain.agents import create_react_agent, Tool, AgentExecutor, AgentOutputParser
from tools.tools import find_linkedin_profile
from output_parsers import linked_search_result_parser


def lookup(name_with_unique_info: str):
    input_text = f"""
      Find the LinkedIn profile URL for: {name_with_unique_info}

      Please return your final answer in this format:
      {linked_search_result_parser.get_format_instructions()}
    """

    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    lookup_tools = [
        Tool(
            description="Crawl Google for user's linkedin profile",
            func=find_linkedin_profile,
            name="Useful for looking up a person's linkedin profile URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        prompt=react_prompt,
        tools=lookup_tools,
    )

    agent_executor = AgentExecutor(agent=agent, tools=lookup_tools, verbose=True)
    response = agent_executor.invoke(input={"input": input_text})
    profile_url = linked_search_result_parser.parse(response["output"])
    url = profile_url.url

    return url
